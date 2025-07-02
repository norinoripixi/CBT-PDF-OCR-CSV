from pdf2image import convert_from_bytes
from typing import List
import io

def convert_pdf_to_images(pdf_file: bytes, dpi=200) -> List[bytes]:
    images = convert_from_bytes(pdf_file, dpi=dpi, fmt='png')
    output_images = []
    for i, image in enumerate(images[:2]):
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        output_images.append(buffer.getvalue())
    return output_images