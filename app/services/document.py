
from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text_from_file(file_content: bytes, file_extension: str) -> str:
    if not file_content:
        raise ValueError("File is empty")

    if file_extension == "txt":
        return file_content.decode("utf-8-sig")

    if file_extension == "pdf":
        pdf_file = BytesIO(file_content)
        reader = PdfReader(pdf_file)

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF files are not supported")

        extracted_pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

        return "\n".join(extracted_pages)

    raise ValueError("Unsupported file type")
