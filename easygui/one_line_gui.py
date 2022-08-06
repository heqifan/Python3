import PySimpleGUI as sg

# # 窗口显示文本框和浏览按钮, 以便选择一个文件夹
# dir_path = sg.popup_get_folder("Select Folder")
# if not dir_path:
#     sg.popup("Cancel", "No folder selected")
#     raise SystemExit("Cancelling: no folder selected")
# else:
#     sg.popup("The folder you chose was", dir_path)


# # 窗口显示文本框和浏览按钮, 以便选择文件
# fname = sg.popup_get_file("Choose Excel file", multiple_files=True, file_types=(("Excel Files", "*.xls*"),),)
# if not fname:
#     sg.popup("Cancel", "No filename supplied")
#     raise SystemExit("Cancelling: no filename supplied")
# else:
#     sg.popup("The filename you chose was", fname)


# 显示一个日历窗口, 通过用户的选择, 返回一个元组(月, 日, 年)
# date = sg.popup_get_date()
# if not date:
#     sg.popup("Cancel", "No date picked")
#     raise SystemExit("Cancelling: no date picked")
# else:
#     sg.popup("The date you chose was", date)


# 显示文本输入框, 输入文本信息, 返回输入的文本, 如果取消则返回None
# text = sg.popup_get_text("Please enter a text:")
# if not text:
#     sg.popup("Cancel", "No text was entered")
#     raise SystemExit("Cancelling: no text entered")
# else:
#     sg.popup("You have entered", text)


# 显示一个弹窗, 但没有任何按钮
# sg.popup_no_buttons("You cannot click any buttons")


# 显示一个没有标题栏的弹窗
# sg.popup_no_titlebar("A very simple popup")


# 显示弹窗且只有OK按钮
# sg.popup_ok("You can only click on 'OK'")


# 显示弹窗且只有error按钮, 按钮带颜色
# sg.popup_error("Something went wrong")


# 显示一个“通知窗口”, 通常在屏幕的右下角, 窗口会慢慢淡入淡出
# sg.popup_notify("Task done!")


# 显示弹窗以及是和否按钮, 选择判断
# answer = sg.popup_yes_no("Do you like this video?")
# sg.popup("You have selected", answer)


# 自定义创建弹窗, 一行代码完成
choice, _ = sg.Window(
    "Continue?",
    [[sg.T("Do you want to subscribe to this channel?")], [sg.Yes(s=10), sg.No(s=10), sg.Button('Maybe', s=10)]],
    disable_close=True,
).read(close=True)
sg.popup("Your choice was", choice)
