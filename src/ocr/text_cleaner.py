# src/ocr/text_cleaner.py

import re


def fix_common_ocr_errors(text):
    """
    Fix common OCR numeric confusions.
    """

    replacements = {
        "O": "0",
        "l": "1",
        "I": "1",
        "०": "0",
        "१": "1",
        "२": "2",
        "३": "3",
        "४": "4",
        "५": "5",
        "६": "6",
        "७": "7",
        "८": "8",
        "९": "9"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


def normalize_dates(text):
    """
    Fix invalid date patterns like 77/72/2025
    but keep valid dates untouched.
    """

    import re

    def fix_date(match):
        day = int(match.group(1))
        month = int(match.group(2))
        year = match.group(3)

        # fix impossible days
        if day > 31:
            day = int(str(day)[-1])

        # fix impossible months only
        if month > 12 or month == 0:
            month = int(str(month)[-1])

        # ensure month never becomes 0
        if month == 0:
            month = 1

        return f"{day:02d}/{month:02d}/{year}"

    return re.sub(r'(\d{{1,2}})/(\d{{1,2}})/(\d{{4}})', fix_date, text)


def clean_text(text):
    """
    Final cleaning stage before LLM.
    """

    # Fix common OCR numeric errors
    text = fix_common_ocr_errors(text)

    # Normalize dates
    text = normalize_dates(text)

    # Remove excessive spaces but preserve line breaks
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove repeated punctuation noise
    text = re.sub(r'\.{2,}', '.', text)

    # Trim trailing spaces per line
    lines = [line.strip() for line in text.split("\n")]

    cleaned = "\n".join(lines)

    return cleaned.strip()