import streamlit as st
import requests
import time

# Page config
st.set_page_config(
    page_title="Climate Risk Calculator",
    page_icon="🌧️",
    layout="wide"
)

# Title and instructions
st.title("🌧️ Climate Hazard Risk Calculator")
st.markdown("Enter location details to assess rainfall-related risk for your industrial sector.")

# Sidebar with instructions
with st.sidebar:
    st.header("📖 Instructions")
    st.markdown("""
    1. Enter latitude and longitude coordinates
    2. Select your industrial sector
    3. Click 'Calculate Risk' to get assessment
    
    **Note:** Processing may take 30-60 seconds as we analyze 100+ years of rainfall data.
    """)

# Main input area
col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude", 
        min_value=-90.0, 
        max_value=90.0, 
        value=28.6139,  # Delhi as example
        format="%.6f",
        help="Enter latitude in decimal degrees"
    )
    
with col2:
    longitude = st.number_input(
        "Longitude", 
        min_value=-180.0, 
        max_value=180.0, 
        value=77.2090,  # Delhi as example
        format="%.6f",
        help="Enter longitude in decimal degrees"
    )

sector = st.selectbox(
    "Select Industrial Sector", 
    ["Chemical", "Engineering", "Food Processing", "Pharmaceutical", "Textile", "Other"],
    help="Different sectors have different risk sensitivities"
)

# Calculate button
if st.button("🔍 Calculate Risk", type="primary"):
    # Replace with YOUR actual backend URL after deployment
    api_url = "https://rainfall-risk-api.onrender.com/risk" # UPDATE THIS!
    
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "sector": sector
    }

    # Show loading state
    with st.spinner("🌍 Analyzing climate data... This may take up to 60 seconds"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Simulate progress updates
            for i in range(10):
                progress_bar.progress((i + 1) / 10)
                status_text.text(f"Processing rainfall data... {(i+1)*10}%")
                time.sleep(0.5)
            
            response = requests.post(api_url, json=payload, timeout=120)
            progress_bar.progress(100)

            if response.status_code == 200:
                data = response.json()
                status_text.text("✅ Analysis complete!")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success("✅ Risk assessment completed successfully!")

                # Main results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🌊 Extreme Rainfall Risk (>100mm)", 
                        f"{data['ER100']:.3f}",
                        help="Probability of daily rainfall exceeding 100mm"
                    )
                
                with col2:
                    st.metric(
                        "⚡ Severe Rainfall Risk (>150mm)", 
                        f"{data['ER150']:.3f}",
                        help="Probability of daily rainfall exceeding 150mm"
                    )
                
                with col3:
                    st.metric(
                        "📈 100-Year Return Period", 
                        f"{data['RP100']:.1f} mm",
                        help="Expected maximum daily rainfall in 100 years"
                    )

                # Risk category
                risk_color = {
                    "Low": "🟢",
                    "Medium": "🟡", 
                    "High": "🔴"
                }.get(data['risk_category'], "⚪")
                
                st.markdown(f"### {risk_color} Overall Risk Level: **{data['risk_category']}**")
                st.markdown(f"**Risk Score:** {data['final_score']:.3f}")

                # Drought probabilities
                st.subheader("🌵 Drought Risk Analysis")
                drought_cols = st.columns(4)
                
                drought_labels = {
                    "P_D1": "Moderate Drought",
                    "P_D2": "Severe Drought", 
                    "P_D3": "Extreme Drought",
                    "P_D4": "Exceptional Drought"
                }
                
                for i, (key, label) in enumerate(drought_labels.items()):
                    with drought_cols[i]:
                        st.metric(label, f"{data[key]:.3f}")

                # Additional info
                with st.expander("📊 Understanding Your Results"):
                    st.markdown("""
                    **Risk Categories:**
                    - 🟢 **Low Risk (0.0-0.5)**: Minimal climate impact expected
                    - 🟡 **Medium Risk (0.5-0.75)**: Moderate climate adaptation needed  
                    - 🔴 **High Risk (0.75-1.0)**: Significant climate resilience required
                    
                    **Indicators Explained:**
                    - **ER100/ER150**: Probability of extreme daily rainfall events
                    - **RP100**: Maximum expected rainfall in a century
                    - **Drought Probabilities**: Likelihood of different drought severities
                    """)
                    
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The analysis takes time due to large datasets. Please try again.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        finally:
            # Clean up progress indicators
            progress_bar.empty()
            status_text.empty()

# Footer
st.markdown("---")
st.markdown("*Climate data sourced from historical rainfall records (1901-2023)*")