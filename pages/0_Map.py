import streamlit as st

from src.services import events

st.set_page_config(page_title="FloodScope US – Map", layout="wide")

st.title("FloodScope US – Map")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Filters")
    hazard = st.selectbox("Hazard type", ["All", "Riverine", "Coastal"])
    severity = st.selectbox("Severity", ["All", "Major", "Moderate", "Minor"])

    active_events = events.list_events(hazard=hazard, severity=severity)
    st.write(f"{len(active_events)} events")

    selected = st.selectbox(
        "Focus event",
        active_events,
        format_func=lambda e: e["name"],
    ) if active_events else None

with col2:
    st.subheader("Map (placeholder)")
    st.markdown(
        """
        This is a Python-native map placeholder.

        In production you would:
        - Use a MapLibre, deck.gl, or folium-based Streamlit component.
        - Render flood extents, gauges, roads, and exposure metrics.
        - Hook into the `events` service for geometries and metrics.
        """
    )

    if selected:
        st.json(selected)

st.caption("Next step: replace this placeholder with a real map component.")
