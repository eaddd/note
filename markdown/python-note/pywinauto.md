# pywinauto笔记

## 一、环境安装

pip install pywinauto==

## 二、 环境检查

命令行中打开python解释器，运行以下代码，windows自带的记事本会被启动，若无报错，则证明pywinauto已安装成功。

```python
from pywinauto.application import Application

app = Application(backend="uia").start("notepad.exe")
```

## 三、PC端元素定位工具介绍及判断backend

1. Backend判断  
Pywinauto中backend有两种：win32和uia，默认为win32。可使用spy++和Inspect工具判断backend适合写哪种。例如：如果使用Inspect的UIA模式，可见的控件和属性更多的话，backend可选uia，反之，backend可选win32。

## 四、启动并创建一个实例对象

1. 启动
start()用于还没有启动软件的情况。timeout为超时参数（可选），若软件启动所需的时间较长可选timeout，默认超时时间为5s。
start(self, cmd_line, timeout=app_start_timeout)
示例：

    ```python
    app = Application(backend = ‘uia’).start(r"E:\Office\Office14\EXCEL.exe)
    ```

2. 连接
connect()用于连接已经启动的程序。连接一个已经运行的程序有以下几种方法：

    a)process：进程id

    ```python
    app = Application().connect(process=2341)
    ```

    b)handle：应用程序的窗口句柄

    ```python
    app = Application().connect(handle=0x010f0c)
    ```

    c)path：进程的执行路径（GetModuleFileNameEx 模块会查找进程的每一个路径并与我们传入的路径去做比较）

    ```python
    app = Application().connect(path=“D:\Office14\EXCEL.exe”)
    ```

    d)参数组合（传递给pywinauto.findwindows.find_elements()这个函数）

    ```python
    app = Application().connect(title_re=".*Notepad", class_name=“Notepad”)
    ```

    注：
    应用程序必须先准备就绪，才能使用connect()，当应用程序start()后没有超时和重连的机制。在pywinauto外再启动应用程序，需要sleep，等程序start

    process：应用程序的进程ID，例如app = Application().connect(process=2341)  
    handle:应用程序窗口的窗口句柄，例如，app = Application().connect(handle=0x010f0c)  
    path:进程的可执行文件的路径（GetModuleFileNameEx用于查找每个进程的路径并与传入的值进行比较），例如：app = Application().connect(path=r"c:\windows\system32\notepad.exe")  

    或者指定窗口的参数的任意组合，这些都被传递给pywinauto.findwindows.find_elements() 函数。 例如  

    ```python
    app = Application().connect(title_re=".*Notepad", class_name="Notepad") 
    ```

    注意: 在使用connect*()之前，应用程序必须准备好。 在start()之后找不到应用程序时没有超时或重试。 因此，如果您在pywinauto之外启动应用程序，则需要睡眠或编程等待循环以等待应用程序完全启动。

## 五、 窗口、对话框及控件元素定位方式

第一个必要的事情是确定哪种可访问性技术（pywinauto的backend）可以用于您的应用程序。

Windows上受支持的辅助功能技术列表

* Win32 API (backend="win32") - 现在的默认backend
  * MFC, VB6, VCL, 简单的WinForms控件和大多数旧的遗留应用程序
* MS UI Automation (backend="uia")
  * WinForms, WPF, Store apps, Qt5, 浏览器  
  
注意: Chrome在启动之前需要--force-renderer-accessibility cmd标志。 由于comtypes Python库限制，不支持自定义属性和控件。

### GUI对象检查/Spy工具 

* Spy++ 包含在MS Visual Studio发行版（甚至是Express或Community）中，可通过“开始”菜单访问。 它使用Win32 API。 这意味着如果Spy ++能够显示所有控件，那么“win32”`backend就是你需要的。 AutoIt Window Info工具是一种Spy ++克隆。

* Inspect.exe 是Microsoft创建的另一个很棒的工具。 它包含在Windows SDK中，因此可以在x64 Windows上的以下位置找到它：

    C:\Program Files (x86)\Windows Kits\<winver>\bin\x64

    将Inspect.exe切换到UIA mode（使用MS UI Automation）。 如果它可以显示比Spy ++更多的控件及其属性，那么可能是 "uia"backend是你的选择。

* py_inspect 是基于pywinauto的多后端间谍工具的原型。 在可用后端之间切换可以通过“win32”和“uia”后端向您显示层次结构的差异。 py \ _inspect是SWAPY的未来替代品，仅在pywinauto == 0.5.4出现时支持“win32”后端。 由于现代pywinauto 0.6.0+架构，py \ _insins的初始实现仅包含大约150行代码。
  
### 窗口

window方法将用于获得真实窗口或控件的匹配/搜索算法的信息。实际窗口查找由wrapper_object()方法执行。 它返回实际现有窗口/控件的一些包装器或引发ElementNotFoundError。但是Python可以隐藏这个wrapper_object()调用，这样你就可以在生产中拥有更紧凑的代码。 以下陈述完全相同：

```python
dlg_spec.wrapper_object().minimize() # 在调试时
dlg_spec.minimize() # 在生产环境中
```

* 属性解析
  1. 使用“最佳匹配”算法来查找拼写错误和小变化 best_match

    ```python
    app.UntitledNotepad
    # 相当于
    app.window(best_match='UntitledNotepad') 
    ```

    如何将“最佳匹配”金牌附加到控件上有几个原则。 因此，如果窗口规范接近其中一个名称，您将获得成功的名称匹配。

    (1). 按标题（窗口文字，名称）： app.Properties.OK.click()  
    (2). 按标题和控件类型： app.Properties.OKButton.click()  
    (3). 按控件类型和编号： app.Properties.Button3.click() (注意: Button0和Button1匹配相同的按钮，Button2是下一个，等等。)  
    (4). 按左上角标签和控件类型： app.OpenDialog.FileNameEdit.set_text("")  
    (5). 按控件类型和项目文本：app.Properties.TabControlSharing.select("General")  


```python
from pywinauto.application import Application
import time

