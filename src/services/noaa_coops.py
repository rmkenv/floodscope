"""
NOAA CO-OPS (Tides & Currents) helpers.

Wraps core CO-OPS water level endpoints for coastal flooding context.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import httpx

BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"


def get_water_level(
    station_id: str,
    start: datetime,
    end: datetime,
    datum: str = "MSL",
) -> Dict[str, Any]:
    """
    Fetch observed water levels for a CO-OPS station.

    See CO-OPS API docs for full parameter options.
    """
    params = {
        "product": "water_level",
        "application": "floodscope-us",
        "station": station_id,
        "begin_date": start.strftime("%Y%m%d"),
        "end_date": end.strftime("%Y%m%d"),
        "datum": datum,
        "time_zone": "gmt",
        "units": "metric",
        "format": "json",
    }
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        r = client.get("", params=params)
        r.raise_for_status()
        return r.json()
