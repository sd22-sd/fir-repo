import streamlit as st
import tempfile
import os

from main import run_pipeline
from src.utils.excel_exporter import json_to_excel


st.set_page_config(
    page_title="FIR Document Intelligence System",
    layout="wide"
)

# Create padding layout
left_pad, center, right_pad = st.columns([1, 2, 1])

with center:

    st.title("FIR Document Intelligence System")

    uploaded_file = st.file_uploader(
        "Upload FIR PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Submit", use_container_width=True):

            with st.spinner("Running OCR..."):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    pdf_path = tmp.name

                try:

                    result = run_pipeline(pdf_path)

                    st.success("Processing completed")

                    metadata = result.get("metadata", {})
                    incident = result.get("incident", {})
                    vehicles = result.get("vehicles", [])

                    st.subheader("Extracted FIR Details")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**FIR Number:** {metadata.get('fir_number','')}")
                        st.markdown(f"**Police Station:** {metadata.get('police_station','')}")
                        st.markdown(f"**District:** {metadata.get('district','')}")
                        st.markdown(f"**FIR DateTime:** {metadata.get('fir_datetime','')}")

                    with col2:
                        st.markdown(f"**Occurrence DateTime:** {incident.get('occurrence_datetime','')}")
                        st.markdown(f"**Location:** {incident.get('location_description','')}")
                        st.markdown(f"**Death:** {incident.get('death','')}")
                        st.markdown(f"**Injury Count:** {incident.get('injury_count','')}")

                    st.subheader("Vehicles")

                    for v in vehicles:

                        st.markdown(
                            f"""
                            **Role:** {v.get("role","")}  
                            **Vehicle Type:** {v.get("vehicle_type","")}  
                            **Vehicle Number:** {v.get("vehicle_number","")}  
                            **Driver Name:** {v.get("driver_name","")}
                            """
                        )

                    st.subheader("Summary")

                    st.info(result.get("narrative_summary", ""))

                    # Excel export
                    excel_path = "output/fir_extracted_data.xlsx"
                    json_to_excel(result, excel_path)

                    with open(excel_path, "rb") as f:

                        st.download_button(
                            label="Download Excel Report",
                            data=f,
                            file_name="fir_extracted_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

                finally:
                    os.remove(pdf_path)