"""
NOAA National Water Prediction Service (NWPS) / National Water Model helpers.

This is a thin wrapper around the NWPS API endpoints
that you can expand as needed.
"""

from __future__ import annotations

from typing import Any, Dict

import httpx

BASE_URL = "https://api.water.noaa.gov/nwps/v1"  # See NOAA NWPS API docs.


def _client(timeout: float = 10.0) -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=timeout)


def get_health() -> Dict[str, Any]:
    with _client() as client:
        r = client.get("/health")
        r.raise_for_status()
        return r.json()


def get_gauge_forecast(station_id: str) -> Dict[str, Any]:
    """
    Placeholder for a gauge forecast call.

    See: https://api.water.noaa.gov/nwps/v1/docs/
    """
    endpoint = f"/stations/{station_id}/timeseries"
    with _client() as client:
        r = client.get(endpoint)
        r.raise_for_status()
        return r.json()


def get_reach_forecast(reach_id: str) -> Dict[str, Any]:
    """
    Placeholder for a reach-based National Water Model forecast query.
    """
    endpoint = f"/reaches/{reach_id}/forecast"
    with _client() as client:
        r = client.get(endpoint)
        r.raise_for_status()
        return r.json()
