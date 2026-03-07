import pandas as pd
from datetime import datetime


def json_to_excel(final_json, file_path):

    metadata = final_json.get("metadata", {})
    incident = final_json.get("incident", {})
    legal = final_json.get("legal", {})
    vehicles = final_json.get("vehicles", [])
    insurance = final_json.get("insurance", {})

    accused_vehicle = None
    victim_vehicle = None
    driver_name = None

    for v in vehicles:
        role = (v.get("role") or "").lower()

        if role == "accused":
            accused_vehicle = v.get("vehicle_number")
            driver_name = v.get("driver_name")

        if role == "victim":
            victim_vehicle = v.get("vehicle_number")

    fir_date = metadata.get("fir_datetime")
    month = None

    if fir_date:
        try:
            month = datetime.strptime(fir_date.split()[0], "%d/%m/%Y").strftime("%B")
        except:
            month = None

    sections = ", ".join(legal.get("sections", [])) if legal.get("sections") else None

    death = incident.get("death")
    injury = incident.get("injury")

    death_injury = None
    if death and injury:
        death_injury = "Death & Injury"
    elif death:
        death_injury = "Death"
    elif injury:
        death_injury = "Injury"

    row = {
        "SR. NO": None,
        "State": metadata.get("state"),
        "DISTRICT": metadata.get("district"),
        "POLICE STATION": metadata.get("police_station"),
        "YEAR": metadata.get("year"),
        "FIR No": metadata.get("fir_number"),
        "MONTH": month,
        "DEATH/INJURY": death_injury,
        "Sections": sections,
        "FIR DATE": metadata.get("fir_datetime"),
        "Accident Date": incident.get("occurrence_datetime"),
        "Accused Vehicle": accused_vehicle,
        "Victim Vehicle": victim_vehicle,
        "INSURANCE COMPANY": insurance.get("company"),
        "VALIDITY": insurance.get("validity"),
        "NUMBER OF DEATH": incident.get("death_count"),
        "NUMBER OF INJURY": incident.get("injury_count"),
        "IO": metadata.get("investigating_officer"),
        "DRIVER NAME": driver_name
    }

    df = pd.DataFrame([row])

    df.to_excel(file_path, index=False)