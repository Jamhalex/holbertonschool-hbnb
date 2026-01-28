# HBnB — UML (Part 1)

This repository contains **Part 1** of the HBnB project (Holberton School): UML diagrams and a compiled technical document to guide the implementation phases.

> Educational project — not affiliated with Airbnb.

---

## Learning Objectives

By the end of Part 1, you should be able to:

- Describe a **3-layer architecture** (Presentation / Business Logic / Persistence).
- Apply the **Facade pattern** to reduce coupling between layers.
- Model core entities using a **UML class diagram** with attributes, methods, and relationships.
- Represent system behavior using **UML sequence diagrams** for API calls.
- Compile a clear **technical documentation** document used as an implementation reference.

---

## Project Structure

All deliverables are under `part1/`:

- `part1/README.md` — Main technical documentation (Task 3)
- `part1/diagrams/` — Mermaid sources (`.mmd`)
- `part1/exports/` — Rendered diagram images (`.png`)
- `part1/HBnB_Part1_Technical_Documentation.pdf` — Compiled PDF document
- `part1/regenerate.sh` — Script to regenerate diagram exports
- `part1/build_pdf.py` — Script to rebuild the PDF from PNG exports

---

## Requirements

- Ubuntu 20.04/22.04 (recommended)
- Bash
- Mermaid CLI (`mmdc`) available via `npx mmdc` or system install
- Python 3 (for PDF build)

> Note: Some environments require additional permissions for headless Chromium (Puppeteer) used by Mermaid CLI exports.

---

## Tasks Covered

### Task 0 — High-Level Package Diagram
- Three-layer architecture + Facade entry point
- Output: `part1/exports/00_package.png`

### Task 1 — Detailed Class Diagram (Business Logic)
- Entities: `User`, `Place`, `Review`, `Amenity`
- Inheritance from `BaseEntity` (`id`, `created_at`, `updated_at`)
- Output: `part1/exports/01_class_diagram.png`

### Task 2 — Sequence Diagrams (API Calls)
- User Registration
- Place Creation
- Review Submission
- List Places
- Outputs: `part1/exports/02_*.png` → `05_*.png`

### Task 3 — Documentation Compilation
- Single structured technical document with diagrams + explanatory notes
- Markdown: `part1/README.md`
- PDF: `part1/HBnB_Part1_Technical_Documentation.pdf`

---

## Usage

### View the documentation
- Open: `part1/README.md` (GitHub renders images)
- Or open the PDF: `part1/HBnB_Part1_Technical_Documentation.pdf`

### Regenerate diagram PNG exports
From the repository root:

```bash
./part1/regenerate.sh
Rebuild the PDF (optional)
python3 part1/build_pdf.py
Output:

part1/HBnB_Part1_Technical_Documentation.pdf

File Tree (Relevant)
.
├── README.md
└── part1
    ├── README.md
    ├── build_pdf.py
    ├── diagrams
    │   ├── 00_package.mmd
    │   ├── 01_class_diagram.mmd
    │   ├── 02_seq_user_register.mmd
    │   ├── 03_seq_place_create.mmd
    │   ├── 04_seq_review_submit.mmd
    │   └── 05_seq_list_places.mmd
    ├── exports
    │   ├── 00_package.png
    │   ├── 01_class_diagram.png
    │   ├── 02_seq_user_register.png
    │   ├── 03_seq_place_create.png
    │   ├── 04_seq_review_submit.png
    │   └── 05_seq_list_places.png
    ├── HBnB_Part1_Technical_Documentation.pdf
    └── regenerate.sh
Author
GitHub: Jamhalex
