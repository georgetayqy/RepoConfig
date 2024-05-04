import streamlit as st

from streamlit_tags import st_tags
from utils.utils import convert_repo_config_csv_to_csv, check_config_file_state, zip_files

st.set_page_config(
    page_title="repo-config.csv",
    page_icon="⚙️",
)


# define session states to be used
if "form-submitted-repo-csv" not in st.session_state:
    st.session_state["form-submitted-repo-csv"] = False

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

st.subheader("`repo-config.csv` Configuration Wizard")
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
    num_branches = st.number_input(
        label=f"Select the number of branches to include in this repository",
        key=f"repo-config-branch-count{reponumber}",
        min_value=1,
        step=1
    )

    # create a new entry in the dict to for updates
    if repo_location and num_branches:
        form_returns[repo_location] = {}

        for branch in range(num_branches):
            st.markdown(f"### Branch {branch + 1}")
            branch_base_key = repo_location + str(branch)  # defines the base key for all widgets in this branch

            branch_name = st.text_input(
                "Enter the name of your branch",
                key=base_key + branch_base_key + "branch_name",
                help="Branch to analyze in the target repository, e.g. `master`")

            if branch_name:
                find_prev_authors = st.checkbox(
                    "Find Previous Authors?",
                    key=base_key + branch_base_key + "find_prev_authors",
                    value=False,
                    help="If enabled, RepoSense will utilize Git blame's ignore revisions functionality to "
                         "blame the line changes caused by commits in the ignore commit list to the previous "
                         "authors who altered those lines (if available)")
                ignore_standalone_configs = st.checkbox(
                    "Ignore Standalone Configs?",
                    key=base_key + branch_base_key + "ignore_standalone_configs",
                    value=False,
                    help="If enabled, RepoSense will ignore the standalone config file (if any) in target "
                         "repository, else the standalone config file will take precedence over configurations "
                         "provided in the CSV files")
                shallow_cloning = st.checkbox(
                    "Shallow Cloning?",
                    key=base_key + branch_base_key + "shallow_cloning",
                    value=False,
                    help="If enabled, RepoSense will utilize Git' shallow clone functionality. This option may "
                         "reduce the time taken to clone repositories, but should be disabled for smaller "
                         "`.git` files of size < 500 MB due to overhead incurred")
                ignore_file_size_limits = st.checkbox(
                    "Ignore File Size Limits?",
                    key=base_key + branch_base_key + "ignore_file_size_limits",
                    value=False,
                    help="If enabled, RepoSense will ignore both the default file size limit and file size "
                         "limits defined by the user in `repo-config.csv`")
                skip_ignored_file_analysis = st.checkbox(
                    "Skip Ignored File Analysis?",
                    key=base_key + branch_base_key + "skip_ignored_file_analysis",
                    value=False,
                    help="If enabled, RepoSense will ignore analysis of files exceeding the file size "
                         "entirely. If skipped, all information about the file will be omitted from the "
                         "report [can possibly improve report generation time!]")
                file_size_limits = st.number_input(
                    "Enter a file size limit for the repository in **bytes**",
                    key=base_key + branch_base_key + "file_size_limits",
                    min_value=0,
                    value=500000,
                    help="Files exceeding the file size limit will be marked as ignored and only the file name "
                         "and line count will be reflected in the report")
                file_fmts = st_tags(
                    label="Enter in file extensions to analyse",
                    key=base_key + branch_base_key + "file_fmts",
                    suggestions=["py", "java"],
                    text="Leave blank to analyse all file types...")
                ignore_glob_lists = st_tags(
                    label="Enter in the list of file path globs to ignore during analysis for each author "
                          "(Refer to [this](https://docs.oracle.com/javase/tutorial/essential/io/fileOps.html"
                          "#glob) for more info on path glob syntax)",
                    text="e.g. test/**, temp/**...",
                    key=base_key + branch_base_key + "ignore_glob_lists")
                ignore_commits_list = st_tags(
                    label="Enter in the list of commit hashes (full or partial) to ignore during analysis",
                    key=base_key + branch_base_key + "ignore_commits_list",
                    text="Use .. to specify range of commits...")
                ignore_authors_list = st_tags(
                    label="Enter in the list of authors to ignore during analysis, specified by "
                          "[Git Author Name](https://reposense.org/ug/configFiles.html#a-note-about-git-"
                          "author-name)",
                    key=base_key + branch_base_key + "ignore_authors_list",
                    text="e.g. long_Git_author-Name123...")

                # write to return dict each branch
                if all([branch_name, file_size_limits, file_fmts,
                        ignore_glob_lists, ignore_commits_list, ignore_authors_list]):
                    form_returns[repo_location][branch_name] = curr = {}
                    # convert all file formats to lowercase for easier processing later
                    curr["file_size_limits"] = file_size_limits
                    curr["file_fmts"] = [ff.lower() for ff in file_fmts]
                    curr["ignore_glob_lists"] = [gl.strip() for gl in ignore_glob_lists]
                    curr["ignore_commits_list"] = [cl.strip() for cl in ignore_commits_list]
                    curr["ignore_authors_list"] = [al.strip() for al in ignore_authors_list]
                    curr["find_prev_authors"] = find_prev_authors
                    curr["ignore_standalone_configs"] = ignore_standalone_configs
                    curr["shallow_cloning"] = shallow_cloning
                    curr["ignore_file_size_limits"] = ignore_file_size_limits
                    curr["skip_ignored_file_analysis"] = skip_ignored_file_analysis

    if reponumber != num_repo - 1:
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
    st.session_state["form-submitted-repo-csv"] = is_valid

if st.session_state["form-submitted-repo-csv"]:
    st.success("Configurations created successfully!")
    st.write("### Preview")
    st.json(form_returns)
    st.session_state["configs"]["repo-config.csv"] = convert_repo_config_csv_to_csv(form_returns)

    st.download_button(
        label="Download Configurations",
        key="repo-config-internal-download-button",
        data=st.session_state["configs"]["repo-config.csv"],
        mime="text/csv",
        file_name='repo-config.csv'
    )
