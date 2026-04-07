"""
Event model for the app.

Version: live NOAA-backed events.

- Riverine events come from NOAA NWPS / National Water Model gauge data.
- Coastal events come from NOAA CO-OPS water level data.
- Exposure metrics (people, roads, critical) are placeholders for now.
"""

from __future__ import annotations

from typing import Any, Dict, List

from . import noaa_nwps, noaa_coops


# -----------------------------
# Helpers
# -----------------------------


def _severity_from_category(category: str | None) -> str:
    """
    Map a flood category string to a severity label.
    """
    if not category:
        return "None"
    cat = category.lower()
    if cat == "major":
        return "Major"
    if cat == "moderate":
        return "Moderate"
    if cat == "minor":
        return "Minor"
    return "None"


# -----------------------------
# Riverine events (NWPS)
# -----------------------------


def _river_events_from_nwps(limit: int = 500) -> List[Dict[str, Any]]:
    """
    Build riverine flood events from NWPS gauges.

    NOTE: This assumes the NWPS /gauges endpoint returns, for each gauge:
      - id
      - name
      - latitude
      - longitude
      - state
      - flood_category  (e.g. "none", "minor", "moderate", "major")

    You may need to adjust key names and/or endpoints once you pin down
    the exact NWPS response format you are using.
    """
    events: List[Dict[str, Any]] = []

    try:
        gauges = noaa_nwps.list_gauges(limit=limit)
    except Exception:
        # In production you would log this.
        return events

    for g in gauges:
        lat = g.get("latitude")
        lon = g.get("longitude")
        if lat is None or lon is None:
            continue

        name = g.get("name", g.get("id", "Gauge"))
        state = g.get("state", "Unknown")

        # Example: NWPS provides a flood category field
        category = g.get("flood_category")  # string like "minor", "moderate", "major"
        severity = _severity_from_category(category)

        # Only keep gauges at or above "minor"
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
                "people": 0,   # TODO: compute from exposure analysis
                "roads": 0,    # TODO: compute from exposure analysis
                "critical": 0, # TODO: compute from exposure analysis
                "lat": lat,
                "lon": lon,
            }
        )

    return events


# -----------------------------
# Coastal events (CO-OPS)
# -----------------------------


# Configure a few example coastal stations; expand as needed.
COASTAL_STATIONS: List[Dict[str, Any]] = [
    {
        "id": "8638863",
        "name": "Sewells Point, VA",
        "state": "Virginia",
        "lat": 36.95,
        "lon": -76.33,
        "minor_threshold_m": 0.5,   # example thresholds; tune per site
        "moderate_threshold_m": 1.0,
    },
    # Add more CO-OPS stations here with their own thresholds and coords.
]


def _coastal_events_from_coops() -> List[Dict[str, Any]]:
    """
    Build coastal flood events from CO-OPS water level data.

    For each configured station, we fetch the latest water level and
    flag it as an event if it exceeds the defined thresholds.
    """
    events: List[Dict[str, Any]] = []

    for s in COASTAL_STATIONS:
        try:
            latest = noaa_coops.get_latest_water_level(s["id"])
        except Exception:
            continue

        level = float(latest.get("v", 0.0)) if latest else 0.0

        sev = "None"
        if level >= s["moderate_threshold_m"]:
            sev = "Major"
        elif level >= s["minor_threshold_m"]:
            sev = "Moderate"
        else:
            continue  # below minor threshold

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
                "lat": s["lat"],
                "lon": s["lon"],
            }
        )

    return events


# -----------------------------
# Public API
# -----------------------------


def list_events(hazard: str = "All", severity: str = "All") -> List[Dict[str, Any]]:
    """
    Return a list of current flood events built from live NOAA sources.

    Each event has:
      - id, name, state, counties
      - hazard ("Riverine" or "Coastal")
      - severity ("Minor" / "Moderate" / "Major")
      - people, roads, critical (currently 0; compute later)
      - lat, lon (for map rendering)
    """
    river = _river_events_from_nwps()
    coastal = _coastal_events_from_coops()
    events = river + coastal

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
