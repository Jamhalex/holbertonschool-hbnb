#!/usr/bin/env python3
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer


def _scaled_image(path: Path, max_width: float, max_height: float) -> Image:
    img = Image(str(path))
    width, height = img.imageWidth, img.imageHeight
    scale = min(max_width / width, max_height / height, 1.0)
    img.drawWidth = width * scale
    img.drawHeight = height * scale
    return img


def main() -> None:
    root = Path(__file__).resolve().parent
    exports_dir = root / "exports"
    output_path = root / "HBnB_Part1_Technical_Documentation.pdf"

    images = {
        "package": exports_dir / "00_package.png",
        "class": exports_dir / "01_class_diagram.png",
        "seq_user_register": exports_dir / "02_seq_user_register.png",
        "seq_place_create": exports_dir / "03_seq_place_create.png",
        "seq_review_submit": exports_dir / "04_seq_review_submit.png",
        "seq_list_places": exports_dir / "05_seq_list_places.png",
    }

    missing = [str(path) for path in images.values() if not path.exists()]
    if missing:
        missing_list = "\n".join(missing)
        raise FileNotFoundError(f"Missing PNG exports:\n{missing_list}")

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading1"]
    subheading_style = styles["Heading2"]
    body_style = styles["BodyText"]
    caption_style = ParagraphStyle(
        name="Caption",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        spaceBefore=4,
        textColor="#333333",
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    story = []
    story.append(Paragraph("HBnB Part 1 Technical Documentation", title_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Introduction", heading_style))
    story.append(
        Paragraph(
            "This document consolidates the UML artifacts for HBnB Part 1 into an "
            "implementation-ready reference. It describes the intended architecture, "
            "the business entities and their relationships, and the expected API interactions.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("High-Level Architecture", heading_style))
    story.append(
        Paragraph(
            "The package diagram describes the Presentation, Business, and Persistence "
            "layers and the facade that centralizes use-case orchestration.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    page_width, page_height = letter
    max_width = page_width - 1.5 * inch
    max_height = page_height - 2.5 * inch

    story.append(_scaled_image(images["package"], max_width, max_height))
    story.append(Paragraph("Package diagram", caption_style))
    story.append(PageBreak())

    story.append(Paragraph("Business Logic Layer", heading_style))
    story.append(
        Paragraph(
            "The class diagram shows the shared BaseEntity and the core entities "
            "used to model users, places, reviews, and amenities.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(_scaled_image(images["class"], max_width, max_height))
    story.append(Paragraph("Class diagram", caption_style))
    story.append(PageBreak())

    story.append(Paragraph("API Interaction Flow", heading_style))
    story.append(
        Paragraph(
            "Each sequence diagram captures the facade-centered flow for key "
            "endpoints and the repository interactions that persist data.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    api_images = [
        ("Sequence: User registers", images["seq_user_register"]),
        ("Sequence: Place created", images["seq_place_create"]),
        ("Sequence: Review submitted", images["seq_review_submit"]),
        ("Sequence: List places", images["seq_list_places"]),
    ]
    for index, (caption, path) in enumerate(api_images):
        story.append(_scaled_image(path, max_width, max_height))
        story.append(Paragraph(caption, caption_style))
        if index < len(api_images) - 1:
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("Regeneration", heading_style))
    story.append(
        Paragraph(
            "PNG diagrams are regenerated from Mermaid source files in "
            "part1/diagrams using the regenerate.sh script, which calls npx mmdc. "
            "This PDF embeds the PNG exports from part1/exports.",
            body_style,
        )
    )

    doc.build(story)
    print(f"PDF generated at {output_path}")


if __name__ == "__main__":
    main()
