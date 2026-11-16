import fitz
from docx import Document
from io import BytesIO


def extract_text_from_pdf(file_content: bytes) -> str:
    text = []

    with fitz.open(stream=file_content, filetype="pdf") as pdf:
        for page in pdf:
            text.append(page.get_text())

    return "\n".join(text).strip()


def extract_text_from_docx(file_content: bytes) -> str:
    document = Document(BytesIO(file_content))

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                text.append(cell.text)

    return "\n".join(text).strip()


def extract_text_from_document(filename: str, file_content: bytes) -> str:

    if not file_content:
        raise ValueError("The uploaded document is empty.")

    extension = filename.lower().rsplit(".", 1)[-1]

    if extension == "pdf":
        extracted_text = extract_text_from_pdf(file_content)

    elif extension == "docx":
        extracted_text = extract_text_from_docx(file_content)

    else:
        raise ValueError("Unsupported file type. Upload PDF or DOCX.")

    if not extracted_text:
        raise ValueError("No readable text found.")

    return extracted_text