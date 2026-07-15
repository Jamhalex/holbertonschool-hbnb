const API_URL = "http://127.0.0.1:5000/api/v1";
let allPlaces = [];


document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const placesList = document.getElementById("places-list");
    const priceFilter = document.getElementById("price-filter");
    const placeDetails = document.getElementById("place-details");
    const reviewForm = document.getElementById("review-form");

    checkAuthentication();

    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
    }

    if (placesList) {
        fetchPlaces();
    }

    if (priceFilter) {
        priceFilter.addEventListener(
            "change",
            handlePriceFilter
        );
    }

    if (placeDetails) {
        const placeId = getPlaceIdFromURL();

        if (placeId) {
            configureAddReviewLink(placeId);
            fetchPlaceDetails(placeId);
        } else {
            placeDetails.textContent = "Missing place ID.";
        }
    }

    if (reviewForm) {
        initializeReviewPage(reviewForm);
    }
});


function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    if (!loginLink) {
        return token;
    }

    if (token) {
        loginLink.style.display = "none";
    } else {
        loginLink.style.display = "inline-block";
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

    errorMessage.textContent = "";

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

        const data = await response.json();

        if (!response.ok) {
            errorMessage.textContent =
                data.error || data.msg || "Login failed";
            return;
        }

        if (!data.access_token) {
            errorMessage.textContent =
                "The server did not return an access token";
            return;
        }

        document.cookie =
            `token=${data.access_token}; path=/; SameSite=Lax`;

        window.location.href = "index.html";
    } catch (error) {
        errorMessage.textContent =
            "Unable to connect to the server";
    }
}


async function fetchPlaces() {
    const placesList = document.getElementById("places-list");
    const token = getCookie("token");
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            `${API_URL}/places/`,
            {
                method: "GET",
                headers
            }
        );

        if (!response.ok) {
            throw new Error(
                `Unable to load places: ${response.status}`
            );
        }

        allPlaces = await response.json();

        displayPlaces(allPlaces);
    } catch (error) {
        placesList.textContent =
            "Unable to load places. Check that the API is running.";

        console.error(error);
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById("places-list");

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
        const detailsLink = document.createElement("a");

        card.className = "place-card";
        card.dataset.price = place.price;

        title.textContent = place.title;

        description.textContent =
            place.description || "No description available.";

        price.textContent =
            `Price per night: $${place.price}`;

        detailsLink.textContent = "View Details";
        detailsLink.className = "details-button";
        detailsLink.href = `place.html?id=${place.id}`;

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(price);
        card.appendChild(detailsLink);

        placesList.appendChild(card);
    });
}


function handlePriceFilter(event) {
    const selectedValue = event.target.value;
    const placeCards = document.querySelectorAll(
        ".place-card"
    );

    placeCards.forEach((card) => {
        const price = Number(card.dataset.price);

        if (
            selectedValue === "all" ||
            price <= Number(selectedValue)
        ) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
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
        addReviewSection.style.display = "none";
        return;
    }

    addReviewSection.style.display = "block";

    if (addReviewLink) {
        addReviewLink.href =
            `add_review.html?id=${placeId}`;
    }
}


async function fetchPlaceDetails(placeId) {
    const detailsSection =
        document.getElementById("place-details");
    const token = getCookie("token");
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            `${API_URL}/places/${placeId}`,
            {
                method: "GET",
                headers
            }
        );

        if (!response.ok) {
            throw new Error(
                `Unable to load place: ${response.status}`
            );
        }

        const place = await response.json();

        displayPlaceDetails(place);
    } catch (error) {
        detailsSection.textContent =
            "Unable to load place details.";

        console.error(error);
    }
}


