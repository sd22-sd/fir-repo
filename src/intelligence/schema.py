# src/intelligence/schema.py

FIR_SCHEMA = {
    "metadata": {
        "state": "UP",
        "district": None,
        "police_station": None,
        "fir_number": None,
        "year": None,
        "fir_datetime": None,
        "investigating_officer": None
    },
    "incident": {
        "occurrence_datetime": None,
        "location_description": None,
        "death": None,
        "injury": None,
        "death_count": None,
        "injury_count": None
    },
    "legal": {
        "acts": [],
        "sections": []
    },
    "vehicles": [
        {
            "role": None,  # "accused" or "victim"
            "vehicle_type": None,
            "vehicle_number": None,
            "driver_name": None,
            "driver_address": None
        }
    ],
    "people": [],
    "insurance": {
        "company": None,
        "validity": None
    },
    "narrative_summary": None
}