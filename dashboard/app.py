# 📁 app.py (Streamlit UI)
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Toxicity Analyzer", page_icon="📊", layout="centered")
st.title("📊 Toxicity Analyzer using Perspective API")

st.sidebar.header("Choose Analysis Mode")
mode = st.sidebar.radio("Mode:", ("Upload Excel File", "Analyze Single Comment"))

BACKEND_URL = "http://127.0.0.1:8000"

if mode == "Upload Excel File":
    st.markdown("Upload an Excel file with a `text` column to analyze toxicity levels.")
    uploaded_file = st.file_uploader("📁 Upload Excel file", type=["xlsx"])

    if uploaded_file is not None and st.button("Analyze File"):
        with st.spinner("Analyzing... Please wait."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
                response = requests.post(f"{BACKEND_URL}/analyze-excel/", files=files)

                if response.status_code == 200:
                    st.success("✅ Analysis Complete!")
                    st.download_button(
                        label="📥 Download Results ZIP",
                        data=response.content,
                        file_name="toxicity_results.zip",
                        mime="application/zip"
                    )
                else:
                    st.error(f"❌ Error from API: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: {e}")

elif mode == "Analyze Single Comment":
    text_input = st.text_area("📝 Enter a comment to analyze", height=150)

    if st.button("Analyze Comment") and text_input.strip():
        with st.spinner("Analyzing comment..."):
            try:
                response = requests.post(f"{BACKEND_URL}/analyze-text/", json={"text": text_input})
                if response.status_code == 200:
                    scores = response.json()
                    st.success("✅ Analysis Complete")
                    st.subheader("Results")
                    for k, v in scores.items():
                        st.write(f"**{k}:** {v if v is not None else 'N/A'}")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: {e}")
