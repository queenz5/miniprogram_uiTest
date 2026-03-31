import pytest
from initDriver import driver_util
from utils.base import Base
from utils.pytesseract_util import *
from utils.assertUtil import AssertionUtil


class Test_example:
    @classmethod
    def setup_class(self):
        self.driver_util = driver_util()
        self.driver = self.driver_util.init_android_driver()
        self.base = Base(self.driver)
        self.assertionUtil = AssertionUtil(self.driver)

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

    def setup_method(self):
        # 每个用例执行前会执行的方法
        pass

    def test_example(self):
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = '/pages/component/view/view?query1=abc&query2=def')
        time.sleep(2)


        # 通过文字识别点击示例：
        # result_text = self.base.find_text(self.driver,"打开小程序",lang="ch",wait_time=3,target_text_index=1)
        # print(result_text)
        # self.base.tap_coordinates(result_text["target_coords"])
        #断言文字是否在当前屏幕出现
        # self.assertionUtil.check_text_exist(self.driver,"小程序",lang="ch",target_text_index=2,wait_time=1,expect=True,fail_msg="“小程序”文案没有出现在当前屏幕")

        # 断言图片是否在当前屏幕出现
        # self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/example/tpl1758530632434.png",resolution=(1080, 2120),position=5,rgb=False, wait_time=1,expect=True, fail_msg="目标图片没出现")

        # 通过图片识别点击示例：
        # result_image = self.base.find_image(self.driver, template_path="testCase/android/example/tpl1758530632434.png",resolution=(1080, 2120),position=5,rgb=False, wait_time=1)
        # print(result_image)
        # self.base.tap_coordinates(result_image["target_coords"])


        # 根据 xpath 查找元素
        # button = self.base.find_element_by_xpath("//android.widget.Button[@resource-id='com.finogeeks.finosprite:id/btnConfigSDK']")
        # self.base.click_element(button)

        #通过坐标滚动
        # self.base.swipe_between_points((200,500),(200,100))

        # 从某个元素滚动到指定坐标
        # button1 = self.base.find_element_by_xpath("//android.widget.Button[@resource-id='com.finogeeks.finosprite:id/btnConfigSDK']")
        # self.base.swipe_from_element_to_coordinates(button1,(200,100))

        # 从某个坐标滚动到指定元素
        # button1 = self.base.find_element_by_xpath("//android.widget.Button[@resource-id='com.finogeeks.finosprite:id/btnConfigSDK']")
        # self.base.swipe_from_coordinates_to_element((200,1000),button1)

        # 从一个元素滚动到另一个元素
        # button1 = self.base.find_element_by_xpath("//android.widget.Button[@resource-id='com.finogeeks.finosprite:id/btnConfigSDK']")
        # button2 = self.base.find_element_by_xpath("//android.widget.Button[@resource-id='com.finogeeks.finosprite:id/btnComponentMulti']")
        # self.base.swipe_from_element_to_element(button2,button1)

        #侧滑返回
        # self.base.swipe_back()

        #回到桌面
        # self.base.go_to_home()

        # 关闭APP
        # self.base.close_app()
