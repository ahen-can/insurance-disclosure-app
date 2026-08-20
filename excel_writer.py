import openpyxl
from openpyxl.utils import get_column_letter
from config import SHEET_CONFIG


def get_or_add_fy_columns(ws, year: str, fields: list, data_start_col: int):
    """
    Row 1 = year label (merged across its fields)
    Row 2 = field subheadings
    Returns the starting column index for this year.
    If year already exists, returns its existing start column.
    """
    for col in range(data_start_col, ws.max_column + 1):
        if ws.cell(row=1, column=col).value == year:
            return col  # already exists

    start_col = data_start_col
    for col in range(data_start_col, ws.max_column + 2):
        if ws.cell(row=1, column=col).value is None:
            if ws.cell(row=2, column=col).value is None:
                start_col = col
                break

    ws.cell(row=1, column=start_col).value = year
    end_col = start_col + len(fields) - 1
    if end_col > start_col:
        ws.merge_cells(
            start_row=1, start_column=start_col,
            end_row=1, end_column=end_col
        )

    for i, field in enumerate(fields):
        ws.cell(row=2, column=start_col + i).value = field

    return start_col


def get_or_create_company_row(ws, insurer_name: str, data_start_row: int = 3):
    """Find existing row for insurer or create new one. Starts from row 3."""
    for row in range(data_start_row, ws.max_row + 2):
        val = ws.cell(row=row, column=1).value
        if val == insurer_name:
            return row
        if val is None:
            ws.cell(row=row, column=1).value = insurer_name
            return row


def write_flat_sheet(wb, sheet_name: str, data: dict,
                     insurer_name: str, year: str, fields: list):
    if sheet_name not in wb.sheetnames:
        return

    ws = wb[sheet_name]

    if ws.cell(row=1, column=1).value is None:
        ws.cell(row=1, column=1).value = "Company"

    start_col = get_or_add_fy_columns(ws, year, fields, data_start_col=2)
    company_row = get_or_create_company_row(ws, insurer_name, data_start_row=3)

    for i, field in enumerate(fields):
        col = start_col + i
        ws.cell(row=company_row, column=col).value = data.get(field)


def _get_or_add_company_block(ws, insurer_name: str, year: str, fields: list, data_start_col: int = 3):
    """
    Finds or creates an nested layout structure:
    Row 1: Company Name (Merged across all its distinct years)
    Row 2: Financial Year (Merged across its field metrics)
    Row 3: Field Subheadings
    """
    block_width = len(fields)
    
    company_start = None
    company_end = None
    
    col = data_start_col
    while col <= max(ws.max_column, data_start_col):
        val = ws.cell(row=1, column=col).value
        if val == insurer_name:
            company_start = col
            # Find where this company block ends by scanning merged or consecutive cells
            next_col = col
            while next_col <= max(ws.max_column, data_start_col):
                next_val = ws.cell(row=1, column=next_col).value
                # Stop if we hit a new company name
                if next_val is not None and next_val != insurer_name:
                    break
                next_col += 1
            company_end = next_col - 1
            break
        col += 1


    if company_start is not None:
        for col in range(company_start, company_end + 1):
            if ws.cell(row=2, column=col).value == year:
                return col  # Exact company + year combination found

        insert_col = company_end + 1
        
        ws.insert_cols(insert_col, amount=block_width)
        
        for merged_range in list(ws.merged_cells.ranges):
            if merged_range.min_row == 1 and merged_range.min_col == company_start:
                ws.unmerge_cells(str(merged_range))
                break
                
        ws.merge_cells(start_row=1, start_column=company_start, end_row=1, end_column=company_end + block_width)
        for c in range(company_start, company_end + block_width + 1):
            ws.cell(row=1, column=c).value = insurer_name
            
        ws.cell(row=2, column=insert_col).value = year
        if block_width > 1:
            ws.merge_cells(start_row=2, start_column=insert_col, end_row=2, end_column=insert_col + block_width - 1)
            
        for i, field in enumerate(fields):
            ws.cell(row=3, column=insert_col + i).value = field
            
        return insert_col

    start_col = data_start_col
    while True:
        if (ws.cell(row=1, column=start_col).value is None and 
            ws.cell(row=2, column=start_col).value is None and 
            ws.cell(row=3, column=start_col).value is None):
            break
        start_col += 1

    end_col = start_col + block_width - 1
    
    ws.cell(row=1, column=start_col).value = insurer_name
    ws.cell(row=2, column=start_col).value = year
    
    if end_col > start_col:
        ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
        ws.merge_cells(start_row=2, start_column=start_col, end_row=2, end_column=end_col)

    for i, field in enumerate(fields):
        ws.cell(row=3, column=start_col + i).value = field

    return start_col

