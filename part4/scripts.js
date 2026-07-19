const API_URL = "http://127.0.0.1:5000/api/v1";

let allPlaces = [];


document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const placesList = document.getElementById("places-list");
    const priceFilter = document.getElementById("price-filter");
    const countryFilter = document.getElementById("country-filter");
    const placeDetails = document.getElementById("place-details");
    const reviewForm = document.getElementById("review-form");
    const token = checkAuthentication();

    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
    }

    if (placesList) {
        if (!token) {
            window.location.href = "login.html";
            return;
        }

        fetchPlaces(token);
    }

    if (priceFilter) {
        priceFilter.addEventListener(
            "change",
            applyPlaceFilters
        );
    }

    if (countryFilter) {
        countryFilter.addEventListener(
            "change",
            applyPlaceFilters
        );
    }

    if (placeDetails) {
        initializePlaceDetailsPage();
    }

    if (reviewForm) {
        initializeReviewPage(reviewForm);
    }
});


function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    if (loginLink) {
        loginLink.style.display = token
            ? "none"
            : "inline-block";
    }

    return token;
}


async function handleLogin(event) {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const errorMessage = document.getElementById("login-error");

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    setMessage(errorMessage, "", false);

    if (!email) {
        setMessage(
            errorMessage,
            "Email is required.",
            true
        );
        emailInput.focus();
        return;
    }

    if (!password) {
        setMessage(
            errorMessage,
            "Password is required.",
            true
        );
        passwordInput.focus();
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/auth/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await parseJsonResponse(response);

        if (!response.ok) {
            setMessage(
                errorMessage,
                data.error ||
                data.msg ||
                "Login failed.",
                true
            );
            return;
        }

        if (!data.access_token) {
            setMessage(
                errorMessage,
                "The server did not return an access token.",
                true
            );
            return;
        }

        document.cookie = [
            `token=${data.access_token}`,
            "path=/",
            "SameSite=Lax"
        ].join("; ");

        window.location.href = "index.html";
    } catch (error) {
        setMessage(
            errorMessage,
            "Unable to connect to the server.",
            true
        );

        console.error(error);
    }
}


