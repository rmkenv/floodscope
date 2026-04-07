import streamlit as st

from src.services import events


def render_sidebar_status() -> None:
    st.sidebar.header("Platform status")
    all_events = events.list_events()
    total_people = sum(ev["people"] for ev in all_events)
    total_roads = sum(ev["roads"] for ev in all_events)
    total_critical = sum(ev["critical"] for ev in all_events)

    st.sidebar.metric("Active events", len(all_events))
    st.sidebar.metric("People at risk", f"{total_people/1000:.1f}k")
    st.sidebar.metric("Road miles", total_roads)
    st.sidebar.metric("Critical sites", total_critical)
