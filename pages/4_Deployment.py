import streamlit as st

st.title("Deployment")

st.markdown("### Local development")

st.code(
    """\
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
""",
    language="bash",
)

st.markdown("### Docker")

st.code(
    """\
docker build -t floodscope-us .
docker run --rm -p 8501:8501 floodscope-us
""",
    language="bash",
)

st.markdown("### Docker Compose")

st.code(
    """\
docker-compose up --build
""",
    language="bash",
)

st.markdown("### Streamlit Community Cloud")

st.markdown(
    """
- Push this repo to GitHub.
- Set the app entrypoint to `app.py`.
- Configure any secrets via the Streamlit Cloud UI (do not commit real secrets).
"""
)
