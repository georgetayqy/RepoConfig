import os
import io
import pandas as pd
import streamlit as st
from zipfile import ZipFile


TEMP_DIR = "./temp"
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)


def check_config_file_state(name_to_file_mapping: dict[str, bytes]):
    if len(name_to_file_mapping) == 0:
        st.warning("No config files created!")

    return name_to_file_mapping


def zip_files(name_to_file_mapping: dict[str, bytes]):
    """
    Converts a series of files into a zip file for downloading.

    References https://discuss.streamlit.io/t/downloading-two-csv-files-using-download-button/39955/2
    :param name_to_file_mapping: Mapping from file name to bytes.
    :return: ByteIO object
    """

    buffer = io.BytesIO()

    with ZipFile(buffer, "x") as file:
        for name, data in name_to_file_mapping.items():
            file.writestr(name, data)

    return buffer


@st.cache_data
def convert_repo_config_csv_to_csv(repoinfo: dict[str, dict[str, dict]]) -> bytes:
    """
    Converts the repo-config map from the form into a CSV file.

    :param repoinfo: Dictionary containing the repository name to branch info and configurations.
    :return: Pandas dataframe containing the mappings.
    """

    all_entries = []
    headers = ["Repository's Location", "Branch", "File formats", "Ignore Glob List", "Ignore standalone config",
               "Ignore Commits List", "Ignore Authors List", "Shallow Cloning", "Find Previous Authors",
               "File Size Limit", "Ignore File Size Limit", "Skip Ignored File Analysis"]

    for repo_url, branches in repoinfo.items():
        for branch, configs in branches.items():
            all_entries.append([
                repo_url,
                branch,
                ";".join(configs["file_fmts"]),
                ";".join(configs["ignore_glob_lists"]),
                "yes" if configs["ignore_standalone_configs"] else "",
                ";".join(configs["ignore_commits_list"]),
                ";".join(configs["ignore_authors_list"]),
                "yes" if configs["shallow_cloning"] else "",
                "yes" if configs["find_prev_authors"] else "",
                0 if configs["file_size_limits"] < 0 else configs["file_size_limits"],
                "yes" if configs["ignore_file_size_limits"] else "",
                "yes" if configs["skip_ignored_file_analysis"] else ""
            ])

    df = pd.DataFrame(all_entries, columns=headers)

    # need to save it to disk first for Docker containers
    df.to_csv("temp/repo-config.csv", index=False)
    return df.to_csv(index=False).encode("utf-8")
