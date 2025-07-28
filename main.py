import streamlit as st
import requests

# Streamlit App UI
st.title("🌧️ Climate Hazard Risk Calculator")
st.markdown("Enter location details to assess rainfall-related risk.")

lat = st.number_input("Latitude", format="%.6f")
lon = st.number_input("Longitude", format="%.6f")
sector = st.selectbox("Select Sector", ["Chemical", "Engineering", "Food", "Pharmaceutical", "Textile", "Other"])

if st.button("Calculate Risk"):
    api_url = "https://climate-risk-backend.onrender.com/risk"  # ✅ Live backend
    payload = {
        "lat": lat,
        "lon": lon,
        "sector": sector
    }

    with st.spinner("Calculating..."):
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Risk assessment complete!")

                st.subheader("📊 Results")
                st.markdown(f"- **ER100 Probability**: `{data['ER100_Probability']}`")
                st.markdown(f"- **ER150 Probability**: `{data['ER150_Probability']}`")
                st.markdown(f"- **RP100 Value**: `{data['RP100_Value_mm']} mm`")
                st.markdown(f"- **Drought Probabilities**:")
                for key, val in data["Drought_Probabilities"].items():
                    st.markdown(f"  - `{key}`: `{val}`")
                st.markdown(f"### 🚦 Final Risk Category: **{data['Final_Risk_Category']}**")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Exception: {str(e)}")
