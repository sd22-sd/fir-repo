import os
import json
import traceback

from src.ocr.ocr_pipeline import run_ocr_on_pdf
from src.ocr.text_cleaner import clean_text
from src.ocr.pdf_reader import extract_text_from_pdf

from src.intelligence.pass1_extractor import run_pass1
from src.intelligence.pass2_validator import run_pass2
from src.intelligence.reader_extractor import run_reader_extraction
from src.intelligence.reader_merger import merge_reader_data
from src.intelligence.regex_extractor import (
    extract_regex_fields,
    apply_regex_corrections
)


def run_pipeline(pdf_path):

    try:

        os.makedirs("output", exist_ok=True)

        # Fixed DPI
        dpi = 500

        # OCR
        ocr_text = run_ocr_on_pdf(pdf_path, dpi=dpi)

        with open("output/raw_ocr_text.txt", "w", encoding="utf-8") as f:
            f.write(ocr_text)

        # Clean OCR
        cleaned = clean_text(ocr_text)

        with open("output/cleaned_ocr_text.txt", "w", encoding="utf-8") as f:
            f.write(cleaned)

        # Pass 1
        structured_pass1 = run_pass1(cleaned)

        with open("output/structured_pass1.json", "w", encoding="utf-8") as f:
            json.dump(structured_pass1, f, indent=4, ensure_ascii=False)

        # Pass 2
        structured_pass2 = run_pass2(cleaned, structured_pass1)

        with open("output/structured_pass2.json", "w", encoding="utf-8") as f:
            json.dump(structured_pass2, f, indent=4, ensure_ascii=False)

        # Reader extraction
        reader_text = extract_text_from_pdf(pdf_path)

        with open("output/reader_text.txt", "w", encoding="utf-8") as f:
            f.write(reader_text)

        reader_data = run_reader_extraction(reader_text)

        # Merge reader
        final_json = merge_reader_data(structured_pass2, reader_data)

        # Regex vehicle validation
        combined_text = cleaned + "\n" + reader_text
        regex_data = extract_regex_fields(combined_text)

        final_json = apply_regex_corrections(final_json, regex_data)

        # Save final JSON
        with open("output/final_structured.json", "w", encoding="utf-8") as f:
            json.dump(final_json, f, indent=4, ensure_ascii=False)

        return final_json

    except Exception as e:

        print("\n========== FULL ERROR TRACEBACK ==========\n")
        traceback.print_exc()
        print("\n========== END TRACEBACK ==========\n")

        raise