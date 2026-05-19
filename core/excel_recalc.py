from __future__ import annotations

import platform
from pathlib import Path


def recalculate_workbook_with_excel(workbook_path: str | Path) -> tuple[bool, str]:
    selected_path = Path(workbook_path)

    if platform.system().lower() != "windows":
        return False, "Excel recalculation requires Windows with Microsoft Excel installed."

    try:
        import win32com.client  # type: ignore
    except ImportError:
        return False, "pywin32 is not installed. Run: pip install pywin32"

    excel = None
    workbook = None

    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(str(selected_path.resolve()))
        excel.CalculateFullRebuild()
        workbook.Save()
        workbook.Close(SaveChanges=True)
        excel.Quit()
        return True, "Excel recalculation completed successfully."
    except Exception as exc:
        try:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
        finally:
            if excel is not None:
                excel.Quit()
        return False, f"Excel recalculation failed: {exc}"
