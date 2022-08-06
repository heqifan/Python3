import PySimpleGUI as sg

# 窗口显示文本框和浏览按钮, 以便选择一个文件夹
dir_path = sg.popup_get_folder("Select Folder")
if not dir_path:
    sg.popup("Cancel", "No folder selected")
    raise SystemExit("Cancelling: no folder selected")
else:
    sg.popup("The folder you chose was", dir_path)


