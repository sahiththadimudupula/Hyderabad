from __future__ import annotations

import pandas as pd

from config.constants import TOTAL_LABEL


def _numeric_sum(dataframe: pd.DataFrame, column_name: str) -> float:
    if column_name not in dataframe.columns:
        return 0.0

    return float(pd.to_numeric(dataframe[column_name], errors="coerce").fillna(0).sum())


def append_total_row(dataframe: pd.DataFrame, label_column: str = "Section") -> pd.DataFrame:
    if dataframe.empty:
        return dataframe

    output_dataframe = dataframe.copy()
    total_row = {column_name: "" for column_name in output_dataframe.columns}

    if label_column in total_row:
        total_row[label_column] = TOTAL_LABEL
    else:
        total_row[output_dataframe.columns[0]] = TOTAL_LABEL

    total_columns = [
        "Machine_Count",
        "BE_Final_Manpower",
        "BE_Scientific_Manpower",
        "General_Shift",
        "Shift_A",
        "Shift_B",
        "Shift_C",
        "Reliever",
        "Total Capacity/Day",
        "Total Capacity/Day/MC",
        "BP/Month",
        "BP/Day",
        "Available_MC",
        "Reqd_MC",
    ]

    for column_name in total_columns:
        if column_name in output_dataframe.columns:
            total_row[column_name] = _numeric_sum(output_dataframe, column_name)

    return pd.concat([output_dataframe, pd.DataFrame([total_row])], ignore_index=True)


def build_manpower_kpis(dataframe: pd.DataFrame) -> list[dict[str, str]]:
    section_count = dataframe["Section"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().nunique()
    machine_count = _numeric_sum(dataframe, "Machine_Count")
    final_manpower = _numeric_sum(dataframe, "BE_Final_Manpower")

    return [
        {"label": "Total Sections Parsed", "value": f"{section_count:,.0f}"},
        {"label": "Machine Count", "value": f"{machine_count:,.2f}"},
        {"label": "Total Final Manpower", "value": f"{final_manpower:,.2f}"},
    ]


def build_bp_kpis(dataframe: pd.DataFrame, month_columns: list[str]) -> list[dict[str, str]]:
    total_machines = dataframe["Machine"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().nunique()
    total_bp_value = 0.0

    for column_name in month_columns:
        total_bp_value += _numeric_sum(dataframe, column_name)

    return [
        {"label": "Total Machines", "value": f"{total_machines:,.0f}"},
        {"label": "Total BP Value", "value": f"{total_bp_value:,.2f}"},
        {"label": "Month Columns", "value": f"{len(month_columns):,.0f}"},
    ]


def build_reqd_mc_kpis(dataframe: pd.DataFrame) -> list[dict[str, str]]:
    total_machines = dataframe["Machine"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().nunique()
    available_mc = _numeric_sum(dataframe, "Available_MC")
    required_mc = _numeric_sum(dataframe, "Reqd_MC")

    return [
        {"label": "Total Machines", "value": f"{total_machines:,.0f}"},
        {"label": "Available Machines", "value": f"{available_mc:,.2f}"},
        {"label": "Required Machines", "value": f"{required_mc:,.2f}"},
    ]
