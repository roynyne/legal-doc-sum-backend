import streamlit as st
import requests
import tempfile

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Legal Case Summarizer", layout="wide")
st.title("⚖️ Legal Case Summarizer")

uploaded_file = st.file_uploader("Upload a legal case XML file", type="xml")

summary = None

if uploaded_file:
    st.success("File uploaded. You can now preprocess, summarize, or download.")

    # === Preprocess ===
    with st.expander("📄 Preprocess Info"):
        if st.button("🔍 View Case Info"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                files = {"file": f}
                res = requests.post(f"{BACKEND_URL}/preprocess/upload", files=files)

            if res.ok:
                case = res.json()
                st.subheader(case["case_name"])
                st.markdown("#### 📌 Catchphrases:")
                st.write(case["catchphrases"])
                st.markdown("#### 📝 Sample Sentences:")
                st.write(case["sentences"][:5])
            else:
                st.error("Preprocessing failed.")

    # === Structured Summary ===
    with st.expander("🧠 Structured Summary"):
        if st.button("Generate Summary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                files = {"file": f}
                res = requests.post(f"{BACKEND_URL}/summarize/structured", files=files)

            if res.ok:
                summary = res.json()
                st.subheader(summary["case_name"])
                for sec, txt in summary["structured_summary"].items():
                    st.markdown(f"### {sec.capitalize()}")
                    st.markdown(txt)
            else:
                st.error("Summary failed.")

    # === Evaluation (not nested) ===
    if summary and "evaluation" in summary:
        with st.expander("📊 Evaluation Metrics"):
            for key, val in summary["evaluation"].items():
                st.markdown(f"- **{key.replace('_', ' ').title()}**: {val}")

    # === Download Section ===
    with st.expander("📥 Download Case Brief"):
        file_format = st.selectbox("Choose format", ["pdf", "docx", "md"])
        if st.button("Download Brief"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                files = {"file": f}
                res = requests.post(f"{BACKEND_URL}/download/brief", params={"format": file_format}, files=files)

            if res.ok:
                st.download_button(
                    label=f"Download {file_format.upper()}",
                    data=res.content,
                    file_name=f"case_brief.{file_format}",
                    mime="application/octet-stream"
                )
            else:
                st.error("Download failed.")
