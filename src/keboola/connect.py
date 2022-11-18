import streamlit as st
import os
import requests
from requests.exceptions import HTTPError
import wget
import tarfile
import glob

KBC_URLS = ['https://connection.keboola.com/',
            'https://connection.north-europe.azure.keboola.com/',
            'https://connection.eu-central-1.keboola.com/']


def add_keboola_table_selection():
    """
        This function is used to initialize all forms to deal with loading a table from Keboola Storage.
        - The Connection Form enters the KBC URL and API Token
        - The Bucket Form enters the selected bucket
        - The Table Form enters the selected table

        The Bucket Form only appears once a connection is made
        The Table Form only appears when a Bucket is selected

    """
    _add_connection_form()
    if 'artifacts' in st.session_state:
        _add_timestamp_form()
    if 'selected_timestamp' in st.session_state:
        _get_table()


def _add_connection_form():
    with st.sidebar.form("Connection Details"):
        connection_url = st.selectbox('Connection URL', KBC_URLS)
        api_key = st.text_input('API Token', 'Enter Password', type="password")
        st.session_state["api_key"] = api_key
        if st.form_submit_button("Connect"):

            # Reset Client
            if "kbc_storage_client" in st.session_state:
                st.session_state.pop("kbc_storage_client")

            # Clear selected buckets and tables if connection is reset
            if "selected_table" in st.session_state:
                st.session_state.pop("selected_table")
            if "selected_table_id" in st.session_state:
                st.session_state.pop("selected_table_id")
            if "selected_bucket" in st.session_state:
                st.session_state.pop("selected_bucket")
            if "uploaded_file" in st.session_state:
                st.session_state.pop("uploaded_file")

            api_url = connection_url + "v2/storage/files/"
            params = {"tags[]": "artifact"}
            headers = {"X-StorageApi-Token": api_key}
            if r := _get_list_of_artifacts(api_url, params, headers):
                st.session_state['artifacts'] = r


def _add_timestamp_form():
    with st.sidebar.form("Run Details"):
        with st.header('Select the run timestamp'):
            try:
                list_of_timestamps = _get_artifact_details()
                ts = st.selectbox('Timestamp', list_of_timestamps)
            except TypeError:
                st.write("Cannot connect to selected source. Check your Connection URL and API Token.")
        if st.form_submit_button("Select Run Timestamp"):
            try:
                st.session_state['selected_timestamp'] = ts
            except UnboundLocalError:
                pass


def _get_list_of_artifacts(api_url, params, headers):
    try:
        r = requests.get(api_url, params=params, headers=headers)
        return r.json()
    except HTTPError:
        st.error("Invalid Connection settings")


def _get_artifact_details():
    """
    This function is used to get the list of buckets from Keboola Storage.
    """
    try:
        return [x['created'] for x in st.session_state['artifacts']]
    except Exception:
        st.error('Could not list buckets')


def _get_table():
    download_path = os.path.join(os.getcwd(), "download")
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    else:
        files = glob.glob(f'{download_path}/*')
        for f in files:
            os.remove(f)

    artifacts = st.session_state["artifacts"]
    ts = st.session_state["selected_timestamp"]

    artifact_info = [x for x in artifacts if x["created"] == ts][0]

    download_url = artifact_info["url"]
    filepath = os.path.join(download_path, str(artifact_info["name"]))
    wget.download(download_url, filepath)

    with tarfile.open(filepath) as file:
        file.extractall('.')

    st.session_state['extracted_file'] = os.path.join(os.getcwd(), "benchmark.csv")
    print(f"table downloaded: {st.session_state['extracted_file']}")
