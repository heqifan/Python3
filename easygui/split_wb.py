from pathlib import Path
import PySimpleGUI as sg
import xlwings as xw

# 选择输入文件夹
INPUT_DIR = sg.popup_get_folder("Select an input folder")
if not INPUT_DIR:
    sg.popup("Cancel", "No folder selected")
    raise SystemExit("Cancelling: no folder selected")
else:
    INPUT_DIR = Path(INPUT_DIR)

# 选择输出文件夹
OUTPUT_DIR = sg.popup_get_folder("Select an output folder")
if not OUTPUT_DIR:
    sg.popup("Cancel", "No folder selected")
    raise SystemExit("Cancelling: no folder selected")
else:
    OUTPUT_DIR = Path(OUTPUT_DIR)

# 获取输入文件夹中所有xls格式文件的路径列表
files = list(INPUT_DIR.rglob("*.xls*"))

with xw.App(visible=False) as app:
    for index, file in enumerate(files):
        # 显示进度
        sg.one_line_progress_meter("Current Progress", index + 1, len(files))
        wb = app.books.open(file)
        # 提取sheet表为单独的Excel表格
        for sheet in wb.sheets:
            wb_new = app.books.add()
            sheet.copy(after=wb_new.sheets[0])
            wb_new.sheets[0].delete()
            wb_new.save(OUTPUT_DIR / f"{file.stem}_{sheet.name}.xlsx")
            wb_new.close()

sg.popup_ok("Task done!")