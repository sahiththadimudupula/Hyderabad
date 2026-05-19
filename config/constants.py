APP_TITLE = "Hyderabad Manpower Engine"

INPUT_WORKBOOK_PATH = "input/Hyderabad.xlsx"
WORKING_DIRECTORY = "working"
WORKING_WORKBOOK_FILENAME = "Hyderabad_live.xlsx"
OUTPUT_DIRECTORY = "output"

MASTER_SHEET_NAME = "Hyderabad"
BP_SHEET_NAME = "BP_Structured"
REQD_MC_SHEET_NAME = "Reqd_MC"

APP_TABS = [
    "Flooring Manpower",
    "BP Structured",
    "Required Machines",
    "Final Master Sheet",
]

VISIBLE_COMPACT_COLUMNS = [
    "Section",
    "Dept_Machine_Name",
    "Designation",
    "BE_Final_Manpower",
]

MANPOWER_EDITABLE_COLUMNS = [
    "BE_Final_Manpower",
    "General_Shift",
    "Shift_A",
    "Shift_B",
    "Shift_C",
    "Reliever",
    "Remarks",
]

BP_READ_ONLY_COLUMNS = ["Section", "Machine"]
REQD_MC_EDITABLE_COLUMNS = ["Total Capacity/Day", "Available_MC"]

SUMMARY_COLUMNS = ["Section", "Machine_Count", "BE_Final_Manpower"]
HIDDEN_SYSTEM_COLUMNS = ["__excel_row_number", "__row_order", "__row_key"]

DEFAULT_DECIMAL_PLACES = 2
DATA_EDITOR_HEIGHT = 430
SUMMARY_TABLE_HEIGHT = 280
COMPACT_TABLE_HEIGHT = 240
FINAL_TABLE_HEIGHT = 680
DRIVER_TABLE_HEIGHT = 560

SUCCESS_STATUS = "Frozen"
PENDING_STATUS = "Draft"
TOTAL_LABEL = "Total"
