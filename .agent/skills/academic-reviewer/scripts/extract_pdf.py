#!/usr/bin/env python3
"""
Extract text content from PDF files for academic review.

Usage:
    python extract_pdf.py <path_to_pdf> [--output <output_path>]

Outputs the extracted text to stdout by default, or to a file if --output is specified.
Each page is delimited with a header showing the page number, making it easy to
reference specific locations in the review.

Dependencies:
    pymupdf (auto-installed if missing)
"""

import subprocess
import sys
import importlib
from pathlib import Path


def ensure_pymupdf():
    """Install pymupdf if it's not already available."""
    try:
        importlib.import_module("pymupdf")
        return True
    except ImportError:
        pass

    # Try common package managers in order of preference
    for cmd in [
        [sys.executable, "-m", "pip", "install", "--quiet", "pymupdf"],
        ["uv", "pip", "install", "--quiet", "pymupdf"],
    ]:
        try:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return False


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF file, preserving page boundaries.

    Returns a string with page-delimited text content. Each page is preceded
    by a header line like '--- Page 1 / 42 ---' so the reviewer can reference
    specific locations.
    """
    import pymupdf  # noqa: E402 — imported after ensure_pymupdf

    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    sections = []

    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text("text")

        header = f"--- Page {page_num + 1} / {total_pages} ---"
        sections.append(f"{header}\n{text.strip()}")

    doc.close()
    return "\n\n".join(sections)


def extract_images_info(pdf_path: str) -> str:
    """
    Extract metadata about images embedded in the PDF.

    Returns a summary of images found per page (count, dimensions) so
    the reviewer can assess figure placement and density without needing
    to render the PDF.
    """
    import pymupdf  # noqa: E402

    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    lines = ["# Image Summary\n"]

    total_images = 0
    for page_num in range(total_pages):
        page = doc[page_num]
        images = page.get_images(full=True)

        if images:
            lines.append(f"## Page {page_num + 1}")
            for idx, img in enumerate(images, 1):
                xref = img[0]
                width = img[2]
                height = img[3]
                lines.append(f"  - Image {idx}: {width}x{height}px (xref: {xref})")
                total_images += 1
            lines.append("")

    doc.close()

    if total_images == 0:
        return "No images found in the PDF."

    lines.insert(1, f"Total images found: {total_images} across {total_pages} pages.\n")
    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract text and image metadata from PDF files for academic review."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output", "-o", help="Write output to file instead of stdout")
    parser.add_argument(
        "--images-only",
        action="store_true",
        help="Only extract image metadata, not full text",
    )
    parser.add_argument(
        "--with-images",
        action="store_true",
        help="Include image metadata summary after the text",
    )

    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not pdf_path.suffix.lower() == ".pdf":
        print(f"Warning: File does not have .pdf extension: {pdf_path}", file=sys.stderr)

    # Ensure pymupdf is available
    if not ensure_pymupdf():
        print(
            "Error: Could not install pymupdf. Please install it manually:\n"
            "  pip install pymupdf",
            file=sys.stderr,
        )
        sys.exit(1)

    # Extract content
    if args.images_only:
        result = extract_images_info(str(pdf_path))
    else:
        result = extract_text(str(pdf_path))
        if args.with_images:
            result += "\n\n" + extract_images_info(str(pdf_path))

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        print(f"Output written to: {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
