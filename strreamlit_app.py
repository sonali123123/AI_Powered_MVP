import requests, streamlit as st

BACKEND = "http://localhost:8000/extract"

st.set_page_config(page_title="📰 News Metadata Extractor", layout="centered")
st.title("📰 News Metadata Extractor")

with st.form("url_form"):
    url = st.text_input("Paste a news-article URL")
    submit = st.form_submit_button("Extract")

if submit:
    with st.spinner("Fetching & analysing…"):
        r = requests.post(BACKEND, json={"url": url})
    if r.ok:
        st.success("Done!")
        st.json(r.json())
    else:
        st.error(f"❌  {r.text}")