def update_excel(results: dict, excel_path: str, wb=None):
    if wb is None:
        wb = openpyxl.load_workbook(excel_path)
    
    flat_sheets = {
        "L2": "L2", "L3": "L3", "L4": "L4", "L5": "L5", "L6": "L6", "L7": "L7",
        "L9": "L9", "L22": "L22", "L37": "L37", "L38": "L38",
        "L39_individual": "L39_Individual", "L39_group": "L39_Group", "L41": "L41", "L45": "L45"
    }

    for insurer_name, result in results.items():
        if result["status"] != "success":
            continue

        data = result["data"]
        year = data.get("year", "FY23")

        for data_key, sheet_name in flat_sheets.items():
            if data_key in data and data_key in SHEET_CONFIG:
                write_flat_sheet(wb, sheet_name, data[data_key], insurer_name, year, SHEET_CONFIG[data_key])

        if "L25_individual" in data:
            write_l25_individual(wb, data["L25_individual"], insurer_name, year)

        if "L25_group" in data:
            write_l25_group(wb, data["L25_group"], insurer_name, year)

    wb.save(excel_path)


def _ensure_state_rows(ws, sno_col=1, state_col=2, header_row=3):
    """
    Writes S.No in col A and State/UT (+ Total row) in col B,
    starting from row 4. Only writes once (skips if already present).
    """
    if ws.cell(row=header_row, column=sno_col).value is None:
        ws.cell(row=header_row, column=sno_col).value = "S.No"
    if ws.cell(row=header_row, column=state_col).value is None:
        ws.cell(row=header_row, column=state_col).value = "State / UT"

    start_row = header_row + 1

    if ws.cell(row=start_row, column=state_col).value is not None:
        return  # already populated

    for idx, state in enumerate(STATE_ORDER, start=1):
        row = start_row + idx - 1
        ws.cell(row=row, column=sno_col).value = idx
        ws.cell(row=row, column=state_col).value = state

    total_row = start_row + len(STATE_ORDER)
    ws.cell(row=total_row, column=sno_col).value = ""
    ws.cell(row=total_row, column=state_col).value = "Total"

def update_excel(results: dict, excel_path: str):
    wb = openpyxl.load_workbook(excel_path)

    flat_sheets = {
        "L2": "L2",
        "L3": "L3",
        "L4": "L4",
        "L5": "L5",
        "L6": "L6",
        "L7": "L7",
        "L9": "L9",
        "L22": "L22",
        "L37": "L37",
        "L38": "L38",
        "L39_individual": "L39_Individual",
        "L39_group": "L39_Group",
        "L41": "L41",
        "L45": "L45"
    }

    for insurer_name, result in results.items():
        if result["status"] != "success":
            continue

        data = result["data"]
        year = data.get("year", "FY23")

        for data_key, sheet_name in flat_sheets.items():
            if data_key in data and data_key in SHEET_CONFIG:
                write_flat_sheet(
                    wb, sheet_name,
                    data[data_key],
                    insurer_name,
                    year,
                    SHEET_CONFIG[data_key]
                )

    wb.save(excel_path)
