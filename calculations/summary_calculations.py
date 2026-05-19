from __future__ import annotations

import pandas as pd

from core.totals import append_total_row


def build_manpower_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=["Section", "Machine_Count", "BE_Final_Manpower"])

    grouped_rows: list[dict[str, object]] = []
    for section_name, section_dataframe in dataframe.groupby("Section", sort=False):
        machine_count = pd.to_numeric(section_dataframe["Machine_Count"], errors="coerce").fillna(0).sum()
        final_manpower = pd.to_numeric(section_dataframe["BE_Final_Manpower"], errors="coerce").fillna(0).sum()

        grouped_rows.append(
            {
                "Section": section_name,
                "Machine_Count": machine_count,
                "BE_Final_Manpower": final_manpower,
            }
        )

    summary_dataframe = pd.DataFrame(grouped_rows)
    return append_total_row(summary_dataframe, label_column="Section")
