import streamlit as st

st.title("Overview")

st.markdown(
    """
    ### What this app is

    FloodScope US is a NOAA-first concept for a national flood intelligence platform:
    - Riverine and coastal flood signals.
    - Mapped inundation and impact layers.
    - An operations-focused console for analysts and responders.

    ### Version 2 goals

    - Move data ingestion and integration into `src/services/`.
    - Use Streamlit mainly for operations, reporting, and internal workflows.
    - Prepare the repo for Docker, compose, and CI.
    """
)
