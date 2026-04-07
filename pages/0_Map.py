# pages/0_Map.py
import streamlit as st
import pandas as pd
import pydeck as pdk

from src.services import events

st.set_page_config(page_title="FloodScope US – Map", layout="wide")
st.title("FloodScope US – Map")

hazard = st.selectbox("Hazard type", ["All", "Riverine", "Coastal"])
severity = st.selectbox("Severity", ["All", "Major", "Moderate", "Minor"])

evs = events.list_events(hazard=hazard, severity=severity)

# For now, use dummy centroids; later use real geometry centroids.
data = pd.DataFrame(
    [
        {
            "lon": -96.0,  # replace with real lon
            "lat": 37.8,   # replace with real lat
            "name": ev["name"],
            "severity": ev["severity"],
            "hazard": ev["hazard"],
        }
        for ev in evs
    ]
)

view_state = pdk.ViewState(
    latitude=37.8,
    longitude=-96.0,
    zoom=3.5,
    pitch=30,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position="[lon, lat]",
    get_color="[200, 30, 0, 160]",
    get_radius=20000,
    pickable=True,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}\n{hazard} – {severity}"},
        map_style=None,  # or a Mapbox/Carto style if you add a key
    )
)
