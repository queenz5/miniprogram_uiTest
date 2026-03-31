import pytest
from initDriver import driver_util
from utils.base import Base
from utils.pytesseract_util import *
from utils.assertUtil import AssertionUtil


class Test_image:
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

    def test_image(self):
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = '/pages/component/image/image')
        testCaseDescription = "测试用例：\n\
        case1:image组件，mode为空，src传网络图片样式检测\n\
        case2:image组件，mode为空，src传本地图片样式检测\n\
        case3:image组件，mode为scaleToFill，image组件样式测试不保持纵横比缩放图片，使图片完全适应\n\
        case4:image组件，mode为aspectFit，image组件样式测试保持纵横比缩放图片，使图片的长边能完全显示出来\n\
        case5:image组件，mode为aspectFill，image组件样式测试保持纵横比缩放图片，只保证图片的短边能完全显示出来\n\
        case6:image组件，mode为top，image组件样式测试不缩放图片，只显示图片的顶部区域\n\
        case7:image组件，mode为bottom，image组件样式测试不缩放图片，只显示图片的底部区域\n\
        case8:image组件，mode为left，image组件样式测试不缩放图片，只显示图片的左边区域\n\
        case9:image组件，mode为right，image组件样式测试不缩放图片，只显示图片的右边边区域\n\
        case10:image组件，mode为top left，image组件样式测试不缩放图片，只显示图片的左上边区域\n\
        case11:image组件，mode为top right，image组件样式测试不缩放图片，只显示图片的右上边区域\n\
        case12:image组件，mode为bottom left，image组件样式测试不缩放图片，只显示图片的左下边区域\n\
        case13:image组件，mode为bottom right，image组件样式测试不缩放图片，只显示图片的右下边区域\n\
        "
        print(testCaseDescription)
        # 1.internet image
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931076703.png",resolution=(1080, 2400),wait_time=3,expect=True, fail_msg="断言：image组件，mode为空，src传网络图片样式检测。期望显示finclip logo图标")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 2.local image
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931310152.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为空，src传本地图片样式检测。期望显示WeChat图片")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 3.scale to fill
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931399880.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为scaleToFill，image组件样式测试不保持纵横比缩放图片，使图片完全适应。期望显示完整的小猫图片")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 4.aspect fit
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931399880.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为aspectFit，image组件样式测试保持纵横比缩放图片，使图片的长边能完全显示出来。期望显示完整的小猫图片")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 5.aspect fill
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931399880.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为aspectFill，image组件样式测试保持纵横比缩放图片，只保证图片的短边能完全显示出来")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 6.top
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760931948228.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为top，image组件样式测试不缩放图片，只显示图片的顶部区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 7.bottom
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932054636.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为bottom，image组件样式测试不缩放图片，只显示图片的底部区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 8.center
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932244575.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为center,期望不缩放图片，只显示图片的中间区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 9.left
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932350572.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为left，image组件样式测试不缩放图片，只显示图片的左边区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 10.right
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932427763.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为right，image组件样式测试不缩放图片，只显示图片的右边边区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 11.top left
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932491991.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为top left，image组件样式测试不缩放图片，只显示图片的左上边区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 12.top right
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932560382.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为top right，image组件样式测试不缩放图片，只显示图片的右上边区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 13.bottom left
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932634119.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为bottom left，image组件样式测试不缩放图片，只显示图片的左下边区域")
        result_text = self.base.find_text(self.driver, "next", lang="en")
        self.base.tap_coordinates(result_text["target_coords"])
        # 14.bottom left
        self.assertionUtil.check_image_exist(self.driver, template_path="testCase/android/image/tpl1760932723703.png",resolution=(1080, 2400),wait_time=2,expect=True, fail_msg="断言：image组件，mode为bottom right，image组件样式测试不缩放图片，只显示图片的右下边区域")