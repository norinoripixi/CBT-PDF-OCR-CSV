from pdf2image import convert_from_path
import tempfile

def convert_pdf_to_images(pdf_file, dpi=200):
    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file)
        tmp_file_path = tmp_file.name

    # パスから変換
    images = convert_from_path(tmp_file_path, dpi=dpi, fmt='png')
    return images
