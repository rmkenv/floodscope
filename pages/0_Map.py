# pages/0_Map.py
import streamlit as st
import pandas as pd
import pydeck as pdk

from src.services import events

st.set_page_config(page_title="FloodScope US – Map", layout="wide")
st.title("FloodScope US – Map")

# Sidebar-style controls
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

with col_map:
    st.subheader("Map")

    if not evs:
        st.info("No events for the current filters.")
    else:
        # Simple dummy centroids per event (replace with real coords later)
        centroid_lookup = {
            "nc-neuse": (-77.03, 35.10),
            "ca-sacramento": (-121.65, 38.65),
            "la-plaquemines": (-89.76, 29.37),
        }

        df = pd.DataFrame(
            [
                {
                    "lon": centroid_lookup.get(ev["id"], (-96.0, 37.8))[0],
                    "lat": centroid_lookup.get(ev["id"], (-96.0, 37.8))[1],
                    "name": ev["name"],
                    "state": ev["state"],
                    "severity": ev["severity"],
                    "hazard": ev["hazard"],
                    "people": ev["people"],
                }
                for ev in evs
            ]
        )

        # View centered on all points
        view_state = pdk.ViewState(
            latitude=df["lat"].mean(),
            longitude=df["lon"].mean(),
            zoom=5 if len(df) == 1 else 3.5,
            pitch=30,
        )

        # Color by severity
        def severity_color(sev: str) -> list[int]:
            sev = sev.lower()
            if sev == "major":
                return [193, 76, 88, 200]      # red
            if sev == "moderate":
                return [215, 166, 61, 200]     # orange
            return [79, 152, 163, 200]        # teal for minor/other

        df["color"] = df["severity"].apply(severity_color)

        layer = pdk.Layer(
            "ScatterplotLayer",
            df,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius=25000,
            pickable=True,
            radius_min_pixels=5,
            radius_max_pixels=50,
        )

        tooltip = {
            "html": "<b>{name}</b><br/>{hazard} – {severity}<br/>{state}<br/>People: {people}",
            "style": {"backgroundColor": "rgba(23,22,20,0.9)", "color": "white"},
        }

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/dark-v10",  # or None for no basemap
        )

        st.pydeck_chart(deck)

st.caption("This is a working map using pydeck ScatterplotLayer; swap centroids for real geometries later.")
