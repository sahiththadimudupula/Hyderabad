from __future__ import annotations

from pathlib import Path

import streamlit as st

from config.constants import FINAL_TABLE_HEIGHT, HIDDEN_SYSTEM_COLUMNS
from core.excel_io import create_download_workbook_copy
from core.formatting import build_formatted_display_dataframe
from core.totals import append_total_row, build_manpower_kpis
from ui.table_renderer import render_html_table
from ui.tab_cards import render_tab_cards


def render_final_master_tab() -> None:
    dataframe = st.session_state.master_dataframe.copy()
    render_tab_cards(build_manpower_kpis(dataframe))

    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Fully Updated Master Sheet</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_columns = [
        column_name
        for column_name in dataframe.columns
        if column_name not in HIDDEN_SYSTEM_COLUMNS and not str(column_name).startswith("__")
    ]

    display_dataframe = dataframe[display_columns].copy()
    display_dataframe = append_total_row(display_dataframe, label_column="Section")
    numeric_columns = [
        "Machine_Count",
        "Manpower_Base_Qty",
        "N_shifts",
        "W",
        "BE_Scientific_Manpower",
        "Contractors",
        "Company_Associate",
        "BE_Final_Manpower",
        "General_Shift",
        "Shift_A",
        "Shift_B",
        "Shift_C",
        "Reliever",
    ]
    display_dataframe = build_formatted_display_dataframe(
        display_dataframe,
        numeric_columns=[column for column in numeric_columns if column in display_dataframe.columns],
    )
    render_html_table(display_dataframe, height=FINAL_TABLE_HEIGHT, compact=False)

    download_path = create_download_workbook_copy(st.session_state.working_workbook_path)
    workbook_name = Path(download_path).name

    with open(download_path, "rb") as workbook_file:
        st.download_button(
            "Download Updated Workbook",
            data=workbook_file.read(),
            file_name=workbook_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="content",
        )
