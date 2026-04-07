"""
Event model for the app.

For now, this uses static example events, but in production you would:
- Build events from NOAA NWPS/NWM signals.
- Enrich with FEMA NFHL and EO flood extents.
- Attach exposure metrics (population, roads, critical).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


_EXAMPLE_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "nc-neuse",
        "name": "Neuse Basin flood surge",
        "state": "North Carolina",
        "counties": ["Craven", "Jones", "Pamlico"],
        "hazard": "Riverine",
        "severity": "Major",
        "people": 58400,
        "roads": 146,
        "critical": 11,
    },
    {
        "id": "ca-sacramento",
        "name": "Sacramento Valley overflow",
        "state": "California",
        "counties": ["Sutter", "Yolo", "Sacramento"],
        "hazard": "Riverine",
        "severity": "Moderate",
        "people": 72100,
        "roads": 285,
        "critical": 18,
    },
    {
        "id": "la-plaquemines",
        "name": "Lower Plaquemines coastal flooding",
        "state": "Louisiana",
        "counties": ["Plaquemines"],
        "hazard": "Coastal",
        "severity": "Minor",
        "people": 37700,
        "roads": 181,
        "critical": 20,
    },
]


def list_events(hazard: str = "All", severity: str = "All") -> List[Dict[str, Any]]:
    hazard_norm = hazard.lower()
    severity_norm = severity.lower()
    out: List[Dict[str, Any]] = []
    for ev in _EXAMPLE_EVENTS:
        if hazard_norm != "all" and ev["hazard"].lower() != hazard_norm:
            continue
        if severity_norm != "all" and ev["severity"].lower() != severity_norm:
            continue
        out.append(ev)
    return out


def events_to_geojson(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    # Placeholder: in production, attach real geometries from PostGIS/EO.
    features: List[Dict[str, Any]] = []
    for ev in events:
        # Dummy point in continental US; replace with real centroids.
        coords = [-96.0, 37.8]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "id": ev["id"],
                    "name": ev["name"],
                    "severity": ev["severity"],
                    "hazard": ev["hazard"],
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": coords,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}
