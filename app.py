import os
from pathlib import Path
import streamlit as st

from app_runner import run_link_checker

st.set_page_config(page_title="Broken Link Checker", layout="wide")

col1, col2, col3 = st.columns([4, 2, 1])

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("Broken Link Checker")
    st.write("Run the Marian University broken link report.")

with col2:
    st.image(
        "https://www.marian.edu/images/default-source/_logos/marian-university-logo.png?sfvrsn=0&MaxWidth=100&MaxHeight=100&ScaleUp=false&Quality=High&Method=ResizeFitToAreaArguments&Signature=0B8446F612A6F807C9682F238368F952",
        width=200
    )

def check_password():
    correct_password = st.secrets["LINK_CHECKER_PASSWORD"]

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password")

    return False


if not check_password():
    st.stop()

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if st.button("Run Link Check Report"):
    with st.spinner("Running crawler... this can take a few minutes"):
        result = run_link_checker()

    st.session_state.last_result = result
    st.success("Report finished")

result = st.session_state.last_result

if result:
    st.subheader("Latest Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Scanned Pages", result["scanned_pages"])
    col2.metric("Broken Links", result["broken_links"])
    col3.metric("Cascade Logins", result["cascade_logins"])
    col4.metric("Affected Pages", result["affected_pages"])

    st.write(f"Last run: {result['run_timestamp_utc']}")

    st.subheader("Download Reports")

    page_report = Path(result["page_report_path"])
    violations_report = Path(result["violations_report_path"])
    summary_report = Path(result["summary_report_path"])

    if page_report.exists():
        with open(page_report, "rb") as f:
            st.download_button(
                "Download Page Report",
                f,
                file_name=page_report.name,
                mime="text/csv",
            )

    if violations_report.exists():
        with open(violations_report, "rb") as f:
            st.download_button(
                "Download Violations Report",
                f,
                file_name=violations_report.name,
                mime="text/csv",
            )

    if summary_report.exists():
        with open(summary_report, "rb") as f:
            st.download_button(
                "Download Summary Report",
                f,
                file_name=summary_report.name,
                mime="text/csv",
            )

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>Made by Jonas Schaefer | Indianapolis, IN</div>",
    unsafe_allow_html=True
)