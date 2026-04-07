# src/services/events.py
from __future__ import annotations
from typing import Any, Dict, List

from . import noaa_nwps, noaa_coops

def _severity_from_category(category: str) -> str:
    cat = (category or "").lower()
    if cat in {"major"}:
        return "Major"
    if cat in {"moderate"}:
        return "Moderate"
    if cat in {"minor"}:
        return "Minor"
    return "None"

def _river_events_from_nwps() -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    try:
        gauges = noaa_nwps.list_gauges(limit=500)
    except Exception:
        return events

    for g in gauges:
        # Align these keys with actual NWPS schema (example placeholders)
        lat = g.get("latitude")
        lon = g.get("longitude")
        if lat is None or lon is None:
            continue

        name = g.get("name", g.get("id", "Gauge"))
        state = g.get("state", "Unknown")
        category = g.get("flood_category")  # e.g. "minor", "moderate", "major"
        severity = _severity_from_category(category)

        # Only keep gauges at or above minor flood
        if severity == "None":
            continue

        events.append(
            {
                "id": f"gauge-{g.get('id')}",
                "name": name,
                "state": state,
                "counties": [],
                "hazard": "Riverine",
                "severity": severity,
                "people": 0,   # compute later
                "roads": 0,    # compute later
                "critical": 0, # compute later
                "lat": lat,
                "lon": lon,
            }
        )
    return events
