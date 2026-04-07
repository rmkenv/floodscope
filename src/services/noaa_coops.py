from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Dict
import httpx

BASE_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

def get_latest_water_level(station: str) -> Dict[str, Any]:
    end = datetime.utcnow()
    start = end - timedelta(days=1)

    params = {
        "product": "water_level",
        "application": "floodscope-us",
        "station": station,
        "begin_date": start.strftime("%Y%m%d"),
        "end_date": end.strftime("%Y%m%d"),
        "datum": "MSL",
        "time_zone": "gmt",
        "units": "metric",
        "format": "json",
    }

    with httpx.Client(timeout=10.0) as client:
        r = client.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    data_points = data.get("data", [])
    return data_points[-1] if data_points else {}