async function fetchPlaces(token) {
    const placesList = document.getElementById("places-list");

    if (!placesList) {
        return;
    }

    placesList.setAttribute("aria-busy", "true");

    try {
        const response = await fetch(
            `${API_URL}/places/`,
            {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data = await parseJsonResponse(response);

        if (response.status === 401) {
            deleteCookie("token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            throw new Error(
                data.error ||
                `Unable to load places: ${response.status}`
            );
        }

        allPlaces = Array.isArray(data)
            ? data
            : [];

        populateCountryFilter(allPlaces);
        displayPlaces(allPlaces);
    } catch (error) {
        placesList.textContent =
            "Unable to load places. Check that the API is running.";

        console.error(error);
    } finally {
        placesList.setAttribute("aria-busy", "false");
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById("places-list");

    if (!placesList) {
        return;
    }

    placesList.innerHTML = "";

    if (places.length === 0) {
        const message = document.createElement("p");

        message.textContent = "No places found.";
        placesList.appendChild(message);
        return;
    }

    places.forEach((place) => {
        const card = document.createElement("article");
        const title = document.createElement("h2");
        const description = document.createElement("p");
        const price = document.createElement("p");
        const country = document.createElement("p");
        const detailsLink = document.createElement("a");

        const placeCountry = getPlaceCountry(place);

        card.className = "place-card";
        card.dataset.price = String(place.price);
        card.dataset.country = placeCountry.toLowerCase();

        title.textContent =
            place.title || "Untitled place";

        description.textContent =
            place.description ||
            "No description available.";

        price.textContent =
            `Price per night: $${formatPrice(place.price)}`;

        if (placeCountry) {
            country.textContent =
                `Country: ${placeCountry}`;
        }

        detailsLink.textContent = "View Details";
        detailsLink.className = "details-button";
        detailsLink.href =
            `place.html?id=${encodeURIComponent(place.id)}`;

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(price);

        if (placeCountry) {
            card.appendChild(country);
        }

        card.appendChild(detailsLink);

        placesList.appendChild(card);
    });
}


function populateCountryFilter(places) {
    const countryFilter =
        document.getElementById("country-filter");

    if (!countryFilter) {
        return;
    }

    const countries = places
        .map((place) => getPlaceCountry(place))
        .filter((country) => country)
        .filter(
            (country, index, values) =>
                values.indexOf(country) === index
        )
        .sort((first, second) =>
            first.localeCompare(second)
        );

    countryFilter.innerHTML = "";

    const allOption = document.createElement("option");

    allOption.value = "all";
    allOption.textContent = "All countries";
    countryFilter.appendChild(allOption);

    countries.forEach((country) => {
        const option = document.createElement("option");

        option.value = country.toLowerCase();
        option.textContent = country;

        countryFilter.appendChild(option);
    });
}


function applyPlaceFilters() {
    const priceFilter =
        document.getElementById("price-filter");

    const countryFilter =
        document.getElementById("country-filter");

    const selectedPrice = priceFilter
        ? priceFilter.value
        : "all";

    const selectedCountry = countryFilter
        ? countryFilter.value.toLowerCase()
        : "all";

    const filteredPlaces = allPlaces.filter((place) => {
        const price = Number(place.price);
        const country = getPlaceCountry(place).toLowerCase();

        const priceMatches = (
            selectedPrice === "all" ||
            price <= Number(selectedPrice)
        );

        const countryMatches = (
            selectedCountry === "all" ||
            country === selectedCountry
        );

        return priceMatches && countryMatches;
    });

    displayPlaces(filteredPlaces);
}


function getPlaceCountry(place) {
    if (!place || typeof place !== "object") {
        return "";
    }

    if (
        typeof place.country === "string" &&
        place.country.trim()
    ) {
        return place.country.trim();
    }

    if (
        place.location &&
        typeof place.location.country === "string"
    ) {
        return place.location.country.trim();
    }

    if (
        place.address &&
        typeof place.address.country === "string"
    ) {
        return place.address.country.trim();
    }

    return "";
}


function initializePlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    const placeDetails =
        document.getElementById("place-details");

    if (!placeId) {
        placeDetails.textContent = "Missing place ID.";
        placeDetails.setAttribute("aria-busy", "false");
        hideAddReviewSection();
        return;
    }

    configureAddReviewLink(placeId);
    fetchPlaceDetails(placeId);
}


function getPlaceIdFromURL() {
    const parameters = new URLSearchParams(
        window.location.search
    );

    return parameters.get("id");
}


function configureAddReviewLink(placeId) {
    const token = getCookie("token");
    const addReviewSection =
        document.getElementById("add-review");
    const addReviewLink =
        document.getElementById("add-review-link");

    if (!addReviewSection) {
        return;
    }

    if (!token) {
        hideAddReviewSection();
        return;
    }

    addReviewSection.style.display = "block";

    if (addReviewLink) {
        addReviewLink.href =
            `add_review.html?id=${encodeURIComponent(placeId)}`;
    }
}


function hideAddReviewSection() {
    const addReviewSection =
        document.getElementById("add-review");

    if (addReviewSection) {
        addReviewSection.style.display = "none";
    }
}


async function fetchPlaceDetails(placeId) {
    const detailsSection =
        document.getElementById("place-details");

    if (!detailsSection) {
        return;
    }

    detailsSection.setAttribute("aria-busy", "true");

    try {
        const response = await fetch(
            `${API_URL}/places/${encodeURIComponent(placeId)}`,
            {
                method: "GET"
            }
        );

        const place = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(
                place.error ||
                `Unable to load place: ${response.status}`
            );
        }

        displayPlaceDetails(place);
    } catch (error) {
        detailsSection.textContent =
            "Unable to load place details.";

        console.error(error);
    } finally {
        detailsSection.setAttribute("aria-busy", "false");
    }
}


function displayPlaceDetails(place) {
    const detailsSection =
        document.getElementById("place-details");

    if (!detailsSection) {
        return;
    }

    detailsSection.innerHTML = "";

    const title = document.createElement("h1");
    const info = document.createElement("div");
    const description = document.createElement("p");
    const price = document.createElement("p");
    const owner = document.createElement("p");
    const country = document.createElement("p");
    const amenitiesTitle = document.createElement("h2");
    const amenitiesList = document.createElement("ul");
    const reviewsTitle = document.createElement("h2");
    const reviewsContainer = document.createElement("div");

    const placeCountry = getPlaceCountry(place);

    info.className = "place-info";

    title.textContent =
        place.title || "Untitled place";

    description.textContent =
        place.description ||
        "No description available.";

    price.textContent =
        `Price per night: $${formatPrice(place.price)}`;

    owner.textContent =
        `Host: ${getOwnerName(place)}`;

    if (placeCountry) {
        country.textContent =
            `Country: ${placeCountry}`;
    }

    amenitiesTitle.textContent = "Amenities";

    displayAmenities(
        place.amenities,
        amenitiesList
    );

    reviewsTitle.textContent = "Reviews";

    displayReviews(
        place.reviews,
        reviewsContainer
    );

    info.appendChild(description);
    info.appendChild(price);
    info.appendChild(owner);

    if (placeCountry) {
        info.appendChild(country);
    }

    info.appendChild(amenitiesTitle);
    info.appendChild(amenitiesList);
    info.appendChild(reviewsTitle);
    info.appendChild(reviewsContainer);

    detailsSection.appendChild(title);
    detailsSection.appendChild(info);
}


function displayAmenities(amenities, container) {
    const amenityList = Array.isArray(amenities)
        ? amenities
        : [];

    if (amenityList.length === 0) {
        const item = document.createElement("li");

        item.textContent = "No amenities listed.";
        container.appendChild(item);
        return;
    }

    amenityList.forEach((amenity) => {
        const item = document.createElement("li");

        if (typeof amenity === "string") {
            item.textContent = amenity;
        } else {
            item.textContent =
                amenity.name || "Unnamed amenity";
        }

        container.appendChild(item);
    });
}


function displayReviews(reviews, container) {
    const reviewList = Array.isArray(reviews)
        ? reviews
        : [];

    if (reviewList.length === 0) {
        const message = document.createElement("p");

        message.textContent = "No reviews yet.";
        container.appendChild(message);
        return;
    }

    reviewList.forEach((review) => {
        const card = document.createElement("article");
        const text = document.createElement("p");
        const user = document.createElement("p");
        const rating = document.createElement("p");

        card.className = "review-card";

        text.textContent =
            review.text || "No review text.";

        user.textContent =
            `User: ${getReviewUser(review)}`;

        rating.textContent =
            `Rating: ${formatRating(review.rating)}/5`;

        card.appendChild(text);
        card.appendChild(user);
        card.appendChild(rating);

        container.appendChild(card);
    });
}


function formatRating(rating) {
    const numericRating = Number(rating);

    if (
        !Number.isInteger(numericRating) ||
        numericRating < 1 ||
        numericRating > 5
    ) {
        return "Not rated";
    }

    return String(numericRating);
}


function initializeReviewPage(reviewForm) {
    const token = getCookie("token");
    const placeId = getPlaceIdFromURL();

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    if (!placeId) {
        displayReviewMessage(
            "Missing place ID.",
            true
        );

        reviewForm.style.display = "none";
        return;
    }

    loadReviewPlaceName(placeId);

    reviewForm.addEventListener(
        "submit",
        (event) => {
            handleReviewSubmission(
                event,
                token,
                placeId
            );
        }
    );
}


async function loadReviewPlaceName(placeId) {
    const placeName =
        document.getElementById("review-place-name");

    if (!placeName) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/places/${encodeURIComponent(placeId)}`,
            {
                method: "GET"
            }
        );

        const place = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(
                place.error || "Unable to load place."
            );
        }

        placeName.textContent =
            `Reviewing: ${place.title}`;
    } catch (error) {
        placeName.textContent =
            "Unable to load place information.";

        console.error(error);
    }
}


async function handleReviewSubmission(
    event,
    token,
    placeId
) {
    event.preventDefault();

    const reviewTextInput =
        document.getElementById("review-text");

    const ratingInput =
        document.getElementById("rating");

    const reviewText =
        reviewTextInput.value.trim();

    const rating = Number(ratingInput.value);

    displayReviewMessage("", false);

    if (!reviewText) {
        displayReviewMessage(
            "Review text is required.",
            true
        );

        reviewTextInput.focus();
        return;
    }

    if (
        !Number.isInteger(rating) ||
        rating < 1 ||
        rating > 5
    ) {
        displayReviewMessage(
            "Select a rating between 1 and 5.",
            true
        );

        ratingInput.focus();
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/reviews/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating,
                    place_id: placeId
                })
            }
        );

        const data = await parseJsonResponse(response);

        if (response.status === 401) {
            deleteCookie("token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            displayReviewMessage(
                data.error ||
                data.msg ||
                "Failed to submit review.",
                true
            );
            return;
        }

        displayReviewMessage(
            "Review submitted successfully!",
            false
        );

        reviewTextInput.value = "";
        ratingInput.value = "";

        setTimeout(() => {
            window.location.href =
                `place.html?id=${encodeURIComponent(placeId)}`;
        }, 1200);
    } catch (error) {
        displayReviewMessage(
            "Unable to connect to the server.",
            true
        );

        console.error(error);
    }
}


function displayReviewMessage(message, isError) {
    const messageElement =
        document.getElementById("review-message");

    if (!messageElement) {
        return;
    }

    setMessage(
        messageElement,
        message,
        isError
    );
}


function setMessage(element, message, isError) {
    if (!element) {
        return;
    }

    element.textContent = message;

    element.classList.remove(
        "error-message",
        "success-message"
    );

    if (!message) {
        return;
    }

    element.classList.add(
        isError
            ? "error-message"
            : "success-message"
    );
}


function getOwnerName(place) {
    if (place.owner) {
        if (typeof place.owner === "string") {
            return place.owner;
        }

        const fullName = getFullName(place.owner);

        if (fullName) {
            return fullName;
        }

        if (place.owner.email) {
            return place.owner.email;
        }
    }

    return place.owner_id || "Unknown";
}


function getReviewUser(review) {
    if (review.user) {
        if (typeof review.user === "string") {
            return review.user;
        }

        const fullName = getFullName(review.user);

        if (fullName) {
            return fullName;
        }

        if (review.user.email) {
            return review.user.email;
        }
    }

    return review.user_id || "Unknown";
}


function getFullName(user) {
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";

    return `${firstName} ${lastName}`.trim();
}


function formatPrice(price) {
    const numericPrice = Number(price);

    if (!Number.isFinite(numericPrice)) {
        return "0.00";
    }

    return numericPrice.toFixed(2);
}


async function parseJsonResponse(response) {
    try {
        return await response.json();
    } catch (error) {
        return {};
    }
}


function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const separatorIndex = cookie.indexOf("=");

        if (separatorIndex === -1) {
            continue;
        }

        const cookieName = cookie
            .slice(0, separatorIndex)
            .trim();

        const cookieValue = cookie
            .slice(separatorIndex + 1)
            .trim();

        if (cookieName === name) {
            return cookieValue;
        }
    }

    return null;
}


function deleteCookie(name) {
    document.cookie = [
        `${name}=`,
        "path=/",
        "Max-Age=0",
        "SameSite=Lax"
    ].join("; ");
}
