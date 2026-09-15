# SPDX-FileCopyrightText: 2026 Oldemar
# SPDX-License-Identifier: MIT

import os
import PyPDF2


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a given PDF file, supporting AES-encrypted documents.

    Args:
        pdf_path: Path to the input PDF file.

    Returns:
        Cleaned text string extracted from all pages.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                # Replace newlines with spaces to aid clean TTS synthesis and sentence segmentation
                text += extracted.replace("\n", " ") + " "
    return text.strip()


def load_input_text(pdf_path: str = None, text_path: str = None) -> str:
    """Loads input text from either a plain text file or a PDF document.

    Args:
        pdf_path: Path to PDF file.
        text_path: Path to plain text file (takes priority if provided).

    Returns:
        The extracted text as a string.
    """
    if text_path and os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif pdf_path and os.path.exists(pdf_path):
        return extract_text_from_pdf(pdf_path)
    else:
        target = text_path if text_path else pdf_path
        raise FileNotFoundError(f"Input file not found: {target}")
