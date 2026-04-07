# src/services/events.py
from __future__ import annotations
from typing import Any, Dict, List

from . import noaa_nwps, noaa_coops

# Example: configure a few key river and coastal sites
RIVER_GAUGES = [
    {"id": "01200500", "name": "Connecticut River at Dalton", "state": "New Hampshire"},
    # add more NWPS gauge IDs you care about
]

COASTAL_STATIONS = [
    {"id": "8638863", "name": "Sewells Point, VA", "state": "Virginia"},
    # add more CO-OPS station IDs
]

def list_events(hazard: str = "All", severity: str = "All") -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []

    # 1) Riverine: build events from NWPS gauges
    try:
        gauges = noaa_nwps.list_gauges(limit=200)
    except Exception:
        gauges = []

    for g in gauges:
        # Adjust keys to actual NWPS gauge schema
        lat = g.get("latitude", 37.8)
        lon = g.get("longitude", -96.0)
        name = g.get("name", g.get("id", "Gauge"))
        state = g.get("state", "Unknown")
        stage = g.get("stage", 0)  # you may have to compute from timeseries

        sev = "Minor"
        if stage >= 2:  # placeholder thresholds
            sev = "Moderate"
        if stage >= 3:
            sev = "Major"

        events.append(
            {
                "id": f"gauge-{g.get('id')}",
                "name": name,
                "state": state,
                "counties": [],
                "hazard": "Riverine",
                "severity": sev,
                "people": 0,
                "roads": 0,
                "critical": 0,
                "lat": lat,
                "lon": lon,
            }
        )

    # 2) Coastal: build events from selected CO-OPS stations
    for s in COASTAL_STATIONS:
        try:
            latest = noaa_coops.get_latest_water_level(s["id"])
        except Exception:
            latest = {}

        level = float(latest.get("v", 0.0)) if latest else 0.0
        sev = "Minor"
        if level >= 0.5:
            sev = "Moderate"
        if level >= 1.0:
            sev = "Major"

        # You will need station metadata (lat/lon) from CO-OPS or a local table
        # For now, placeholders:
        lat, lon = 36.95, -76.33  # Sewells Point approx

        events.append(
            {
                "id": f"coops-{s['id']}",
                "name": s["name"],
                "state": s["state"],
                "counties": [],
                "hazard": "Coastal",
                "severity": sev,
                "people": 0,
                "roads": 0,
                "critical": 0,
                "lat": lat,
                "lon": lon,
            }
        )

    # Filter by hazard/severity
    hazard_norm = hazard.lower()
    severity_norm = severity.lower()
    out: List[Dict[str, Any]] = []
    for ev in events:
        if hazard_norm != "all" and ev["hazard"].lower() != hazard_norm:
            continue
        if severity_norm != "all" and ev["severity"].lower() != severity_norm:
            continue
        out.append(ev)
    return out