app = Application().start('notepad.exe')
time.sleep(1)
app[' 无标题 - 记事本 '].menu_select("编辑(&E) -> 替换(&R)..")
time.sleep(1)
app['替换'].取消.click()

# 没有with_spaces 参数空格将不会被键入。请参阅SendKeys的这个方法的文档，因为它是SendKeys周围的薄包装。
app[' 无标题 - 记事本 '].Edit.type_keys("Hi from Python interactive prompt %s" % str(dir()), with_spaces = True)

app[' 无标题 - 记事本 '].menu_select('文件(&F) -> 退出(&X)')

# 在这时候不清楚“不保存”的按钮名就对app['记事本'] 使用print_control_identifiers()
app['记事本'].Button2.click()
```

## 如何指定应用程序的对话框

使用项目或属性访问权来根据其标题选择对话框  
dlg = app.Notepad   
或者等价于dlg = app['Notepad']   
dlg = app.window(title_re="Page Setup", class_name="#32770") 

## 如何在对话框上指定控件

## 如何将pywinauto与英语以外的应用程序语言一起使用

必须写app.window(title_re="非Ascii字符").window(title="非Ascii字符").click() 

## 等待长时间操作

GUI应用程序行为通常不稳定，您的脚本需要等待，直到出现新窗口或关闭/隐藏现有窗口。 pywinauto可以隐式地（默认超时）灵活地等待对话框初始化，或者明确地使用专用方法/函数来帮助您使代码更容易和更可靠。

### Application 方法

```python 
wait_cpu_usage_lower (new in pywinauto 0.5.2, renamed in 0.6.0)
app.wait_cpu_usage_lower(threshold=5) # 等到CPU使用率低于5％
```

此方法对于多线程接口很有用，当GUI响应且所有控件都已存在且似乎已准备好使用时，允许在另一个线程中进行延迟初始化。因此，等待特定窗口的存在/状态是无用的。在这种情况下，整个进程的CPU使用率表示任务计算尚未完成。
注意:此方法仅适用于整个应用程序进程，不适用于窗口/元素。

### WindowSpecification 方法

These methods are available to all controls.

* wait
* wait_not

WindowSpecification对象不一定与现有窗口/控件相关。 这只是一个描述，即搜索窗口的几个标准。 wait方法（如果没有引发任何异常）可以保证目标控件存在，甚至可见，启用和/或激活。

### timings模块中的函数

还有一些对任何Python代码都有用的低级方法。

* wait_until
* wait_until_passes
如果每个函数调用都应该有时序控制，也可以使用装饰器pywinauto.timings.always_wait_until()和pywinauto.timings.always_wait_until_passes()

```python
# call ensure_text_changed(ctrl) every 2 sec until it's passed or timeout (4 sec) is expired

@always_wait_until_passes(4, 2)
def ensure_text_changed(ctrl):
    if previous_text == ctrl.window_text():
        raise ValueError('The ctrl text remains the same while change is expected')
```

### Global timings for all actions

许多动作需要在之前，之后和之间暂停。 模块timings中有几个全局常量定义了这种暂停。 通过在对象timings.Timings中设置全局静态变量，它可以单独根据您的需要进行调整。

所有全局计时可以一次设置为默认值，或者加倍，或者除以2：

```python
from timings import Timings

