def build_pass1_prompt(text):

    return f"""
You are an expert Indian FIR document analyst.

The FIR may contain Hindi and English text.

Extract structured information from the FIR.

----------------------------------------
Important instructions
----------------------------------------

1. The FIR header may contain fields like:

District/Unit (जिला/इकाई)
P.S. (थाना)

Map them to the schema as follows:

District/Unit → district  
P.S. / थाना → police_station

Example:

District/Unit: लखनऊ मध्य (कमिश्नरेट लखनऊ)  
P.S.: महानगर थाना, लखनऊ  

Output:
district = "लखनऊ मध्य"  
police_station = "महानगर थाना"

If the district contains extra text like "(कमिश्नरेट लखनऊ)",
extract only the main district name.

----------------------------------------

2. Identify vehicles and classify them as:

- "accused" (vehicle causing accident)
- "victim" (vehicle/person impacted)

Extract the vehicle model if explicitly mentioned.

Example:
"गाड़ी Tata Tiago" → vehicle_type = "Tata Tiago"

If only generic words appear such as:
गाड़ी
कार
मोटरसाइकिल

leave vehicle_type empty.

----------------------------------------

3. Extract injury and death information.

Example:

"हम दोनों घायल हो गये"

→ injury = true  
→ injury_count = "2"

----------------------------------------

4. Narrative Summary

Generate a short narrative summary of the FIR.

The summary should include:
- who was involved
- where the incident occurred
- what happened
- which vehicle caused the accident
- the outcome (injury or death)

Keep the summary concise (2–3 sentences) but informative.  
Do not copy the entire FIR text.

----------------------------------------

5. Preserve numbers exactly as written.

6. Do NOT invent information.

----------------------------------------

Return STRICT JSON only.

----------------------------------------

Schema:

{{
  "metadata": {{
    "state": "UP",
    "district": "",
    "police_station": "",
    "fir_number": "",
    "year": "",
    "fir_datetime": "",
    "investigating_officer": ""
  }},
  "incident": {{
    "occurrence_datetime": "",
    "location_description": "",
    "death": true/false/null,
    "injury": true/false/null,
    "death_count": "",
    "injury_count": ""
  }},
  "legal": {{
    "acts": [],
    "sections": []
  }},
  "vehicles": [
    {{
      "role": "accused/victim",
      "vehicle_type": "",
      "vehicle_number": "",
      "driver_name": "",
      "driver_address": ""
    }}
  ],
  "people": [],
  "insurance": {{
    "company": "",
    "validity": ""
  }},
  "narrative_summary": ""
}}

----------------------------------------

FIR TEXT:

\"\"\"
{text}
\"\"\"
"""