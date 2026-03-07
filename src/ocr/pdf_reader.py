import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text directly from PDF using PyMuPDF.
    This helps capture clean machine-readable text
    when OCR makes mistakes.
    """

    doc = fitz.open(pdf_path)

    full_text = []

    for page in doc:
        text = page.get_text()
        if text:
            full_text.append(text)

    return "\n".join(full_text)