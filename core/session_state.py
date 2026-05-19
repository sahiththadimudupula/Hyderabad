from __future__ import annotations

import streamlit as st

from config.constants import PENDING_STATUS


def initialize_session_state(engine_data: dict, input_workbook_path: str, working_workbook_path: str) -> None:
    if "hyderabad_engine_initialized" not in st.session_state:
        st.session_state.input_workbook_path = input_workbook_path
        st.session_state.working_workbook_path = working_workbook_path
        st.session_state.freeze_status = PENDING_STATUS
        st.session_state.last_freeze_timestamp = None
        st.session_state.hyderabad_engine_initialized = True

    refresh_session_state(engine_data)


def refresh_session_state(engine_data: dict) -> None:
    st.session_state.master_dataframe = engine_data["master"]
    st.session_state.bp_dataframe = engine_data["bp"]
    st.session_state.reqd_mc_dataframe = engine_data["reqd_mc"]
    st.session_state.sheet_metadata = engine_data["metadata"]


def clear_ui_state() -> None:
    keys_to_remove = [
        key
        for key in st.session_state.keys()
        if key.startswith("filter_")
        or key.startswith("editor_")
        or key.startswith("apply_")
    ]

    for key in keys_to_remove:
        del st.session_state[key]
