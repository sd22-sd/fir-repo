import re

# More tolerant Indian vehicle pattern
VEHICLE_REGEX = re.compile(
    r"\b[A-Z]{2}[- ]?\d{1,2}[- ]?[A-Z]{1,3}[- ]?\d{2,4}\b",
    re.IGNORECASE
)


def normalize_vehicle_text(text: str):
    """
    Fix common OCR mistakes in vehicle numbers
    and remove OCR garbage.
    """

    replacements = {
        "O": "0",
        "I": "1",
        "l": "1"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # remove OCR garbage characters
    text = re.sub(r"[^A-Z0-9\s\-]", " ", text.upper())

    return text


def normalize_vehicle_format(vehicle: str):
    """
    Convert vehicle numbers to standard format.

    UP 42 CB 8711
    UP-42-CB-8711

    → UP42CB8711
    """

    vehicle = vehicle.upper()
    vehicle = vehicle.replace(" ", "")
    vehicle = vehicle.replace("-", "")

    return vehicle


def extract_regex_fields(text: str):
    """
    Extract vehicle numbers using regex from document text.
    """

    text = normalize_vehicle_text(text)

    matches = VEHICLE_REGEX.findall(text)

    vehicles = []

    for v in matches:

        normalized = normalize_vehicle_format(v)

        # basic sanity check
        if 7 <= len(normalized) <= 11:
            vehicles.append(normalized)

    vehicles = list(set(vehicles))

    return {
        "vehicle_numbers": vehicles
    }


def apply_regex_corrections(final_json, regex_data):
    """
    Validate and correct vehicle numbers in final JSON.
    """

    vehicles = final_json.get("vehicles", [])
    detected_numbers = regex_data.get("vehicle_numbers", [])

    for v in vehicles:

        current = v.get("vehicle_number")

        if current:
            current_clean = normalize_vehicle_format(current)
        else:
            current_clean = None

        # If missing or invalid
        if not current_clean or not VEHICLE_REGEX.match(current):

            if detected_numbers and v.get("role") == "accused":
                v["vehicle_number"] = detected_numbers[0]
            else:
                v["vehicle_number"] = None

    final_json["vehicles"] = vehicles

    return final_json