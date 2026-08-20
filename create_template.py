import openpyxl

wb = openpyxl.Workbook()

# Remove default sheet
wb.remove(wb.active)

# Create all required sheets
sheets = [
    "L2", "L3", "L4", "L5", "L6", "L7",
    "L9", "L22",
    "L37", "L38",
    "L39_Individual", "L39_Group",
    "L41", "L45"
]

for sheet in sheets:
    wb.create_sheet(sheet)

wb.save("insurance_data.xlsx")
print("Template created: insurance_data.xlsx")
