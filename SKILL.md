---
name: pdf-to-md
description: Convert local PDF files to Markdown with extracted images using a bundled PyMuPDF-based script. Use when the user asks to turn a local .pdf into .md, extract a PDF into Markdown, preserve tables/headings/images, or batch-convert local PDF documents.
---

# PDF to Markdown

Use this skill when the user wants to convert a local PDF into a Markdown file on disk, especially when they want to preserve headings, tables, and extracted images.

## What this skill does
- Converts a local PDF into a `.md` file
- Extracts embedded images into an `images/` directory beside the output markdown
- Preserves document title, page separators, heading heuristics, and Markdown tables where possible

## When to use
- "把这个 PDF 转成 md"
- "Convert this local PDF to markdown"
- "提取 PDF 内容到 Markdown，并保留图片和表格"
- Batch conversion of local PDF files into markdown files

## Workflow
1. Confirm the input PDF path from the user.
2. If the user gave an explicit output path and it already exists, ask before overwriting.
3. Run the bundled script:
   - default output path:
     `python "C:/Users/xxxx/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/path/to/input.pdf"`
   - explicit output path:
     `python "C:/Users/xxxx/.claude/skills/pdf-to-md/scripts/run_pdf_to_md.py" "C:/path/to/input.pdf" -o "C:/path/to/output.md"`
4. After success, report:
   - generated markdown file path
   - extracted images directory path, if images were written

## Notes
- This skill writes files to disk.
- It requires `PyMuPDF` / `fitz` to be installed.
- It does not perform OCR; it extracts native PDF text, tables, and embedded images.
- Use absolute Windows paths when available.
- The underlying script emits Chinese progress logs; that is expected.
