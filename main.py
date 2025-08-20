import streamlit as st
import requests
import time

# Page setup
st.set_page_config(page_title="🌧️ Climate Risk Calculator", page_icon="🌍", layout="wide")

st.title("🌧️ Climate Hazard Risk Calculator")
st.markdown("Enter location details to assess rainfall-related climate risk.")

# Inputs
col1, col2 = st.columns(2)
with col1:
    lat = st.number_input("Latitude", value=19.0, format="%.4f")
    lon = st.number_input("Longitude", value=73.0, format="%.4f")
with col2:
    sector = st.text_input("Sector", value="Chemical")

# Action button
if st.button("🔍 Calculate Risk"):
    API_URL = "https://climate-risk-backend.onrender.com/risk"
    payload = {"latitude": lat, "longitude": lon, "sector": sector}

    with st.spinner("⏳ Processing 100+ years of rainfall data... Please wait"):
        try:
            response = requests.post(API_URL, json=payload)
            time.sleep(1)  # small delay for spinner effect

            if response.status_code == 200:
                result = response.json()
                st.success("✅ Risk calculation completed")

                # --- Summary Metrics ---
                st.subheader("📊 Risk Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Category", result["risk_result"]["Category"])
                col2.metric("Final Score", round(result["risk_result"]["Final_Score"], 3))
                col3.metric("Composite Hazard", round(result["hazards"]["Composite_Hazard"], 3))

                # --- Tabs for details ---
                tab1, tab2, tab3 = st.tabs(["🌧️ Hazards", "📈 Risk Breakdown", "🛠️ Raw JSON"])

                with tab1:
                    st.markdown("### Hazard Indicators")
                    hazards = result["hazards"]
                    df = {k: [v] for k, v in hazards.items()}
                    st.dataframe(df)

                with tab2:
                    st.markdown("### Weighted Risk Calculation")
                    st.json(result["risk_result"])

                with tab3:
                    st.markdown("### Full API Response")
                    st.json(result)

            else:
                st.error(f"API request failed: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