Timings.defaults()
Timings.slow() # double all timings (~2x slower script execution)
Timings.fast() # divide all timings by two (~2x faster)
```

## 基本用户输入模块

### pywinauto.mouse跨平台模块模拟真实用户的鼠标事件

pywinauto.mouse.click(button='left', coords=(0, 0))

单击指定的坐标

pywinauto.mouse.double_click(button='left', coords=(0, 0))

双击指定的坐标

pywinauto.mouse.move(coords=(0, 0))

移动鼠标

pywinauto.mouse.press(button='left', coords=(0, 0))

按下鼠标按钮

pywinauto.mouse.release(button='left', coords=(0, 0))

释放鼠标按钮

pywinauto.mouse.right_click(coords=(0, 0))

右键单击指定的坐标

pywinauto.mouse.scroll(coords=(0, 0), wheel_dist=1)

滚动鼠标滚轮

pywinauto.mouse.wheel_click(coords=(0, 0))

鼠标中键单击指定的坐标

### pywinauto.keyboard

键盘输入仿真模块

通过调用send_keys方法自动键入键或单个键操作（即按住，释放）到活动窗口。

您可以使用任何Unicode字符（在Windows上）和下面列出的一些特殊键。 该模块也可在Linux上使用。

可用的按键代码:

{SCROLLLOCK}, {VK_SPACE}, {VK_LSHIFT}, {VK_PAUSE}, {VK_MODECHANGE},
{BACK}, {VK_HOME}, {F23}, {F22}, {F21}, {F20}, {VK_HANGEUL}, {VK_KANJI},
{VK_RIGHT}, {BS}, {HOME}, {VK_F4}, {VK_ACCEPT}, {VK_F18}, {VK_SNAPSHOT},
{VK_PA1}, {VK_NONAME}, {VK_LCONTROL}, {ZOOM}, {VK_ATTN}, {VK_F10}, {VK_F22},
{VK_F23}, {VK_F20}, {VK_F21}, {VK_SCROLL}, {TAB}, {VK_F11}, {VK_END},
{LEFT}, {VK_UP}, {NUMLOCK}, {VK_APPS}, {PGUP}, {VK_F8}, {VK_CONTROL},
{VK_LEFT}, {PRTSC}, {VK_NUMPAD4}, {CAPSLOCK}, {VK_CONVERT}, {VK_PROCESSKEY},
{ENTER}, {VK_SEPARATOR}, {VK_RWIN}, {VK_LMENU}, {VK_NEXT}, {F1}, {F2},
{F3}, {F4}, {F5}, {F6}, {F7}, {F8}, {F9}, {VK_ADD}, {VK_RCONTROL},
{VK_RETURN}, {BREAK}, {VK_NUMPAD9}, {VK_NUMPAD8}, {RWIN}, {VK_KANA},
{PGDN}, {VK_NUMPAD3}, {DEL}, {VK_NUMPAD1}, {VK_NUMPAD0}, {VK_NUMPAD7},
{VK_NUMPAD6}, {VK_NUMPAD5}, {DELETE}, {VK_PRIOR}, {VK_SUBTRACT}, {HELP},
{VK_PRINT}, {VK_BACK}, {CAP}, {VK_RBUTTON}, {VK_RSHIFT}, {VK_LWIN}, {DOWN},
{VK_HELP}, {VK_NONCONVERT}, {BACKSPACE}, {VK_SELECT}, {VK_TAB}, {VK_HANJA},
{VK_NUMPAD2}, {INSERT}, {VK_F9}, {VK_DECIMAL}, {VK_FINAL}, {VK_EXSEL},
{RMENU}, {VK_F3}, {VK_F2}, {VK_F1}, {VK_F7}, {VK_F6}, {VK_F5}, {VK_CRSEL},
{VK_SHIFT}, {VK_EREOF}, {VK_CANCEL}, {VK_DELETE}, {VK_HANGUL}, {VK_MBUTTON},
{VK_NUMLOCK}, {VK_CLEAR}, {END}, {VK_MENU}, {SPACE}, {BKSP}, {VK_INSERT},
{F18}, {F19}, {ESC}, {VK_MULTIPLY}, {F12}, {F13}, {F10}, {F11}, {F16},
{F17}, {F14}, {F15}, {F24}, {RIGHT}, {VK_F24}, {VK_CAPITAL}, {VK_LBUTTON},
{VK_OEM_CLEAR}, {VK_ESCAPE}, {UP}, {VK_DIVIDE}, {INS}, {VK_JUNJA},
{VK_F19}, {VK_EXECUTE}, {VK_PLAY}, {VK_RMENU}, {VK_F13}, {VK_F12}, {LWIN},
{VK_DOWN}, {VK_F17}, {VK_F16}, {VK_F15}, {VK_F14} 
修饰符:

'+': {VK_SHIFT}
'^': {VK_CONTROL}
'%': {VK_MENU} a.k.a. Alt键
示例如何使用修饰符:

send_keys('^a^c') # 全选（Ctrl + A）并复制到剪贴板（Ctrl + C）
send_keys('+{INS}') # 从剪贴板插入（Shift + Ins）
send_keys('%{F4}') # 使用Alt + F4关闭活动窗口 
可以为特殊键指定重复计数。 {ENTER 2}表示按两次Enter键。

示例显示如何按住或释放键盘上的按键:

send_keys("{VK_SHIFT down}"
          "pywinauto"
          "{VK_SHIFT up}") # to type PYWINAUTO

send_keys("{h down}"
          "{e down}"
          "{h up}"
          "{e up}"
          "llo") # to type hello 
使用花括号来转义修饰符并将保留符号键入为单个键:

send_keys('{^}a{^}c{%}') # 键入字符串 "^a^c%" (不会按下Ctrl键)
send_keys('{{}ENTER{}}') # 键入字符串“{ENTER}”而不按Enter键 