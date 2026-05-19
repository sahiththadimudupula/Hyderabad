from __future__ import annotations

import pandas as pd
import streamlit as st

from config.constants import SUMMARY_TABLE_HEIGHT
from core.formatting import build_formatted_display_dataframe
from ui.table_renderer import render_html_table


def render_summary_table(summary_dataframe: pd.DataFrame) -> None:
    st.markdown(
        """
        <div class="summary-banner">
            <div class="summary-banner-text">Section Summary</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_dataframe = build_formatted_display_dataframe(
        summary_dataframe,
        numeric_columns=["Machine_Count", "BE_Final_Manpower"],
    )

    render_html_table(display_dataframe, height=SUMMARY_TABLE_HEIGHT, compact=True)
