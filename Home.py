# This is the main file where the application will run out of
import streamlit as st

from utils.utils import check_config_file_state, zip_files

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

if "configs" not in st.session_state:
    st.session_state["configs"] = {}

# create the sidebars
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

# start of application
st.header("RepoConfig")
st.write("_Your one-stop shop for creating RepoSense configurations and scaffolding to get your RepoSense "
         "app up and running in no time!_")
st.divider()

st.info("Select any Configurator on the sidebar to start creating RepoSense configurations and scaffoldings!")
