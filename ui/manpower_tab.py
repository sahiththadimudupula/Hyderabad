from __future__ import annotations

import streamlit as st

from calculations.summary_calculations import build_manpower_summary
from core.filters import apply_manpower_filters
from core.totals import build_manpower_kpis
from ui.filter_bar import render_manpower_filter_bar
from ui.section_tables import render_section_tables
from ui.summary_table import render_summary_table
from ui.tab_cards import render_tab_cards


def render_flooring_manpower_tab() -> None:
    dataframe = st.session_state.master_dataframe.copy()

    selected_sections, selected_machines, selected_designations, remarks_search_text = render_manpower_filter_bar(
        dataframe
    )

    filtered_dataframe = apply_manpower_filters(
        dataframe,
        selected_sections,
        selected_machines,
        selected_designations,
        remarks_search_text,
    )

    render_tab_cards(build_manpower_kpis(filtered_dataframe))
    render_summary_table(build_manpower_summary(filtered_dataframe))
    render_section_tables(filtered_dataframe)
