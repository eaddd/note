# 滑动操作
from appium import webdriver


class Slide:

    def __init__(self, driver):
        self.driver = driver

    # 获取屏幕大小
    def get_screen_size(self):
        return self.driver.get_window_size(self)

    # 上滑
    def swipe_up(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.5
        y1 = screen_size['height'] * 0.75
        y2 = screen_size['height'] * 0.25
        self.driver.swipe(x1, y1, x1, y2, t)

    # 下滑
    def swipe_down(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.5
        y1 = screen_size['height'] * 0.25
        y2 = screen_size['height'] * 0.75
        self.driver.swipe(x1, y1, x1, y2, t)

    # 左滑
    def swipe_left(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.75
        y1 = screen_size['height'] * 0.5
        x2 = screen_size['width'] * 0.25
        self.driver.swipe(x1, y1, x2, y1, t)

    # 右滑
    def swipe_right(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.25
        y1 = screen_size['height'] * 0.5
        x2 = screen_size['width'] * 0.75
        self.driver.swipe(x1, y1, x2, y1, t)
