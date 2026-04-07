"""
FEMA National Flood Hazard Layer (NFHL) helper.

This module provides helpers for querying the NFHL map service.
"""

from __future__ import annotations

from typing import Any, Dict

import httpx

# FEMA NFHL MapServer REST endpoint
NFHL_URL = "https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/0"


def query_nfhl_by_bbox(bbox: str, out_fields: str = "*") -> Dict[str, Any]:
    """
    Query NFHL features intersecting a bounding box.

    bbox format: minx,miny,maxx,maxy in WGS84.
    """
    params = {
        "f": "json",
        "geometry": bbox,
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": out_fields,
        "returnGeometry": True,
    }
    with httpx.Client(timeout=10.0) as client:
        r = client.get(f"{NFHL_URL}/query", params=params)
        r.raise_for_status()
        return r.json()
