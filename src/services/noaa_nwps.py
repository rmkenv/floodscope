# src/services/noaa_nwps.py
from __future__ import annotations
from typing import Any, Dict, List
import httpx

BASE_URL = "https://api.water.noaa.gov/nwps/v1"  # NWPS base

def _client(timeout: float = 10.0) -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=timeout)

def list_gauges(limit: int = 200) -> List[Dict[str, Any]]:
    """List gauges with basic metadata (id, name, coords, etc.)."""
    with _client() as client:
        r = client.get("/gauges", params={"limit": limit})
        r.raise_for_status()
        data = r.json()
    # Adjust to match actual NWPS response schema
    return data.get("gauges", data)
