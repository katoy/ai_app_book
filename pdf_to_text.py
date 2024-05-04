import fitz  # PyMuPDF
import argparse

def extract_text_vertically(pdf_path):
    document = fitz.open(pdf_path)
    full_text = []

    for page in document:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' in block:
                paragraph = ''
                for line in block['lines']:
                    # 行内の各スパン（テキストの断片）を連結
                    paragraph += ''.join(span['text'] for span in line['spans'])
                # 各段落を改行で区切ってリストに追加
                full_text.append(paragraph.replace('\n', ''))  # 余計な改行を削除

    document.close()
    # 段落間に改行を入れて全テキストを結合
    return "\n".join(full_text)

def main():
    parser = argparse.ArgumentParser(description="Extract vertical text from a PDF file.")
    parser.add_argument("pdf_path", help="The path to the PDF file from which to extract text.")

    args = parser.parse_args()
    extracted_text = extract_text_vertically(args.pdf_path)
    print(extracted_text)

if __name__ == "__main__":
    main()
