import streamlit as st

from utils.utils import convert_report_config_json_to_json, check_config_file_state, zip_files

st.set_page_config(
    page_title="report-config.json",
    page_icon="⚙️",
)


# define session states to be used
if "form-submitted-report-json" not in st.session_state:
    st.session_state["form-submitted-report-json"] = False

if "configs" not in st.session_state:
    st.session_state["configs"] = {}

with st.sidebar:
    st.write("## Download Config Files")
    st.download_button(
        on_click=lambda: check_config_file_state(st.session_state["configs"]),
        label="Download Config Files",
        data=zip_files(st.session_state["configs"]),
        mime="application/octet-stream",
        file_name="configs.zip",
        key="config-file-download"
    )

    st.write("## Export as RepoSense Scaffold")
    st.button("Export...")

st.header("RepoConfig")
st.write("_Your one-stop shop for creating RepoSense configurations and scaffolding to get your RepoSense "
         "app up and running in no time!_")
st.divider()

st.subheader("`report-config.json` Configuration Wizard")
st.write("Enter in the following details to create a `report-config.json` config!")

st.write("#### Repo and Branch Configurations")
report_title = st.text_input(
    "Enter in the report title",
    key="report-config-report-title",
    help="Title of the generated report, which is also the title of the deployed dashboard"
)

form_returns = {"title": report_title}

# if st.form_submit_button("Create RepoSense Configuration!"):
if st.button("Create configurations!"):
    is_valid = True

    if not report_title or len(report_title) < 1:
        is_valid = False

    if not is_valid:
        st.error("Check your inputs and ensure that you filled in all mandatory fields for the "
                 "branches!")

    form_returns = {
        "title": report_title
    }

    # set the result of the form validation as the indicator if the form is successfully submitted
    st.session_state["form-submitted-report-json"] = is_valid

if st.session_state["form-submitted-report-json"]:
    st.success("Configurations created successfully!")
    st.write("### Preview")
    st.json(form_returns)
    st.session_state["configs"]["report-config.json"] = convert_report_config_json_to_json(form_returns)

    st.download_button(
        label="Download Configurations",
        key="repo-config-internal-download-button",
        data=st.session_state["configs"]["report-config.json"],
        mime="application/octet-stream",
        file_name='report-config.json'
    )
