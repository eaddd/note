# coding=utf-8

import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from slide import Slide as Slide
import time
import logging
log = logging.getLogger(__name__)

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='127.0.0.1:62001',
    appPackage='com.truedian.dragon',
    appActivity='.activity.fragment.MainActivity',
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
        self.wait = WebDriverWait(self.driver, 30)
        self.slide = Slide(self.driver)

    def tearDown(self) -> None:
        try:
            self.rm_downloadFile
        except Exception as e:
            pass
        if self.driver:
            self.driver.quit()

    def test_download_wego(self) -> None:
        start_text = "第1⃣️7⃣️款：亏本清🉐️39.9元"
        end_text = "本场更新结束"

        # 界面打开好友并查找进入要转发的好友店铺
        self.open_wegohaoyou()
        start_eles = None
        while True:
            self.wait.until(EC.presence_of_all_elements_located(
                (By.ID, "com.truedian.dragon:id/title_home_fragment")))
            self.slide.swipe_up(2500)
            eles = self.driver.find_elements(AppiumBy.ID,
                                             'com.truedian.dragon:id/title_home_fragment')  # 获取多个元素的值
            for ele in eles:
                if ele.text.startswith(start_text):
                    start_eles = ele
                    break
            if start_eles != None:
                break  # 中断while 循环
        # 点击下载按钮
        download_btn_xpath = '//*[contains(@text,"%s")]/following-sibling::android.view.ViewGroup/android.widget.TextView[@resource-id="com.truedian.dragon:id/download_home_fragment"]' % start_text
        try:
            download_eles = self.driver.find_element(
                AppiumBy.XPATH, download_btn_xpath)
            download_eles.click()
        except Exception as e:
            self.slide.swipe_up(2500)
            download_eles = self.driver.find_element(
                AppiumBy.XPATH, download_btn_xpath)
            download_eles.click()

        cancel_btn = self.wait.until(EC.element_to_be_clickable(
            (By.ID, 'com.truedian.dragon:id/tv_left_btn')))
        cancel_btn.click()

        # 启动微信
        self.driver.start_activity("com.tencent.mm", ".ui.LauncherUI")

        self.open_pengyouquan()
        self.send_pengyouquan()
        self.rm_downloadFile()

        # 切换微商相册
        self.driver.implicitly_wait(10)
        self.driver.activate_app("com.truedian.dragon")

        is_end = False
        while True:
            swipe_product_layout_xpath = '//*[contains(@text,"%s")]/../preceding-sibling::android.widget.RelativeLayout' % start_text
            product_layout = self.driver.find_elements(
                AppiumBy.XPATH, swipe_product_layout_xpath)
            size = len(product_layout) - 1
            for i in range(size, -1, -1):
                try:
                    product_text = product_layout[i].find_element(
                        AppiumBy.ID, "com.truedian.dragon:id/title_home_fragment")
                except Exception as e:
                    self.slide.swipe_down(2500)
                    self.wait.until(EC.presence_of_all_elements_located(
                        (AppiumBy.ID, "com.truedian.dragon:id/title_home_fragment")))
                    product_text = product_layout[i].find_element(
                        AppiumBy.ID, "com.truedian.dragon:id/title_home_fragment")

                log.info("产品:" + product_text.text)
                if product_text.text.startswith(end_text):
                    is_end = True
                product_download_btn = product_layout[i].find_element(
                    AppiumBy.ID, "com.truedian.dragon:id/download_home_fragment")
                product_download_btn.click()
                cancel_btn = self.wait.until(EC.element_to_be_clickable(
                    (By.ID, 'com.truedian.dragon:id/tv_left_btn')))
                cancel_btn.click()

                self.driver.activate_app("com.tencent.mm")
                self.send_pengyouquan()
                self.rm_downloadFile()

                self.driver.implicitly_wait(10)
                self.driver.activate_app("com.truedian.dragon")
                if is_end:
                    break
                if i == 0:
                    start_text = product_text.text[0:40]

            if is_end:
                break
            self.slide.swipe_down(2500)

    def rm_downloadFile(self) -> None:
        time.sleep(5)
        result = self.driver.execute_script('mobile: shell', {
            'command': 'rm -r',
            'args': ['/sdcard/DCIM/0wsxc/downloadFile'],
            'includeStderr': True,
            'timeout': 5000
        })
        print(result['stdout'])

    def open_pengyouquan(self) -> None:
        # 点击搜索
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/gsl")))
        search_btn.click()
        # 获取搜索框并输入
        search_input = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cd7')))
        search_input.send_keys("黑眼圈2号")
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
        try:
            moment_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/iwg")))
            moment_btn.click()
        except Exception as e:
            moment_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/iwg")))
            moment_btn.click()

    def send_pengyouquan(self) -> None:
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
        list_item = self.driver.find_elements(
            AppiumBy.ID, "com.tencent.mm:id/iwq")
        size = len(list_item)
        is_video = False
        for i in range(size):
            picture_checkbox = list_item[i].find_elements(
                AppiumBy.ID, 'com.tencent.mm:id/gpy')
            picture_size = len(picture_checkbox)
            if picture_size < 1:
                video_checkbox = list_item[i].find_elements(
                    AppiumBy.ID, 'com.tencent.mm:id/gqq')
                video_checkbox[0].click()
                is_video = True
                finish_btn = self.wait.until(EC.element_to_be_clickable((
                    AppiumBy.ID, 'com.tencent.mm:id/cco')))
                finish_btn.click()
            else:
                picture_checkbox[0].click()
        if is_video == False:
            finish_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/en")))
            finish_btn.click()
        publish_text = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/jsy")))
        product_text = self.driver.get_clipboard_text()
        publish_text.send_keys(product_text)

        # 设置谁可以看
        private_selector = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/icb")))
        private_selector.click()
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/far')))
        private_level_selector = self.driver.find_elements(
            AppiumBy.ID, 'com.tencent.mm:id/far')
        private_level_selector[0].click()
        publish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/en")))
        publish_btn.click()
        time.sleep(2)
        # 设置可见end

        # 发布
        publish_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/en")))
        publish_btn.click()

    def open_wegohaoyou(self) -> None:
        # 点击好友
        haoyou_btn = self.wait.until(EC.element_to_be_clickable(
            (By.ID, "com.truedian.dragon:id/focus_container")))
        haoyou_btn.click()
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@resource-id="container"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]')))
        search_btn.click()
        # 获取搜索框并输入
        for i in range(3):
            try:
                search_input = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//android.widget.EditText')))
                search_input.send_keys("A周圈圈")
                break
            except Exception as e:
                search_btn.click()
        search_btn.click()
        for i in range(10):
            try:
                touxiang_btn = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@resource-id="container"]/android.view.View[2]/android.view.View[2]')))
                touxiang_btn.click()
                break
            except Exception as e:
                search_btn.click()
                self.driver.implicitly_wait(3)


if __name__ == '__main__':
    unittest.main()
