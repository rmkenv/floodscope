# pages/0_Map.py
import streamlit as st
import folium
from streamlit_folium import st_folium

from src.services import events

st.set_page_config(page_title="FloodScope US – Map", layout="wide")
st.title("FloodScope US – Map (Folium)")

col_filters, col_map = st.columns([1, 3])

with col_filters:
    st.subheader("Filters")

    hazard = st.selectbox("Hazard type", ["All", "Riverine", "Coastal"])
    severity = st.selectbox("Severity", ["All", "Major", "Moderate", "Minor"])

    evs = events.list_events(hazard=hazard, severity=severity)
    st.write(f"{len(evs)} events")

    selected = st.selectbox(
        "Focus event",
        evs,
        format_func=lambda e: e["name"],
    ) if evs else None

# Dummy centroids for now – replace with real ones later
centroid_lookup = {
    "nc-neuse": (35.10, -77.03),
    "ca-sacramento": (38.65, -121.65),
    "la-plaquemines": (29.37, -89.76),
}

if evs:
    lats = []
    lons = []
    for ev in evs:
        lat, lon = centroid_lookup.get(ev["id"], (37.8, -96.0))
        lats.append(lat)
        lons.append(lon)
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
else:
    center_lat, center_lon = 37.8, -96.0

with col_map:
    st.subheader("Map")

    # Create Leaflet/Folium map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Add markers for each event
    for ev in evs:
        lat, lon = centroid_lookup.get(ev["id"], (37.8, -96.0))
        popup = (
            f"<b>{ev['name']}</b><br>"
            f"{ev['state']}<br>"
            f"{ev['hazard']} – {ev['severity']}<br>"
            f"People: {ev['people']:,}"
        )
        color = {
            "Major": "red",
            "Moderate": "orange",
            "Minor": "blue",
        }.get(ev["severity"], "green")

        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=popup,
        ).add_to(m)

    # Render map in Streamlit
    st_folium(m, width="100%", height=600)


