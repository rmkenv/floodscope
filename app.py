from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="FloodScope US",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("FloodScope US")
st.caption("US flood intelligence prototype – Version 2")

st.markdown(
    """
This app is the operations console for a US flood intelligence platform.

- The **Map** page shows events and a map-focused view.
- Supporting pages describe data sources, architecture, and deployment.
"""
)

html_path = Path(__file__).parent / "assets" / "floodscope-us.html"
if html_path.exists():
    html = html_path.read_text(encoding="utf-8")
    st.components.v1.html(html, height=900, scrolling=False)
else:
    st.info("Place `floodscope-us.html` in the `assets/` folder to render the prototype map shell.")
