import re

VEHICLE_REGEX = r"[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{2,4}"


def clean_vehicle_numbers(nums):

    valid = []

    for v in nums:

        if not v:
            continue

        v = v.upper().replace("-", "").replace(" ", "").strip()

        if re.search(VEHICLE_REGEX, v):
            valid.append(v)

    return list(set(valid))


def merge_reader_data(final_json, reader_data):

    metadata = final_json.get("metadata", {})
    incident = final_json.get("incident", {})
    legal = final_json.get("legal", {})
    vehicles = final_json.get("vehicles", [])

    # -----------------------------
    # Metadata overrides
    # -----------------------------

    reader_fir = reader_data.get("fir_number")
    reader_fir_datetime = reader_data.get("fir_datetime")
    reader_occurrence = reader_data.get("occurrence_datetime")

    if reader_fir:
        metadata["fir_number"] = reader_fir

    if reader_fir_datetime:
        metadata["fir_datetime"] = reader_fir_datetime

    if reader_occurrence:
        incident["occurrence_datetime"] = reader_occurrence

    # -----------------------------
    # Legal sections
    # -----------------------------

    reader_sections = reader_data.get("sections")
    if reader_sections:
        legal["sections"] = list(set(reader_sections))

    reader_acts = reader_data.get("acts")
    if reader_acts:
        legal["acts"] = list(set(reader_acts))

    # -----------------------------
    # Vehicle numbers
    # -----------------------------

    reader_vehicles = clean_vehicle_numbers(
        reader_data.get("vehicle_numbers", [])
    )

    for v in vehicles:

        current = v.get("vehicle_number")

        # keep existing if valid
        if current and re.search(VEHICLE_REGEX, current):
            continue

        # otherwise use reader detected number
        if reader_vehicles and v.get("role") == "accused":
            v["vehicle_number"] = reader_vehicles[0]
        else:
            v["vehicle_number"] = None

    # -----------------------------
    # Update JSON
    # -----------------------------

    final_json["metadata"] = metadata
    final_json["incident"] = incident
    final_json["legal"] = legal
    final_json["vehicles"] = vehicles

    return final_json