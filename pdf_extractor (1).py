#!/usr/bin/env python3
"""
PDF Outline Extractor for Adobe India Hackathon Challenge
Round 1A: Structured PDF Outline Extraction

This script extracts structured outlines (Title, H1/H2/H3 headings) from PDF files
and outputs them in JSON format as specified in the challenge requirements.

Author: AI Assistant
Date: July 2025
"""

import os
import json
import sys
import re
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
from collections import defaultdict
import time


class PDFOutlineExtractor:
    """
    Extracts structured outlines from PDF documents using multiple heuristics
    for heading detection based on font properties and text positioning.
    """

    def __init__(self):
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'

    def log(self, message: str):
        """Debug logging"""
        if self.debug:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def extract_title_from_metadata(self, doc: fitz.Document) -> Optional[str]:
        """Try to extract title from PDF metadata first"""
        try:
            metadata = doc.metadata
            if metadata and metadata.get('title'):
                title = metadata['title'].strip()
                if title and len(title) > 0:
                    self.log(f"Found title in metadata: {title}")
                    return title
        except Exception as e:
            self.log(f"Error extracting metadata title: {e}")
        return None

    def analyze_page_text_blocks(self, page: fitz.Page) -> List[Dict]:
        """
        Extract text blocks with detailed font and positioning information
        """
        try:
            # Get text as dictionary with detailed formatting info
            text_dict = page.get_text("dict")
            blocks = []

            for block in text_dict.get("blocks", []):
                if "lines" not in block:  # Skip image blocks
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            block_info = {
                                "text": span["text"].strip(),
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],  # Bold, italic flags
                                "bbox": span["bbox"],
                                "page": page.number + 1,
                                "x0": span["bbox"][0],
                                "y0": span["bbox"][1],
                                "x1": span["bbox"][2],
                                "y1": span["bbox"][3]
                            }
                            blocks.append(block_info)

            return blocks
        except Exception as e:
            self.log(f"Error analyzing page {page.number + 1}: {e}")
            return []

    def is_bold_text(self, span_info: Dict) -> bool:
        """
        Determine if text is bold using multiple heuristics
        """
        # Check font flags (bit 4 is bold in PyMuPDF)
        if span_info["flags"] & 2**4:  # Bold flag
            return True

        # Check font name for bold indicators
        font_name = span_info["font"].lower()
        bold_keywords = ["bold", "heavy", "black", "semibold", "demibold"]
        if any(keyword in font_name for keyword in bold_keywords):
            return True

        return False

    def clean_heading_text(self, text: str) -> str:
        """Clean and normalize heading text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove common artifacts
        text = re.sub(r'^[\d\W]*', '', text)  # Remove leading numbers/symbols
        text = re.sub(r'[\n\r\t]', ' ', text)  # Replace newlines with spaces

        return text.strip()

    def detect_title_from_first_page(self, page: fitz.Page, blocks: List[Dict]) -> Optional[str]:
        """
        Detect document title from the first page using heuristics
        """
        if page.number != 0:  # Only check first page
            return None

        # Sort blocks by position (top to bottom, left to right)
        page_blocks = [b for b in blocks if b["page"] == 1]
        page_blocks.sort(key=lambda x: (x["y0"], x["x0"]))

        # Look for title in top portion of page
        page_height = page.rect.height
        top_third = page_height * 0.33

        title_candidates = []

        for block in page_blocks[:20]:  # Check first 20 text blocks
            if block["y0"] > top_third:  # Only consider top third of page
                continue

            text = self.clean_heading_text(block["text"])
            if len(text) < 5 or len(text) > 100:  # Reasonable title length
                continue

            # Score based on font size, position, and styling
            score = 0
            score += block["size"] * 2  # Larger font = higher score
            score += 50 if self.is_bold_text(block) else 0
            score += max(0, 30 - block["y0"])  # Higher on page = higher score

            title_candidates.append((text, score))

        if title_candidates:
            # Return the highest scoring candidate
            title_candidates.sort(key=lambda x: x[1], reverse=True)
            title = title_candidates[0][0]
            self.log(f"Detected title from content: {title}")
            return title

        return None

    def classify_heading_level(self, block: Dict, avg_font_size: float, max_font_size: float) -> Optional[str]:
        """
        Classify text block as H1, H2, or H3 based on various heuristics
        """
        text = block["text"].strip()
        font_size = block["size"]

        # Skip very short or very long text
        if len(text) < 3 or len(text) > 200:
            return None

        # Skip text that looks like body content
        if len(text) > 100 and not self.is_bold_text(block):
            return None

        # Check for numbered headings (1., 1.1, 1.1.1, etc.)
        numbered_heading = re.match(r'^(\d+(\.|\)|:)+(\d+(\.|\)|:)*)*\s*[A-Za-z]', text)

        # Font size based classification
        size_ratio = font_size / avg_font_size if avg_font_size > 0 else 1

        score = 0

        # Font size score
        if size_ratio >= 1.5:
            score += 30
        elif size_ratio >= 1.2:
            score += 20
        elif size_ratio >= 1.1:
            score += 10

        # Bold text score
        if self.is_bold_text(block):
            score += 25

        # Numbered heading score
        if numbered_heading:
            score += 20

        # Position score (left-aligned text is more likely to be heading)
        if block["x0"] < 100:  # Left margin
            score += 10

        # Length score (shorter text more likely to be heading)
        if len(text) < 50:
            score += 15
        elif len(text) < 20:
            score += 25

        # Capitalization pattern
        if text.isupper() or text.istitle():
            score += 10

        # Classification thresholds
        if score >= 50:
            # Further classify based on font size and numbering pattern
            if numbered_heading:
                dots = text.count('.')
                if dots == 1:
                    return "H1"
                elif dots == 2:
                    return "H2"
                else:
                    return "H3"
            elif font_size >= max_font_size * 0.9:
                return "H1"
            elif font_size >= max_font_size * 0.8:
                return "H2"
            else:
                return "H3"
        elif score >= 35:
            return "H2"
        elif score >= 25:
            return "H3"

        return None

    def extract_outline(self, pdf_path: str) -> Dict:
        """
        Main method to extract structured outline from PDF
        """
        try:
            doc = fitz.open(pdf_path)
            self.log(f"Processing PDF: {pdf_path} ({doc.page_count} pages)")

            # Try to get title from metadata first
            title = self.extract_title_from_metadata(doc)

            # Extract all text blocks with formatting info
            all_blocks = []
            font_sizes = []

            for page_num in range(min(doc.page_count, 50)):  # Limit to 50 pages as per requirement
                page = doc.load_page(page_num)
                blocks = self.analyze_page_text_blocks(page)
                all_blocks.extend(blocks)
                font_sizes.extend([b["size"] for b in blocks])

            if not all_blocks:
                self.log("No text blocks found in PDF")
                return {"title": title or "", "outline": []}

            # Calculate font statistics
            avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12
            max_font_size = max(font_sizes) if font_sizes else 12

            self.log(f"Average font size: {avg_font_size:.2f}, Max font size: {max_font_size:.2f}")

            # If no title from metadata, try to detect from first page
            if not title:
                first_page = doc.load_page(0)
                title = self.detect_title_from_first_page(first_page, all_blocks)

            # Extract headings
            outline = []
            seen_headings = set()  # Avoid duplicates

            for block in all_blocks:
                heading_level = self.classify_heading_level(block, avg_font_size, max_font_size)

                if heading_level:
                    heading_text = self.clean_heading_text(block["text"])

                    # Avoid duplicate headings
                    heading_key = (heading_text.lower(), block["page"])
                    if heading_key in seen_headings:
                        continue
                    seen_headings.add(heading_key)

                    if heading_text:  # Only add non-empty headings
                        outline.append({
                            "level": heading_level,
                            "text": heading_text,
                            "page": block["page"]
                        })

            # Sort outline by page number and position
            outline.sort(key=lambda x: (x["page"], x["text"]))

            self.log(f"Extracted {len(outline)} headings")

            doc.close()

            return {
                "title": title or "",
                "outline": outline
            }

        except Exception as e:
            self.log(f"Error processing PDF {pdf_path}: {e}")
            return {"title": "", "outline": []}


def process_single_pdf(input_path: str, output_path: str):
    """Process a single PDF file"""
    extractor = PDFOutlineExtractor()
    result = extractor.extract_outline(input_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Processed: {input_path} -> {output_path}")


def process_pdf_directory(input_dir: str, output_dir: str):
    """Process all PDF files in the input directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all PDF files
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to process")

    for pdf_file in pdf_files:
        # Create corresponding JSON output file
        json_file = output_path / f"{pdf_file.stem}.json"

        try:
            start_time = time.time()
            process_single_pdf(str(pdf_file), str(json_file))
            end_time = time.time()

            print(f"Completed {pdf_file.name} in {end_time - start_time:.2f} seconds")

        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Extract structured outlines from PDF files")
    parser.add_argument("--input", "-i", default="/app/input", 
                       help="Input directory containing PDF files")
    parser.add_argument("--output", "-o", default="/app/output", 
                       help="Output directory for JSON files")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        os.environ['DEBUG'] = 'true'

    print("PDF Outline Extractor - Adobe India Hackathon Challenge Round 1A")
    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")

    # Check if input directory exists
    if not os.path.exists(args.input):
        print(f"Error: Input directory {args.input} does not exist")
        sys.exit(1)

    # Process all PDFs
    start_time = time.time()
    process_pdf_directory(args.input, args.output)
    end_time = time.time()

    print(f"Total processing time: {end_time - start_time:.2f} seconds")
    print("Processing complete!")


if __name__ == "__main__":
    main()
