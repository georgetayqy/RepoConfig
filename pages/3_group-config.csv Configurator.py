import streamlit as st

from streamlit_tags import st_tags
from utils.utils import convert_group_config_csv_to_csv, check_config_file_state, zip_files

st.set_page_config(
    page_title="group-config.csv",
    page_icon="⚙️",
)


# define session states to be used
if "form-submitted-group-csv" not in st.session_state:
    st.session_state["form-submitted-group-csv"] = False

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

st.subheader("`group-config.csv` Configuration Wizard")
st.write("Select the number of repositories to configure for and how many branches per repository!")
st.warning("Using duplicate branch names will override the previous branch configurations!")

st.write("#### Repo and Branch Configurations")
num_repo = st.number_input(
    "Select the number of repositories to include",
    key="repo-config-num-repo",
    min_value=1,
)

st.divider()
form_returns: dict[str, dict[str, dict]] = {}

for reponumber in range(num_repo):
    base_key = str(reponumber)  # defines the base key for all widgets to avoid key errors

    st.markdown(f"### Repository {reponumber + 1}")
    repo_location = st.text_input(
        "Enter in the Remote Repo URL or Disk Path to the `git` repository",
        key=base_key + "repo_location",
        help=r"e.g. https://github.com/foo/bar.git or C:\Users\user\Desktop\GitHub\foo\bar" 
             "\n\nNote that Disk Path only works if the `git` repository is located in the same "
             "directory as this application!")
    num_groups = st.number_input(
        label=f"Select the number of groups in this repository",
        key=f"repo-config-group-count{reponumber}",
        min_value=1,
        step=1
    )

    # create a new entry in the dict to for updates
    if repo_location and num_groups:
        form_returns[repo_location] = {}

        for group_num in range(num_groups):
            st.markdown(f"### Group {group_num + 1}")
            group_key = repo_location + str(group_num)  # defines the base key for all widgets in this branch

            group_name = st.text_input(
                "Enter the name of the group",
                key=base_key + group_key + "branch_name",
                help="Branch to analyze in the target repository, e.g. `master`")

            if group_name:
                glob_lists = st_tags(
                    label="Enter in the list of file path globs to include for this group "
                          "(Refer to [this](https://docs.oracle.com/javase/tutorial/essential/io/fileOps.html"
                          "#glob) for more info on path glob syntax)",
                    text="e.g. test/**, temp/**...",
                    key=base_key + group_key + "ignore_glob_lists")

                # write to return dict each branch
                form_returns[repo_location][group_name] = curr = {}
                # convert all file formats to lowercase for easier processing later
                curr["glob_lists"] = [gl.strip() for gl in glob_lists]

    if reponumber != num_repo - 1:
        st.divider()

# if st.form_submit_button("Create RepoSense Configuration!"):
if st.button("Create configurations!"):
    is_valid = True
    if len(form_returns) < 1:
        is_valid = False
        st.error("Check your form and ensure that you fill in all mandatory fields for the repositories!")

    for repo, groups in form_returns.items():
        if len(groups) < 1:
            is_valid = False

    if not is_valid:
        st.error("Check your inputs and ensure that you filled in all mandatory fields for the "
                 "branches!")

    # set the result of the form validation as the indicator if the form is successfully submitted
    st.session_state["form-submitted-group-csv"] = is_valid

if st.session_state["form-submitted-group-csv"]:
    st.success("Configurations created successfully!")
    st.write("### Preview")
    st.json(form_returns)
    st.session_state["configs"]["group-config.csv"] = convert_group_config_csv_to_csv(form_returns)

    st.download_button(
        label="Download Configurations",
        key="repo-config-internal-download-button",
        data=st.session_state["configs"]["group-config.csv"],
        mime="text/csv",
        file_name='group-config.csv'
    )
