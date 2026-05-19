from __future__ import annotations

import streamlit as st


def render_tab_cards(cards: list[dict[str, str]]) -> None:
    if not cards:
        return

    columns = st.columns(len(cards))
    for column, card in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="summary-card">
                    <div class="summary-card-label">{card["label"]}</div>
                    <div class="summary-card-value">{card["value"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
