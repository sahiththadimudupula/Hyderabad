from __future__ import annotations

import pandas as pd

from config.constants import DEFAULT_DECIMAL_PLACES


def to_numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def format_number(value: object, decimals: int = DEFAULT_DECIMAL_PLACES) -> str:
    if value is None or pd.isna(value):
        return ""

    numeric_value = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric_value):
        return str(value)

    return f"{float(numeric_value):,.{decimals}f}"


def build_formatted_display_dataframe(
    dataframe: pd.DataFrame,
    numeric_columns: list[str] | None = None,
) -> pd.DataFrame:
    display_dataframe = dataframe.copy()
    numeric_columns = numeric_columns or []

    for column_name in numeric_columns:
        if column_name in display_dataframe.columns:
            display_dataframe[column_name] = display_dataframe[column_name].apply(format_number)

    return display_dataframe
