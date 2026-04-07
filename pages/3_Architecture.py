import streamlit as st

st.title("Architecture")

st.markdown(
    """
A practical production architecture for FloodScope US:

1. **Ingestion workers**
   - Pull NOAA NWPS/NWM, CO-OPS, FEMA NFHL, and EO scene metadata.
2. **Processing / analytics**
   - Normalize geometries, consolidate events, compute exposure metrics.
3. **Storage**
   - PostGIS for events, gauges, assets, and exposure summaries.
   - Object storage for rasters, COGs, and tiles.
4. **APIs and tiles**
   - Event API (JSON) plus vector/raster tiles for the map.
5. **Streamlit layer**
   - Operations console and reporting views driven by the services API.
"""
)
