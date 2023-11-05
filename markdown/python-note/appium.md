# appium 笔记


## 安装

1. 安装JDK

    下载解压文件夹安装。并且设置 Java 环境变量,右键点击我的电脑--属性--高级--环境变量,新建系统变量JAVA_HOME和CLASSPATH  
             变量名：JAVA_HOME  
             变量值：C:\Program Files (x86)\Java\jdk 1.7.0_01  
             变量名：Path  
             变量值：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;  
             变量名：CLASSPATH  
             变量值：;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;

2. AndroidSDK下载及安装 *<https://blog.csdn.net/xiaoxiaoTeddy/article/details/130817310>*

3. 一、appium服务端下载：  
    <https://github.com/appium/appium-desktop/releases?page=5>  
    appium-desktop-Setup-1.6.2.exe  

    安装appium2 

    ```sh

    npm i --location=global appium

    appium driver install uiautomator2

    ```

    问题1:  Error installing Chromedriver: unable to verify the first certificate  
    解决: 设置环境变量 set APPIUM_SKIP_CHROMEDRIVER_INSTALL=1 

    二、安装Appium-python库  
    pip install Appium-Python-Client
4. 安装夜神模拟器

## 连接android sdk,appuim, 夜神模拟器

1. 夜神模拟器打开开发者选项， 打开usb调试
2. 将Android SDK安装目录的platform-tools文件夹下adb.exe文件复制一份出来，复制到夜神模拟器的安装目录bin目录下覆盖里面的nox_adb.exe，因为夜神模拟器目录下原本的adb文件名字叫做nox_adb.exe，因此复制过去之后也得改名为nox_adb.exe。
3. 

### adb命令

```sh

adb kill-server # 停止adb服务

adb start-server # 启动adb服务

adb connect 127.0.0.1:62001 # 连接到夜神模拟器

adb devices  # 查看设备

adb shell # 打开设备终端

dumpsys activity | grep mFocusedActivity # 获取当前打开app的包名和启动页面名称

adb shell getprop ro.build.version.release # 获取手机版本
```

## 元素定位工具

### uiautomatorviewer

1、在SDK的安装目录tools下双击uiautomatorviewer.bat启动  
uiautomatorviewer工具使用前提  
打开uiautomatorviewer工具  
所测试设备是开机状态（手机或者模拟器）  
确保电脑与设备是链接状态，也就是
cmd进入命令行终端，  
输入adb connect 127.0.0.1:62001链接夜神模拟器，
输入adb devices能够获取设备名称。

### Appium Inspector

### weditor

```sh
pip  install -U weditor # uiautomator , facebook-wda会被作为依赖一并安装

python -m weditor 启动weditor
```

- 命令执行成功后会自动调用浏览器打开地址<http://localhost:17310/>
- 选择目标设备Android
- 输入命令查看android设备UUID：adb devices
- 在WEditor界面输入设备UUID
- 点击Connect，连接成功
- 点击dump hierarchy
  
问题：nicodeDecodeError: 'gbk' codec can't decode byte 0xad in position 645: illegal multibyte sequence

set PYTHONUTF8=1 再执行pip安装


## 元素定位

1. 通过resourceId属性定位 find_element_by_id返回是WebElement对象 element_to_be_clickable((By.ID, "com.tencent.mm:id/iq"))
2. 通过文本定位 find_element_by_android_uiautomator() 调用系统自带框架实现元素定位uiautomator实现元素定位, 基于java类UiSelector, new一个UiSelector
   组合定位 find_element_by_android_uiautomator('new UiSelector().text("").resourceId("")'), driver.find_element('-android uiautomator','new UiSelector().text("全部")')
3. 通过content-desc/description属性实现元素定位find_element_by_accessibility_id("")
4. 通过xpath定位 driver.find_element(By.XPATH,'')

## 元素的操作

1. app四大常用元素操作 click() send_keys() get_attibute() text()
2. 滑屏swipe(self,start_x,start_y,end_x,end_y,duration=None):从A点滑动至B点，滑动时间为毫秒，A点的坐标为start_x,start_y，B点的坐标为end_x,end_y
    下滑操作：

    ```python
     x=driver.get_window_size()['width']
     y=driver.get_window_size()['height']
      driver.swipe(x/2,y/2,x/2,y/4,0) #上滑相反坐标即可（采用绝对坐标）
    ```

   多点触控、
   长按 


## 等待

appium三种等待方式：

- 强制等待
- 隐式等待
- 显式等待

三种等待方式之间的区别：

 1、强制等待

使用方式：time.sleep()

强制执行对应的等待时间后，才能执行下面的操作语句，影响脚本运行的速度，一般不推荐

  2、隐式等待

使用方式：driver.imolicitly_wait()

相对于强制等待来讲，较智能。设置隐式等待不影响下面脚本的执行，当元素可以被定位到，则继续执行；如果超过时长还没有定位到，则会抛出异常

隐式等待是全局的，设置时间不宜过长。当元素处于不可交互的状态时就会触发隐式等待，多次设置的话后一次会覆盖前一次。

这种方法也存在一个弊端，就是程序会一直等到整个页面加载完成才会继续执行下一步，比如某些时候想要的页面元素早就加载完了，但是由于个别JS等资源加载稍慢，此时程序仍然等待全部页面加载完成后才会继续执行下一步，无形中加长了测试用例的执行时间

3、显示等待

使用方式：

```python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
 
WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable(element))
```

显式等待使用前需要先定义元素，设置显式等待，直到某个元素可以被定位条件成立后，则不再等待，继续执行下面的操作。

总结：

1、一般不推荐强制等待，页面确实没有定位的元素，再使用该方式更合理一些

2、显示等待和隐式等待相对来讲更智能

3、根据不同的应用场景使用不同的等待方式


## 开发笔记

1. 怎么获取多个相同的元素，遍历
   使用find_elements

    ```python
    pictures = self.driver.find_elements(AppiumBy.ID, "com.tencent.mm:id/iwq")
    size = len(pictures)
    for i in range(size):
        print (pictures[i])
    ```

2. 滑动窗口，根据文本查找对象

    ```python
    
    ```