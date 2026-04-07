# FloodScope US 

Streamlit repo for a US flood intelligence platform.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Layout

- `app.py` – main entrypoint, embeds the prototype HTML (if present).
- `pages/` – Streamlit multipage views (Map, Overview, Data, Architecture, Deployment).
- `src/services/` – NOAA, FEMA, and event/exposure service modules.
- `src/components/` – Reusable UI components (e.g., sidebar status).
- `.streamlit/` – theme and config.

Next steps:
- Add real NOAA, FEMA, and EO ingestion logic in `src/services/`.
- Replace the map placeholder with a MapLibre, deck.gl, or other component.
