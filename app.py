import streamlit as st
import requests

st.title("Company News Sentiment Analysis & Hindi TTS")

company_name = st.text_input("Enter Company Name:")

if st.button("Analyze"):
    if not company_name:
        st.error("Please enter a company name.")
    else:
        response = requests.post("http://127.0.0.1:5000/analyze", json={"company": company_name})

        if response.status_code == 200:
            try:
                data = response.json()

                # Display full JSON output
                st.json(data)

                # Play Hindi TTS audio if available
                if "Audio" in data and data["Audio"]:
                    st.subheader("Hindi TTS Summary")
                    st.audio(data["Audio"])
                else:
                    st.warning("No valid audio available.")

            except Exception as e:
                st.error(f"Unexpected response format: {e}")
        else:
            st.error("Failed to fetch data from API.")
