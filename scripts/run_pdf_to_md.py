#!/usr/bin/env python3
"""Thin wrapper for the pdf-to-md skill."""
import argparse
import sys
from pathlib import Path

from pdf_to_md import convert_pdf_to_md


def main():
    parser = argparse.ArgumentParser(description="Run the pdf-to-md skill converter")
    parser.add_argument("pdf_file", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output Markdown file path")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    output_path = Path(args.output) if args.output else None

    try:
        result = convert_pdf_to_md(pdf_path, output_path)
        print(f"[SKILL] Markdown generated: {result}")
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[ERROR] pdf-to-md skill failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
