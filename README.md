# Adobe-Project
# PDF Outline Extractor

A fast, offline tool to extract structured outlines (Title, H1/H2/H3 headings) from PDF documents into JSON format. Built for the **Adobe India Hackathon 2025 – Round 1A**.

---

## 🚀 Features

- 🧠 **Multi-heuristic heading detection** using font size, boldness, positioning & numbering
- 🏷️ **Title extraction** via PDF metadata or content analysis
- ⚡ **Fast processing**: Handles 50-page PDFs in under 10 seconds
- 📦 **Dockerized**: Runs offline in a secure, containerized environment
- 💻 **CPU-only, AMD64-compatible**: No GPU dependencies

---

## 🔍 How It Works

### Heading Detection

Uses a rule-based scoring system based on:

- **Font Analysis**
  - Font size relative to document average
  - Bold font detection via font flags or names
  - Font family consistency

- **Positional Analysis**
  - Left-aligned text
  - Vertical spacing and placement
  - Distance from margins

- **Content Analysis**
  - Numbered patterns (1., 1.1, etc.)
  - Short text likely to be a heading
  - Use of capitalization and keywords

- **Hierarchy Detection**
  - H1: Largest/boldest or numbered (1.)
  - H2: Medium size or numbered (1.1)
  - H3: Smaller or numbered (1.1.1)

### Title Extraction

- First tries **PDF metadata**
- Falls back to detecting largest styled text in the **top third of the first page**

---

## 🧰 Tech Stack

- **Python 3.9**
- **PyMuPDF (fitz)** for PDF processing
- **Docker** (for offline containerized execution)

---

## 📦 Project Structure


---

⚡ Performance
Speed: ≤ 10 seconds for 50-page PDF

Memory: Minimal usage

Architecture: Optimized for CPU-only (AMD64)

Model Size: No ML models; rule-based logic

🔐 Error Handling
Skips unreadable or malformed PDFs

Logs errors and continues processing

Outputs empty JSON if structure is not detectable

🧪 Tested On
Academic papers

Technical documentation

Business reports

Multi-language PDFs (primarily Latin scripts)

⚠️ Limitations
Heavily depends on consistent font styling

Not optimized for scanned PDFs

May struggle with multi-column layouts

Focused on English / Latin-based languages

🧠 Future Enhancements
Machine learning-based heading classification

OCR for scanned image PDFs

Complex layout support (multi-column, tables)

Enhanced language detection and support
