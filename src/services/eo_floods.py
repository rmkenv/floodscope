# src/services/eo_floods.py
from typing import List, Dict, Any

def list_flood_scenes(aoi_wkt: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Query your STAC or catalog for flood scenes intersecting the AOI.
    """
    ...

def get_flood_polygon(event_id: str) -> Dict[str, Any]:
    """
    Return a GeoJSON polygon/multipolygon for an event.
    """
    ...
