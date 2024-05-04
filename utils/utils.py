import json
import os
import io
import pandas as pd
import streamlit as st
from zipfile import ZipFile


TEMP_DIR = "./temp"
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)
else:
    for file in os.listdir(TEMP_DIR):
        os.remove(os.path.join(TEMP_DIR, file))

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
    :return: Bytes object
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


@st.cache_data
def convert_author_config_csv_to_csv(repoinfo: dict[str, dict[str, dict]]) -> bytes:
    """
    Converts the author-config map from the form into a CSV file.

    :param repoinfo: Dictionary containing the repository name to branch info and authors.
    :return: Bytes object
    """

    all_entries = []
    headers = ["Repository's Location",	"Branch", "Author's Git Host ID", "Author's Emails", "Author's Display Name",
               "Author's Git Author Name", "Ignore Glob List"]

    for repo_url, branches in repoinfo.items():
        for branch, configs in branches.items():
            all_entries.append([
                repo_url,
                branch,
                configs["author_git_host_id"],
                ";".join(configs["author_emails"]),
                configs["author_display_name"],
                ";".join(configs["git_author_name"]),
                ";".join(configs["ignore_glob_lists"])
            ])

    df = pd.DataFrame(all_entries, columns=headers)

    # need to save it to disk first for Docker containers
    df.to_csv("temp/author-config.csv", index=False)
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data
def convert_group_config_csv_to_csv(repoinfo: dict[str, dict[str, dict]]) -> bytes:
    """
    Converts the group-config map from the form into a CSV file.

    :param repoinfo: Dictionary containing the repository name to branch info and authors.
    :return: Bytes object
    """

    all_entries = []
    headers = ["Repository's Location", "Group Name", "Globs"]

    for repo_url, groups in repoinfo.items():
        for group, configs in groups.items():
            all_entries.append([
                repo_url,
                group,
                ";".join(configs["glob_lists"]),
            ])

    df = pd.DataFrame(all_entries, columns=headers)

    # need to save it to disk first for Docker containers
    df.to_csv("temp/group-config.csv", index=False)
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data
def convert_report_config_json_to_json(repoinfo: dict[str, str]) -> str:
    """
    Converts the report-config.json mapping to a JSON file.

    :param repoinfo: Dictionary containing JSON-serializable data to turn into a JSON file
    :return: JSON string
    """

    with open("temp/report-config.json", "w") as f:
        json.dump(repoinfo, f, ensure_ascii=False, indent=4)

    return json.dumps(repoinfo, indent=4)


@st.cache_data
def convert_config_json_to_json(repoinfo: dict) -> str:
    """
    Converts the report-config.json mapping to a JSON file.

    :param repoinfo: Dictionary containing JSON-serializable data to turn into a JSON file
    :return: JSON string
    """

    repoinfo_copy = repoinfo.copy()
    repoinfo_copy["authors"] = list(repoinfo_copy["authors"].values())

    with open("temp/config.json", "w") as f:
        json.dump(repoinfo_copy, f, ensure_ascii=False, indent=4)

    return json.dumps(repoinfo_copy, indent=4)
