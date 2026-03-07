import re


def run_reader_extraction(reader_text):

    data = {
        "fir_number": None,
        "fir_datetime": None,
        "occurrence_datetime": None,
        "vehicle_numbers": [],
        "sections": [],
        "acts": []
    }

    text = reader_text.upper()

    # FIR NUMBER
    fir_match = re.search(r"FIR\s*NO.*?(\d{1,6})", text)
    if fir_match:
        data["fir_number"] = fir_match.group(1).zfill(4)

    # FIR DATETIME
    fir_dt = re.search(r"(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})", text)
    if fir_dt:
        data["fir_datetime"] = f"{fir_dt.group(1)} {fir_dt.group(2)}"

    # OCCURRENCE DATE
    occ_date = re.search(r"DATE\s*FROM.*?(\d{2}/\d{2}/\d{4})", text, re.DOTALL)

    # OCCURRENCE TIME
    occ_time = re.search(r"TIME\s*FROM.*?(\d{1,2}:\d{2})", text, re.DOTALL)

    if occ_date and occ_time:
        data["occurrence_datetime"] = f"{occ_date.group(1)} {occ_time.group(1)}"

    # VEHICLE NUMBERS (tolerant detection)
    vehicles = re.findall(
        r"[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,3}\s*\d{2,4}",
        text
    )

    cleaned = []

    for v in vehicles:
        plate = re.sub(r"\s+", "", v)
        cleaned.append(plate)

    if cleaned:
        data["vehicle_numbers"] = list(set(cleaned))

    # LEGAL SECTIONS
    sections = re.findall(r"\b(1\d{2}|2\d{2}|3\d{2})\b", text)

    if sections:
        data["sections"] = list(set(sections))

    if "BNS" in text:
        data["acts"].append("BNS")

    return data