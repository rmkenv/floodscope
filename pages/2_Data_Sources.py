import streamlit as st

st.title("Data sources")

st.markdown(
    """
Suggested production inputs:

- **NOAA National Water Prediction Service / National Water Model**
  - River flow, stage, and flood forecasting signals.
- **NOAA CO-OPS (Tides & Currents)**
  - Coastal water levels, surge, and high-tide flooding metrics.
- **FEMA National Flood Hazard Layer (NFHL)**
  - Regulatory and hazard-zone context around flood risk.
- **Earth observation (EO)**
  - SAR flood detections and optical change/damage mapping.
- **Exposure layers**
  - Roads, parcels, critical facilities, power infrastructure, and population.
- **Terrain and hydrography**
  - DEM, hydrography, and derived inundation surfaces.
"""
)
