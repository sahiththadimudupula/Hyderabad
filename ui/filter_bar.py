from __future__ import annotations

import pandas as pd
import streamlit as st

from core.filters import ordered_unique_values


def render_manpower_filter_bar(dataframe: pd.DataFrame):
    section_options = ordered_unique_values(dataframe["Section"]) if "Section" in dataframe.columns else []
    machine_options = ordered_unique_values(dataframe["Dept_Machine_Name"]) if "Dept_Machine_Name" in dataframe.columns else []
    designation_options = ordered_unique_values(dataframe["Designation"]) if "Designation" in dataframe.columns else []

    section_column, machine_column, designation_column, remarks_column = st.columns([1.2, 1.2, 1.2, 1.1])

    with section_column:
        selected_sections = st.multiselect(
            "Section",
            options=section_options,
            default=[],
            key="filter_section",
            placeholder="All sections",
        )

    with machine_column:
        selected_machines = st.multiselect(
            "Machine",
            options=machine_options,
            default=[],
            key="filter_machine",
            placeholder="All machines",
        )

    with designation_column:
        selected_designations = st.multiselect(
            "Designation",
            options=designation_options,
            default=[],
            key="filter_designation",
            placeholder="All designations",
        )

    with remarks_column:
        remarks_search_text = st.text_input(
            "Remarks",
            value="",
            key="filter_remarks",
            placeholder="Search remarks",
        )

    return selected_sections, selected_machines, selected_designations, remarks_search_text
