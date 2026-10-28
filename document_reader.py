
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Validate an uploaded PDF and extract its text page by page.
    """

    if uploaded_file is None:
        raise ValueError("Please upload a PDF document.")

    # Check the file extension
    filename = getattr(uploaded_file, "name", "")

    if Path(filename).suffix.lower() != ".pdf":
        raise ValueError("Invalid file type. Please upload a PDF.")

    # Read the uploaded file
    file_bytes = uploaded_file.getvalue()

    if not file_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        reader = PdfReader(BytesIO(file_bytes))

        if reader.is_encrypted:
            raise ValueError(
                "This PDF is password-protected. "
                "Please upload an accessible PDF."
            )

        if len(reader.pages) == 0:
            raise ValueError("The PDF contains no pages.")

        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            extracted_pages.append({
                "page_number": page_number,
                "text": page_text.strip()
            })

        full_text = "\n\n".join(
            f"Page {page['page_number']}:\n{page['text']}"
            for page in extracted_pages
            if page["text"]
        )

        if not full_text.strip():
            raise ValueError(
                "No readable text was found in this PDF. "
                "It may be a scanned or image-only document."
            )

        return {
            "filename": filename,
            "text": full_text,
            "pages": extracted_pages,
            "page_count": len(reader.pages),
            "character_count": len(full_text)
        }

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "Could not read this PDF. Please check that "
            "the file is valid and try another PDF."
        ) from error
