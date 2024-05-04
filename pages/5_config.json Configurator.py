import streamlit as st

from streamlit_tags import st_tags
from utils.utils import convert_config_json_to_json, check_config_file_state, zip_files

st.set_page_config(
    page_title="repo-config.csv",
    page_icon="⚙️",
)


# define session states to be used
if "form-submitted-config-json" not in st.session_state:
    st.session_state["form-submitted-config-json"] = False

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

st.subheader("`config.json` Configuration Wizard")
st.write("Enter in the following details to get started!")
st.write("#### Repo and Branch Configurations")

ignore_glob_lists = st_tags(
    label="Enter in the list of file path globs to ignore during analysis for each author "
          "(Refer to [this](https://docs.oracle.com/javase/tutorial/essential/io/fileOps.html"
          "#glob) for more info on path glob syntax)",
    text="e.g. test/**, temp/**...",
    key="ignore_glob_lists")
file_fmts = st_tags(
    label="Enter in file extensions to analyse",
    key="file_fmts",
    suggestions=["py", "java"],
    text="Leave blank to analyse all file types...")
ignore_commits_list = st_tags(
    label="Enter in the list of commit hashes (full or partial) to ignore during analysis",
    key="ignore_commits_list",
    text="Use .. to specify range of commits...")
ignore_authors_list = st_tags(
    label="Enter in the list of authors to ignore during analysis, specified by "
          "[Git Author Name](https://reposense.org/ug/configFiles.html#a-note-about-git-"
          "author-name)",
    key="ignore_authors_list",
    text="e.g. long_Git_author-Name123...")
num_authors = st.number_input(
    "Select the number of repositories to include",
    key="repo-config-num-repo",
    min_value=1,
)

form_returns: dict = {
    "ignoreGlobList": [gl.strip() for gl in ignore_glob_lists],
    "formats": [ff.lower().strip() for ff in file_fmts],
    "ignoreCommitList": [cl.strip() for cl in ignore_commits_list],
    "ignoreAuthorList": [al.strip() for al in ignore_authors_list],
}

for author in range(num_authors):
    base_key = str(author)  # defines the base key for all widgets to avoid key errors

    st.markdown(f"### Author {author + 1}")
    author_git_host_id = st.text_input(
        label="Enter in the Author's Git Host ID",
        key=base_key + "author_git_host_id",
        help="Username of the target author's profile on GitHub, GitLab or Bitbucket, e.g. `JohnDoe`"
    )
    author_display_name = st.text_input(
        label="Enter the name of the author's display name",
        key=base_key + "author_display_name",
        help="The name to display for the author; defaults to author's username"
    )
    author_emails = st_tags(
        label="Enter in the email(s) associated with an author",
        key=base_key + "author_emails"
    )
    git_author_name = st_tags(
        label="Enter in the `git` author name(s)",
        key=base_key + "git_author_name"
    )
    ignore_glob_lists = st_tags(
        label="Enter in the list of file path globs to ignore during analysis for each author "
              "(Refer to [this](https://docs.oracle.com/javase/tutorial/essential/io/fileOps.html"
              "#glob) for more info on path glob syntax)",
        text="e.g. test/**, temp/**...",
        key=base_key + "ignore_glob_lists")

    # write to return dict each branch
    if all([file_fmts, ignore_glob_lists, ignore_commits_list, ignore_authors_list, author_git_host_id,
            author_display_name, author_emails, git_author_name, ignore_glob_lists]):
        form_returns["authors"] = {}
        form_returns["authors"][author] = curr = {}
        curr["gitId"] = author_git_host_id
        curr["emails"] = [ae.strip() for ae in author_emails]
        curr["displayName"] = author_display_name
        curr["authorNames"] = [an.strip() for an in git_author_name]
        curr["ignoreGlobList"] = [gl.lower() for gl in ignore_glob_lists]

    if author != num_authors - 1:
        st.divider()

# if st.form_submit_button("Create RepoSense Configuration!"):
if st.button("Create configurations!"):
    is_valid = True
    if len(form_returns) < 1:
        is_valid = False
        st.error("Check your form and ensure that you fill in all mandatory fields for the repositories!")

    for repo, branches in form_returns.items():
        if len(branches) < 1:
            is_valid = False

    if not is_valid:
        st.error("Check your inputs and ensure that you filled in all mandatory fields for the "
                 "branches!")

    # set the result of the form validation as the indicator if the form is successfully submitted
    st.session_state["form-submitted-config-json"] = is_valid

if st.session_state["form-submitted-config-json"]:
    st.success("Configurations created successfully!")
    st.write("### Preview")
    st.json(form_returns)
    st.session_state["configs"]["config.json"] = convert_config_json_to_json(form_returns)

    st.download_button(
        label="Download Configurations",
        key="repo-config-internal-download-button",
        data=st.session_state["configs"]["config.json"],
        mime="application/octet-stream",
        file_name='config.json'
    )
