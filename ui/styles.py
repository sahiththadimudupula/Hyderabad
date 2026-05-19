from __future__ import annotations

import streamlit as st

from config.ui_config import (
    BACKGROUND,
    BORDER_COLOR,
    LIGHT_BLUE,
    NAVY_TEXT,
    PANEL_SHADOW,
    PRIMARY_BLUE,
    RADIUS_LARGE,
    RADIUS_MEDIUM,
    SECONDARY_BLUE,
    SLATE_TEXT,
    WHITE,
)


def apply_global_styles() -> None:
    css = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {display: none;}
        [data-testid="stDecoration"] {display: none;}

        .stApp {
            background: %%BACKGROUND%%;
        }

        .block-container {
            padding-top: 0.65rem;
            padding-bottom: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }

        .engine-shell {
            background: transparent;
            border: none;
            padding: 0.1rem 0 0.35rem 0;
            margin-bottom: 0.55rem;
        }

        .engine-title {
            font-size: 2.05rem;
            font-weight: 850;
            color: %%PRIMARY_BLUE%%;
            letter-spacing: -0.025em;
            margin: 0;
        }

        .summary-card {
            background: linear-gradient(180deg, #ffffff 0%, #f4f9ff 100%);
            border: 1px solid %%BORDER_COLOR%%;
            border-radius: %%RADIUS_MEDIUM%%;
            padding: 1rem 1.05rem;
            box-shadow: %%PANEL_SHADOW%%;
            margin-bottom: 0.8rem;
        }

        .summary-card-label {
            font-size: 0.82rem;
            color: %%SLATE_TEXT%%;
            font-weight: 750;
            margin-bottom: 0.32rem;
        }

        .summary-card-value {
            font-size: 1.55rem;
            color: %%NAVY_TEXT%%;
            font-weight: 850;
            line-height: 1.1;
        }

        .section-panel {
            background: %%WHITE%%;
            border: 1px solid %%BORDER_COLOR%%;
            border-radius: 8px;
            padding: 0.65rem 0.75rem 0.95rem 0.75rem;
            box-shadow: %%PANEL_SHADOW%%;
            margin-bottom: 1rem;
        }

        .section-strip {
            background: linear-gradient(90deg, %%PRIMARY_BLUE%% 0%, %%SECONDARY_BLUE%% 100%);
            color: %%WHITE%%;
            padding: 0.82rem 1rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }

        .editor-panel-title {
            color: %%NAVY_TEXT%%;
            font-size: 0.95rem;
            font-weight: 850;
            margin: 0.2rem 0 0.65rem 0;
        }

        div[data-testid="stExpander"] {
            border: 1px solid %%BORDER_COLOR%%;
            border-radius: 8px;
            background: #fbfdff;
            margin-top: 0.75rem;
            overflow: hidden;
        }

        div[data-testid="stExpander"] details > summary {
            background: #eef6ff;
            min-height: 2.8rem;
            padding: 0.25rem 0.75rem;
        }

        div[data-testid="stExpander"] details > summary p {
            color: %%NAVY_TEXT%% !important;
            font-size: 0.92rem;
            font-weight: 800;
        }

        div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            padding: 0.85rem 0.9rem 0.95rem 0.9rem;
            background: #ffffff;
        }

        .summary-banner {
            background: %%LIGHT_BLUE%%;
            border: 1px solid %%BORDER_COLOR%%;
            border-radius: %%RADIUS_MEDIUM%%;
            padding: 0.75rem 0.95rem;
            margin: 0.8rem 0;
        }

        .summary-banner-text {
            color: %%NAVY_TEXT%%;
            font-weight: 800;
            font-size: 0.92rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.65rem;
            background: transparent;
            padding: 0.15rem 0 0.65rem 0;
        }

        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            border-radius: 999px;
            background: %%WHITE%%;
            border: 1px solid %%BORDER_COLOR%%;
            color: %%NAVY_TEXT%%;
            font-weight: 750;
            padding: 0 1.15rem;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, %%PRIMARY_BLUE%% 0%, %%SECONDARY_BLUE%% 100%);
            color: %%WHITE%% !important;
            border: 1px solid %%PRIMARY_BLUE%%;
        }

        .stButton > button {
            border-radius: 999px;
            height: 2.75rem;
            border: 1px solid %%PRIMARY_BLUE%%;
            font-weight: 750;
            background: %%WHITE%%;
            color: %%NAVY_TEXT%%;
        }

        .stButton > button:hover {
            border-color: %%SECONDARY_BLUE%%;
            color: %%PRIMARY_BLUE%%;
        }

        .stDownloadButton > button {
            border-radius: 999px;
            height: 2.75rem;
            border: 1px solid %%PRIMARY_BLUE%%;
            font-weight: 750;
            background: linear-gradient(90deg, %%PRIMARY_BLUE%% 0%, %%SECONDARY_BLUE%% 100%);
            color: %%WHITE%%;
        }

        div[data-testid="stDataEditor"] {
            border: 1px solid %%BORDER_COLOR%%;
            border-radius: 8px;
            overflow: hidden;
            background: #ffffff !important;
        }

        div[data-testid="stDataEditor"] * {
            color: #111111 !important;
        }

        div[data-testid="stDataEditor"] input,
        div[data-testid="stDataEditor"] textarea,
        div[data-testid="stDataEditor"] [role="gridcell"],
        div[data-testid="stDataEditor"] [role="columnheader"],
        div[data-testid="stDataEditor"] section,
        div[data-testid="stDataEditor"] canvas {
            background: #ffffff !important;
            color: #111111 !important;
        }
    </style>
    """

    replacements = {
        "%%BACKGROUND%%": BACKGROUND,
        "%%BORDER_COLOR%%": BORDER_COLOR,
        "%%LIGHT_BLUE%%": LIGHT_BLUE,
        "%%NAVY_TEXT%%": NAVY_TEXT,
        "%%PANEL_SHADOW%%": PANEL_SHADOW,
        "%%PRIMARY_BLUE%%": PRIMARY_BLUE,
        "%%RADIUS_LARGE%%": RADIUS_LARGE,
        "%%RADIUS_MEDIUM%%": RADIUS_MEDIUM,
        "%%SECONDARY_BLUE%%": SECONDARY_BLUE,
        "%%SLATE_TEXT%%": SLATE_TEXT,
        "%%WHITE%%": WHITE,
    }

    for placeholder, value in replacements.items():
        css = css.replace(placeholder, value)

    st.markdown(css, unsafe_allow_html=True)
