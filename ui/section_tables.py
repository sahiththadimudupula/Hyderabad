from __future__ import annotations

import pandas as pd
import streamlit as st

from config.constants import (
    COMPACT_TABLE_HEIGHT,
    DATA_EDITOR_HEIGHT,
    MANPOWER_EDITABLE_COLUMNS,
    MASTER_SHEET_NAME,
    VISIBLE_COMPACT_COLUMNS,
)
from core.excel_io import load_all_engine_data, write_row_updates_to_workbook
from core.excel_recalc import recalculate_workbook_with_excel
from core.formatting import build_formatted_display_dataframe
from core.totals import append_total_row
from ui.table_renderer import render_html_table


NUMERIC_COLUMNS = [
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
]

EDITOR_CONTEXT_COLUMNS = ["Section", "Dept_Machine_Name", "Designation"]


def _available_columns(dataframe: pd.DataFrame, columns: list[str]) -> list[str]:
    return [column for column in columns if column in dataframe.columns]


def _build_editor_config(dataframe: pd.DataFrame):
    editor_config = {}

    for column_name in dataframe.columns:
        if column_name in NUMERIC_COLUMNS:
            editor_config[column_name] = st.column_config.NumberColumn(
                label=column_name,
                format="%.2f",
                step=0.01,
            )
        elif column_name == "Remarks":
            editor_config[column_name] = st.column_config.TextColumn(label=column_name, width="medium")
        elif column_name in EDITOR_CONTEXT_COLUMNS:
            editor_config[column_name] = st.column_config.TextColumn(label=column_name, width="medium")

    return editor_config


def _build_editor_column_order(dataframe: pd.DataFrame) -> list[str]:
    priority_columns = _available_columns(dataframe, EDITOR_CONTEXT_COLUMNS + MANPOWER_EDITABLE_COLUMNS)
    remaining_columns = [column_name for column_name in dataframe.columns if column_name not in priority_columns]
    return priority_columns + remaining_columns


def _normalize_comparable_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    comparable_dataframe = dataframe.copy()
    for column_name in comparable_dataframe.columns:
        if column_name in NUMERIC_COLUMNS:
            comparable_dataframe[column_name] = (
                pd.to_numeric(comparable_dataframe[column_name], errors="coerce")
                .round(2)
                .astype("object")
                .where(lambda series: series.notna(), None)
            )
        else:
            comparable_dataframe[column_name] = comparable_dataframe[column_name].fillna("").astype(str)
    return comparable_dataframe


def _extract_changed_values(original_dataframe: pd.DataFrame, edited_dataframe: pd.DataFrame) -> dict[int, dict[str, object]]:
    editable_columns = _available_columns(edited_dataframe, MANPOWER_EDITABLE_COLUMNS)
    if not editable_columns:
        return {}

    original_values = _normalize_comparable_values(original_dataframe[editable_columns])
    edited_values = _normalize_comparable_values(edited_dataframe[editable_columns])

    changed_updates: dict[int, dict[str, object]] = {}

    for excel_row_number in edited_dataframe.index:
        row_updates: dict[str, object] = {}
        for column_name in editable_columns:
            if edited_values.loc[excel_row_number, column_name] != original_values.loc[excel_row_number, column_name]:
                row_updates[column_name] = edited_dataframe.loc[excel_row_number, column_name]

        if row_updates:
            changed_updates[int(excel_row_number)] = row_updates

    return changed_updates


def render_section_tables(dataframe: pd.DataFrame) -> None:
    if dataframe.empty:
        st.info("No data is available for the selected filters.")
        return

    for section_name, section_dataframe in dataframe.groupby("Section", sort=False):
        section_total = pd.to_numeric(section_dataframe["BE_Final_Manpower"], errors="coerce").fillna(0).sum()
        safe_section_key = str(section_name).replace(" ", "_").replace("/", "_").replace("&", "and")

        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-strip">{section_name} &nbsp;&nbsp;|&nbsp;&nbsp; Final Manpower: {section_total:,.2f}</div>',
            unsafe_allow_html=True,
        )

        compact_columns = _available_columns(section_dataframe, VISIBLE_COMPACT_COLUMNS)
        compact_dataframe = section_dataframe[compact_columns].copy()
        compact_dataframe = append_total_row(compact_dataframe, label_column="Section")
        compact_dataframe = build_formatted_display_dataframe(compact_dataframe, numeric_columns=["BE_Final_Manpower"])
        render_html_table(compact_dataframe, height=COMPACT_TABLE_HEIGHT, compact=True)

        with st.expander(f"Expand full editable table for {section_name}", expanded=False):
            editor_dataframe = section_dataframe.copy().set_index("__excel_row_number", drop=True)
            visible_editor_columns = [
                column_name for column_name in editor_dataframe.columns if not str(column_name).startswith("__")
            ]
            editor_dataframe = editor_dataframe[visible_editor_columns]
            editor_column_order = _build_editor_column_order(editor_dataframe)

            disabled_columns = [
                column_name for column_name in editor_dataframe.columns if column_name not in MANPOWER_EDITABLE_COLUMNS
            ]

            st.markdown('<div class="editor-panel-title">Editable manpower inputs</div>', unsafe_allow_html=True)
            edited_dataframe = st.data_editor(
                editor_dataframe,
                width="stretch",
                hide_index=True,
                height=DATA_EDITOR_HEIGHT,
                disabled=disabled_columns,
                column_order=editor_column_order,
                column_config=_build_editor_config(editor_dataframe),
                key=f"editor_master_{safe_section_key}",
            )

            changed_updates = _extract_changed_values(editor_dataframe, edited_dataframe)
            _, button_column, _ = st.columns([3.2, 1.6, 3.2])

            with button_column:
                if st.button(
                    "Apply Section Changes",
                    key=f"apply_master_{safe_section_key}",
                    width="stretch",
                    disabled=not bool(changed_updates),
                ):
                    metadata = st.session_state.sheet_metadata[MASTER_SHEET_NAME]
                    write_row_updates_to_workbook(
                        st.session_state.working_workbook_path,
                        MASTER_SHEET_NAME,
                        changed_updates,
                        metadata["column_excel_indexes"],
                    )
                    recalculate_workbook_with_excel(st.session_state.working_workbook_path)
                    engine_data = load_all_engine_data(st.session_state.working_workbook_path, data_only=True)
                    st.session_state.master_dataframe = engine_data["master"]
                    st.session_state.bp_dataframe = engine_data["bp"]
                    st.session_state.reqd_mc_dataframe = engine_data["reqd_mc"]
                    st.session_state.sheet_metadata = engine_data["metadata"]
                    st.session_state.freeze_status = "Draft"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
