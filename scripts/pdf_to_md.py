#!/usr/bin/env python3
"""PDF to Markdown Converter"""
import argparse
import re
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("请先安装 PyMuPDF: pip install pymupdf")
    sys.exit(1)


def get_table_bboxes(page):
    bboxes = []
    try:
        tables = page.find_tables()
        if tables and tables.tables:
            for table in tables.tables:
                bboxes.append(table.bbox)
    except Exception:
        pass
    return bboxes


def is_in_tables(block, table_bboxes):
    if not table_bboxes:
        return False
    if "bbox" not in block:
        return False
    x0, y0, x1, y1 = block["bbox"]
    for tx0, ty0, tx1, ty1 in table_bboxes:
        if not (x1 < tx0 or x0 > tx1 or y1 < ty0 or y0 > ty1):
            return True
    return False


def detect_heading_level(text, font_size, is_bold):
    text = text.strip()
    if not text or len(text) > 60:
        return 0

    if re.search(r'[&=]|https?://|[:,;]\s*\d', text):
        return 0
    if re.match(r'^\d{4,}', text):
        return 0
    if re.search(r'[{}\[\]<>|\\]', text):
        return 0
    if re.match(r'^[A-Za-z0-9+/]{20,}=*$', text):
        return 0
    if re.search(r'[A-Za-z0-9+/]{10,}[+/][A-Za-z0-9+/]{10,}', text):
        return 0
    if re.match(r'^[A-Za-z0-9+/=_-]{30,}$', text):
        return 0

    if re.match(r'^\d+(\.\d+)+\s+[\u4e00-\u9fa5a-zA-Z]', text):
        dots = text.count('.')
        return min(dots + 1, 6)
    if re.match(r'^\d+(\.\d+)+$', text):
        dots = text.count('.')
        return min(dots + 1, 6)
    if re.match(r'^\d+\s+[\u4e00-\u9fa5]', text):
        return 1
    if re.match(r'^\d+\s+\d+\s*[\u4e00-\u9fa5]', text):
        return 2
    if re.match(r'^\d+\s+[A-zA-Z]', text):
        return 1

    if font_size >= 18:
        return 1
    elif font_size >= 14:
        return 2
    elif font_size >= 12 and is_bold:
        return 3
    return 0


def convert_pdf_to_md(pdf_path, output_path=None):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"文件不存在: {pdf_path}")

    if output_path is None:
        output_path = pdf_path.with_suffix('.md')
    else:
        output_path = Path(output_path)

    output_dir = output_path.parent
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    md_content = []
    md_content.append(f"# {pdf_path.stem}\n\n")
    md_content.append(f"> 来源: {pdf_path.name}  \n")
    md_content.append(f"> 页数: {total_pages}\n\n")
    md_content.append("---\n\n")

    print(f"开始转换: {pdf_path.name}")
    print(f"总页数: {total_pages}")

    for page_num in range(total_pages):
        page = doc[page_num]
        md_content.append(f"\n\n--- Page {page_num + 1} ---\n\n")
        table_bboxes = []

        tables_info = []
        try:
            tables = page.find_tables()
            if tables and tables.tables:
                for table in tables.tables:
                    table_bboxes.append(table.bbox)
                    rows = table.extract()
                    if rows and len(rows) >= 1:
                        table_md = []
                        header = [str(cell).replace('\n', '<br>') if cell else '' for cell in rows[0]]
                        table_md.append('| ' + ' | '.join(header) + ' |\n')
                        table_md.append('| ' + ' | '.join(['---'] * len(header)) + ' |\n')
                        for row in rows[1:]:
                            row_data = [str(cell).replace('\n', '<br>') if cell else '' for cell in row]
                            table_md.append('| ' + ' | '.join(row_data) + ' |\n')
                        table_md.append('\n')
                        tables_info.append((table.bbox[1], ''.join(table_md)))
        except Exception:
            pass

        text_blocks = []
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
        for block in blocks:
            if block["type"] != 0:
                continue
            if is_in_tables(block, table_bboxes):
                continue
            block_text = ""
            font_sizes = []
            is_bold = False
            for line in block.get("lines", []):
                line_text = ""
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    line_text += text
                    font_sizes.append(span.get("size", 10))
                    if span.get("flags", 0) & 16:
                        is_bold = True
                if line_text.strip():
                    block_text += line_text + "\n"
            if not block_text.strip():
                continue
            avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 10
            heading_level = detect_heading_level(block_text.strip(), avg_font_size, is_bold)
            y_pos = block.get("bbox", [0, 0, 0, 0])[1]
            text_blocks.append((y_pos, block_text, heading_level))

        all_elements = []
        for y_pos, table_md in tables_info:
            all_elements.append((y_pos, 'table', table_md))
        for y_pos, block_text, heading_level in text_blocks:
            all_elements.append((y_pos, 'text', (block_text, heading_level)))

        all_elements.sort(key=lambda x: x[0])

        for _, elem_type, content in all_elements:
            if elem_type == 'table':
                md_content.append(content)
            else:
                block_text, heading_level = content
                if heading_level > 0:
                    clean_title = block_text.strip().replace('\n', ' ')
                    md_content.append('#' * heading_level + ' ' + clean_title + '\n\n')
                else:
                    md_content.append(block_text.strip() + '\n')

        image_list = page.get_images(full=True)
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    if len(image_bytes) < 1024:
                        continue
                    image_filename = f"page{page_num + 1}_img{img_idx + 1}.{image_ext}"
                    image_path = images_dir / image_filename
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    md_content.append(f"\n![image](images/{image_filename})\n")
            except Exception:
                pass
        print(f"  处理进度: {page_num + 1}/{total_pages}")
    doc.close()
    final_content = ''.join(md_content)
    final_content = re.sub(r'\n{4,}', '\n\n\n', final_content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"\n[OK] 转换完成!")
    print(f"[OUT] 输出文件: {output_path}")
    if list(images_dir.glob("*")):
        print(f"[IMG] 图片目录: {images_dir}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='将PDF文件转换为Markdown文档')
    parser.add_argument('pdf_file', help='要转换的PDF文件路径')
    parser.add_argument('-o', '--output', help='输出Markdown文件路径')
    args = parser.parse_args()
    try:
        convert_pdf_to_md(args.pdf_file, args.output)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 转换失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
