"""Reading the finished workbook back out for on-screen display.

The copy view is built from the written workbook rather than from the extracted
JSON, so what you copy is exactly what the download would contain: same sheets,
same column order, same values.
"""

import openpyxl

MAX_HEADER_ROWS = 2      # the templates use "Company / FY" then the field names


def read_workbook(path):
    """[(sheet_name, headers, [row, ...]), ...] with empty sheets dropped."""
    workbook = openpyxl.load_workbook(path, data_only=True)
    out = []
    for name in workbook.sheetnames:
        worksheet = workbook[name]
        rows = [list(r) for r in worksheet.iter_rows(values_only=True)]
        rows = [r for r in rows if any(c is not None and str(c).strip() for c in r)]
        if len(rows) <= MAX_HEADER_ROWS:
            continue                      # header-only sheet, nothing extracted
        headers = _headers(rows)
        data = rows[MAX_HEADER_ROWS:]
        if data:
            out.append((name, headers, data))
    return out


def _headers(rows):
    """The field-name row, falling back to the first row."""
    candidate = rows[1] if len(rows) > 1 else rows[0]
    if not any(candidate):
        candidate = rows[0]
    return ["" if c is None else str(c) for c in candidate]


def to_tsv(row):
    """One row as tab-separated text, ready to paste across Excel columns."""
    cells = []
    for value in row:
        if value is None:
            cells.append("")
        elif isinstance(value, float) and value.is_integer():
            cells.append(str(int(value)))
        else:
            cells.append(str(value))
    return "\t".join(cells).rstrip("\t")