function displayPlaceDetails(place) {
    const detailsSection =
        document.getElementById("place-details");

    detailsSection.innerHTML = "";

    const title = document.createElement("h1");
    const info = document.createElement("div");
    const description = document.createElement("p");
    const price = document.createElement("p");
    const owner = document.createElement("p");
    const amenitiesTitle = document.createElement("h2");
    const amenitiesList = document.createElement("ul");
    const reviewsTitle = document.createElement("h2");
    const reviewsContainer = document.createElement("div");

    info.className = "place-info";

    title.textContent = place.title;

    description.textContent =
        place.description || "No description available.";

    price.textContent =
        `Price per night: $${place.price}`;

    owner.textContent =
        `Host: ${getOwnerName(place)}`;

    amenitiesTitle.textContent = "Amenities";

    const amenities = place.amenities || [];

    if (amenities.length === 0) {
        const item = document.createElement("li");

        item.textContent = "No amenities listed.";
        amenitiesList.appendChild(item);
    } else {
        amenities.forEach((amenity) => {
            const item = document.createElement("li");

            item.textContent =
                typeof amenity === "string"
                    ? amenity
                    : amenity.name || "Unnamed amenity";

            amenitiesList.appendChild(item);
        });
    }

    reviewsTitle.textContent = "Reviews";

    const reviews = place.reviews || [];

    if (reviews.length === 0) {
        const message = document.createElement("p");

        message.textContent = "No reviews yet.";
        reviewsContainer.appendChild(message);
    } else {
        reviews.forEach((review) => {
            const card = document.createElement("article");
            const text = document.createElement("p");
            const user = document.createElement("p");

            card.className = "review-card";

            text.textContent =
                review.text || "No review text.";

            user.textContent =
                `User: ${getReviewUser(review)}`;

            card.appendChild(text);
            card.appendChild(user);

            reviewsContainer.appendChild(card);
        });
    }

    info.appendChild(description);
    info.appendChild(price);
    info.appendChild(owner);
    info.appendChild(amenitiesTitle);
    info.appendChild(amenitiesList);
    info.appendChild(reviewsTitle);
    info.appendChild(reviewsContainer);

    detailsSection.appendChild(title);
    detailsSection.appendChild(info);
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

    loadReviewPlaceName(placeId, token);

    reviewForm.addEventListener("submit", (event) => {
        handleReviewSubmission(
            event,
            token,
            placeId
        );
    });
}


async function loadReviewPlaceName(placeId, token) {
    const placeName =
        document.getElementById("review-place-name");

    try {
        const response = await fetch(
            `${API_URL}/places/${placeId}`,
            {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Unable to load place.");
        }

        const place = await response.json();

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
    const reviewText = reviewTextInput.value.trim();
    const userId = getUserIdFromToken(token);

    if (!reviewText) {
        displayReviewMessage(
            "Review text is required.",
            true
        );
        return;
    }

    if (!userId) {
        displayReviewMessage(
            "Unable to identify the authenticated user.",
            true
        );
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
                    user_id: userId,
                    place_id: placeId
                })
            }
        );

        const data = await response.json();

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

        setTimeout(() => {
            window.location.href =
                `place.html?id=${placeId}`;
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

    messageElement.textContent = message;

    if (isError) {
        messageElement.classList.add("error-message");
        messageElement.classList.remove("success-message");
    } else {
        messageElement.classList.add("success-message");
        messageElement.classList.remove("error-message");
    }
}


function getUserIdFromToken(token) {
    try {
        const tokenParts = token.split(".");

        if (tokenParts.length !== 3) {
            return null;
        }

        const normalizedPayload = tokenParts[1]
            .replace(/-/g, "+")
            .replace(/_/g, "/");

        const decodedPayload = JSON.parse(
            decodeURIComponent(
                atob(normalizedPayload)
                    .split("")
                    .map((character) => {
                        return `%${(
                            "00" +
                            character.charCodeAt(0).toString(16)
                        ).slice(-2)}`;
                    })
                    .join("")
            )
        );

        return decodedPayload.sub || null;
    } catch (error) {
        console.error("Unable to decode JWT:", error);
        return null;
    }
}


function getOwnerName(place) {
    if (place.owner) {
        if (typeof place.owner === "string") {
            return place.owner;
        }

        const firstName = place.owner.first_name || "";
        const lastName = place.owner.last_name || "";
        const fullName = `${firstName} ${lastName}`.trim();

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

        const firstName = review.user.first_name || "";
        const lastName = review.user.last_name || "";
        const fullName = `${firstName} ${lastName}`.trim();

        if (fullName) {
            return fullName;
        }

        if (review.user.email) {
            return review.user.email;
        }
    }

    return review.user_id || "Unknown";
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
