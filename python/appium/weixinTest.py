import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='127.0.0.1:62001',
    appPackage='com.tencent.mm',
    appActivity='.ui.LauncherUI',
    # appPackage='com.android.settings',
    # appActivity='.Settings',
    platformVersion="7.1.2",
    noReset=True
)

appium_server_url = 'http://localhost:4723/wd/hub'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 3)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_send_pengyouquan(self) -> None:
        # 点击搜索
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/gsl")))
        search_btn.click()
        # 获取搜索框并输入
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cd7')))
        search_input.send_keys("小易")
        # 点击头像进入
        touxiang_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/a27")))
        touxiang_btn.click()
        # 点击右上角...进入
        menu_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/eo")))
        menu_btn.click()
        # 再点击头像
        icon_btn = self.wait.until(EC.element_to_be_clickable(
            (By.ID, "com.tencent.mm:id/iwc")))
        icon_btn.click()
        # 点击朋友圈
        self.driver.implicitly_wait(2)
        moment_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/iwg")))
        moment_btn.click()
        send_pengyouquan_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/kex")))
        send_pengyouquan_btn.click()
        try:
            open_picture_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@resource-id="com.tencent.mm:id/ahh"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]')))
            open_picture_btn.click()
            permission_allow_button = self.wait.until(EC.element_to_be_clickable(
                (By.ID, "com.android.packageinstaller:id/permission_allow_button")))
            permission_allow_button.click()
        except Exception as e:
            pass
        self.wait.until(EC.element_to_be_clickable(
            (By.ID, "com.tencent.mm:id/iwq")))
        pictures = self.driver.find_elements(
            AppiumBy.ID, "com.tencent.mm:id/iwq")
        size = len(pictures)
        for i in range(size):
            picture_checkbox = pictures[i].find_elements(
                AppiumBy.ID, 'com.tencent.mm:id/gpy')
            picture_checkbox[0].click()
        finish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/en")))
        finish_btn.click()
        publish_text = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/jsy")))
        publish_text.send_keys("✅Mc抽绳裂口破洞牛仔裤：26-30码当下主流款，拯救无感穿搭，一条设计感牛仔裤就足够了！")
        publish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/en")))
        publish_btn.click()


if __name__ == '__main__':
    unittest.main()
