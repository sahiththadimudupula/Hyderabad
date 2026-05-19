from __future__ import annotations

import streamlit as st

from config.constants import APP_TITLE


def render_page_header() -> None:
    st.markdown(
        f"""
        <div class="engine-shell">
            <div class="engine-title">{APP_TITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
