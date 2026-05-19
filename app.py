from __future__ import annotations

from datetime import datetime
from pathlib import Path
from shutil import copy2

import streamlit as st

from config.constants import (
    APP_TABS,
    APP_TITLE,
    OUTPUT_DIRECTORY,
    SUCCESS_STATUS,
)
from core.excel_io import (
    ensure_working_workbook,
    load_all_engine_data,
    reset_working_workbook,
    resolve_input_workbook_path,
    workbook_exists,
)
from core.session_state import clear_ui_state, initialize_session_state, refresh_session_state
from ui.driver_tabs import render_bp_structured_tab, render_required_machines_tab
from ui.final_master import render_final_master_tab
from ui.header import render_page_header
from ui.manpower_tab import render_flooring_manpower_tab
from ui.styles import apply_global_styles

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _reload_working_data() -> None:
    engine_data = load_all_engine_data(st.session_state.working_workbook_path, data_only=True)
    refresh_session_state(engine_data)


def _freeze_workbook() -> Path:
    output_directory = Path(OUTPUT_DIRECTORY)
    output_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    frozen_path = output_directory / f"Hyderabad_Manpower_Frozen_{timestamp}.xlsx"
    copy2(st.session_state.working_workbook_path, frozen_path)
    return frozen_path


def render_plan_actions() -> None:
    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Plan Actions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, reset_column, freeze_column, _ = st.columns([3.2, 1.2, 1.4, 3.2])

    with reset_column:
        if st.button("Reset", key="bottom_reset_button", width="stretch"):
            working_workbook_path = reset_working_workbook(st.session_state.input_workbook_path)
            clear_ui_state()
            engine_data = load_all_engine_data(str(working_workbook_path), data_only=True)
            refresh_session_state(engine_data)
            st.session_state.working_workbook_path = str(working_workbook_path)
            st.session_state.freeze_status = "Draft"
            st.session_state.last_freeze_timestamp = None
            st.rerun()

    with freeze_column:
        if st.button("Freeze Plan", key="bottom_freeze_button", width="stretch"):
            frozen_path = _freeze_workbook()
            _reload_working_data()
            st.session_state.freeze_status = SUCCESS_STATUS
            st.session_state.last_freeze_timestamp = frozen_path.name
            st.success("Plan frozen successfully.")


def main() -> None:
    apply_global_styles()

    input_workbook_path = resolve_input_workbook_path()
    if not workbook_exists(input_workbook_path):
        st.error(f"Workbook not found at: {input_workbook_path}")
        st.stop()

    working_workbook_path = ensure_working_workbook(input_workbook_path)
    engine_data = load_all_engine_data(str(working_workbook_path), data_only=True)
    initialize_session_state(
        engine_data,
        str(input_workbook_path),
        str(working_workbook_path),
    )

    render_page_header()

    tabs = st.tabs(APP_TABS)

    with tabs[0]:
        render_flooring_manpower_tab()

    with tabs[1]:
        render_bp_structured_tab()

    with tabs[2]:
        render_required_machines_tab()

    with tabs[3]:
        render_final_master_tab()
        if st.session_state.last_freeze_timestamp:
            st.info(f"Last frozen file: {st.session_state.last_freeze_timestamp}")

    render_plan_actions()


if __name__ == "__main__":
    main()
