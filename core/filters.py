from __future__ import annotations

import pandas as pd


def ordered_unique_values(series: pd.Series) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()

    for value in series.fillna("").astype(str):
        cleaned_value = value.strip()
        if not cleaned_value or cleaned_value in seen:
            continue
        seen.add(cleaned_value)
        values.append(cleaned_value)

    return values


def apply_manpower_filters(
    dataframe: pd.DataFrame,
    selected_sections: list[str],
    selected_machines: list[str],
    selected_designations: list[str],
    remarks_search_text: str,
) -> pd.DataFrame:
    filtered_dataframe = dataframe.copy()

    if selected_sections:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Section"].fillna("").astype(str).isin(selected_sections)
        ]

    if selected_machines:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Dept_Machine_Name"].fillna("").astype(str).isin(selected_machines)
        ]

    if selected_designations:
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Designation"].fillna("").astype(str).isin(selected_designations)
        ]

    if remarks_search_text and "Remarks" in filtered_dataframe.columns:
        search_text = remarks_search_text.strip().lower()
        filtered_dataframe = filtered_dataframe[
            filtered_dataframe["Remarks"].fillna("").astype(str).str.lower().str.contains(search_text, na=False)
        ]

    if "__row_order" in filtered_dataframe.columns:
        filtered_dataframe = filtered_dataframe.sort_values("__row_order", kind="stable")

    return filtered_dataframe
