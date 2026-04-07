# src/services/events.py (continuing)

COASTAL_STATIONS = [
    {
        "id": "8638863",
        "name": "Sewells Point, VA",
        "state": "Virginia",
        "lat": 36.95,
        "lon": -76.33,
        "minor_threshold_m": 0.5,
        "moderate_threshold_m": 1.0,
    },
    # add more CO-OPS stations as needed
]

def _coastal_events_from_coops() -> List[Dict[str, Any]]:
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
