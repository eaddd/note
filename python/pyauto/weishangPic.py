import psutil
import pywinauto
from pywinauto.application import Application

PID =0
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid','name'])
    except psutil.NoSuchProcess:
        pass
    else:
        if'WeChat.exe'== pinfo['name']:
            PID = pinfo['pid']

app =Application(backend='uia').connect(process=PID)

win = app['微信']
win.set_focus()
win.draw_outline()

pyq_btn = win.child_window(title="朋友圈", control_type="Button")
pyq_btn.print_control_identifiers()
element_position = pyq_btn.rectangle()
center_position = (int((element_position.left + element_position.right) / 2),
                           int((element_position.top + element_position.bottom) / 2))
pywinauto.mouse.click(button='left', coords=center_position)
