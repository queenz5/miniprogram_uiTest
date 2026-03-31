"""
基础页面对象类，定义所有页面的通用方法。
"""

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple
import time
from selenium.common.exceptions import NoSuchElementException


from sympy.physics.units import length

from initDriver import DEFAULT_TIMEOUT,ANDROID_CAPABILITIES,IOS_CAPABILITIES
from utils.pytesseract_util import find_text_in_screen
from utils.openCv_util import find_image_in_screen
from config.testData import similarity


class Base:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def tap_coordinates(self,coordinates) -> None:
        """
        通过坐标点击：coordinates = (x,y)
        """
        x = coordinates[0]
        y = coordinates[1]
        platform = self.driver.capabilities.get("platformName", "").lower()

        if "ios" in platform:
            # iOS 优先使用 mobile: tap
            self.driver.execute_script('mobile: tap', {'x': x, 'y': y})
            # self.driver.tap([(x,y)])
        else:
            # Android 使用标准方法
            actions = ActionBuilder(self.driver)
            actions.pointer_action.move_to_location(x, y)
            actions.pointer_action.click()
            actions.perform()

    @classmethod
    def find_text(self,driver, target_text, lang="en", target_text_index=1,wait_time=1):
        """
        识别屏幕中目标文案的坐标。
        """
        return find_text_in_screen(driver, target_text, lang, target_text_index,wait_time)

    @classmethod
    def  find_image(self,driver,template_path,threshold: float = similarity,match_method: int = None,resolution= None,position: int = 5,rgb: bool = False,wait_time=1):
        """
        识别屏幕中目标图片的坐标。
        """
        if isinstance(template_path, list):
            for i in range(len(template_path)):
                result = find_image_in_screen(driver,template_path[i],threshold,match_method,resolution,position,rgb,wait_time)
                if result["isExits"] == True:
                    break
            return result
        else:
            return find_image_in_screen(driver,template_path,threshold,match_method,resolution,position,rgb,wait_time)

    def close_app(self):
        """
        关闭APP，根据平台决定从 ANDROID_CAPABILITIES 或者 IOS_CAPABILITIES 里面取 bundleId
        """
        platform = self.driver.capabilities.get("platformName", "").lower()
        
        if "android" in platform:
            bundle_id = ANDROID_CAPABILITIES.get("bundleId")
        elif "ios" in platform:
            bundle_id = IOS_CAPABILITIES.get("bundleId")
        else:
            raise Exception(f"不支持的平台: {platform}")
        
        if bundle_id:
            self.driver.terminate_app(bundle_id)
        else:
            raise Exception("未找到应用的bundleId")

    def swipe_back(self):
        """
        模拟系统侧滑返回
        """
        platform = self.driver.capabilities.get("platformName", "").lower()
        size = self.driver.get_window_size()
        
        if "ios" in platform:
            # iOS 侧滑返回
            self.driver.execute_script('mobile: swipe', {'direction': 'right'})
        else:
            # Android 侧滑返回（从屏幕左边缘向右滑动）
            start_x = size['width'] * 0.1
            start_y = size['height'] / 2
            end_x = size['width'] * 0.9
            end_y = start_y
            
            self.driver.swipe(start_x, start_y, end_x - start_x, end_y - start_y, 500)

    def go_to_home(self):
        """
        模拟系统回到桌面
        """
        platform = self.driver.capabilities.get("platformName", "").lower()
        
        if "ios" in platform:
            # iOS 回到桌面
            self.driver.execute_script('mobile: pressButton', {'name': 'home'})
        else:
            # Android 回到桌面
            self.driver.press_keycode(3)  # HOME键

    def find_element_by_id(self, element_id: str) -> WebElement:
        """
        根据ID查找单个元素
        """
        return self.driver.find_element(AppiumBy.ID, element_id)

    def find_elements_by_class_name(self, class_name: str) -> List[WebElement]:
        """
        根据类名查找多个元素
        """
        return self.driver.find_elements(AppiumBy.CLASS_NAME, class_name)

    def find_element_by_xpath(self, xpath: str) -> WebElement:
        """
        根据XPath查找单个元素
        """
        return self.driver.find_element(AppiumBy.XPATH, xpath)

    def find_element_by_accessibility_id(self, accessibility_id: str) -> WebElement:
        """
        根据Accessibility ID查找单个元素
        """
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
        
    def swipe_between_points(self, start_point: Tuple[int, int], end_point: Tuple[int, int], duration: int = 1000):
        """
        swipe 方式实现在两个坐标点之间滑动
        
        Args:
            start_point: 起始坐标 (x, y)
            end_point: 结束坐标 (x, y)
            duration: 滚动持续时间(毫秒)
        """
        start_x, start_y = start_point
        end_x, end_y = end_point
        
        # 确保坐标在屏幕范围内
        window_size = self.driver.get_window_size()
        start_x = max(0, min(start_x, window_size['width'] - 1))
        start_y = max(0, min(start_y, window_size['height'] - 1))
        end_x = max(0, min(end_x, window_size['width'] - 1))
        end_y = max(0, min(end_y, window_size['height'] - 1))
        
        # 计算偏移量
        offset_x = end_x - start_x
        offset_y = end_y - start_y

        # 执行滑动操作
        self.driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def actions_between_points(self, start_point: Tuple[int, int], end_point: Tuple[int, int]):
        """
        actions 方式实现在两个坐标点之间滑动，模拟手指操作

        Args:
            start_point: 起始坐标 (x, y)
            end_point: 结束坐标 (x, y)
            duration: 滚动持续时间(毫秒)
        """
        start_x, start_y = start_point
        end_x, end_y = end_point

        # 确保坐标在屏幕范围内
        window_size = self.driver.get_window_size()
        start_x = max(0, min(start_x, window_size['width'] - 1))
        start_y = max(0, min(start_y, window_size['height'] - 1))
        end_x = max(0, min(end_x, window_size['width'] - 1))
        end_y = max(0, min(end_y, window_size['height'] - 1))

        # 使用W3C Actions执行滑动
        actions = ActionBuilder(self.driver)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.pointer_up()
        actions.perform()

    def mobile_swiper(self,direction="up"):
        """
        使用 mobile:手势命令实现屏幕上下左右滑动

        Args:
            direction: 滑动方向，支持 up、down、left、right
        """
        platform = self.driver.capabilities.get("platformName", "").lower()
        direction = direction.lower()
        
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError(f"不支持的滑动方向: {direction}，支持的方向: up, down, left, right")
        
        if "ios" in platform:
            # iOS 使用 mobile: swipe 命令
            self.driver.execute_script('mobile: swipe', {'direction': direction})
        else:
            # Android 使用传统swipe方法
            size = self.driver.get_window_size()
            center_x = size['width'] // 2
            center_y = size['height'] // 2
            # 滑动距离为屏幕尺寸的40%
            scroll_distance = int(min(size['width'], size['height']) * 0.4)
            
            if direction == "up":
                self.driver.swipe(center_x, center_y + scroll_distance, center_x, center_y - scroll_distance, 500)
            elif direction == "down":
                self.driver.swipe(center_x, center_y - scroll_distance, center_x, center_y + scroll_distance, 500)
            elif direction == "left":
                self.driver.swipe(center_x + scroll_distance, center_y, center_x - scroll_distance, center_y, 500)
            elif direction == "right":
                self.driver.swipe(center_x - scroll_distance, center_y, center_x + scroll_distance, center_y, 500)
        
    def swipe_from_element_to_coordinates(self, element: WebElement, end_coordinates: Tuple[int, int], duration: int = 1000):
        """
        从元素滚动到指定坐标
        
        Args:
            element: 起始元素
            end_coordinates: 结束坐标 (x, y)
            duration: 滚动持续时间(毫秒)
        """
        # 获取元素的中心点坐标
        location = element.location
        size = element.size
        start_x = location['x'] + size['width'] // 2
        start_y = location['y'] + size['height'] // 2
        
        # 执行滑动操作
        self.swipe_between_points((start_x, start_y), end_coordinates, duration)
        
    def swipe_from_coordinates_to_element(self, start_coordinates: Tuple[int, int], element: WebElement, duration: int = 1000):
        """
        从指定坐标滚动到元素
        
        Args:
            start_coordinates: 起始坐标 (x, y)
            element: 目标元素
            duration: 滚动持续时间(毫秒)
        """
        # 获取元素的中心点坐标
        location = element.location
        size = element.size
        end_x = location['x'] + size['width'] // 2
        end_y = location['y'] + size['height'] // 2
        
        # 执行滑动操作
        self.swipe_between_points(start_coordinates, (end_x, end_y), duration)
        
    def swipe_from_element_to_element(self, start_element: WebElement, end_element: WebElement, duration: int = 1000):
        """
        从一个元素滚动到另一个元素
        
        Args:
            start_element: 起始元素
            end_element: 目标元素
            duration: 滚动持续时间(毫秒)
        """
        # 获取起始元素的中心点坐标
        start_location = start_element.location
        start_size = start_element.size
        start_x = start_location['x'] + start_size['width'] // 2
        start_y = start_location['y'] + start_size['height'] // 2
        
        # 获取目标元素的中心点坐标
        end_location = end_element.location
        end_size = end_element.size
        end_x = end_location['x'] + end_size['width'] // 2
        end_y = end_location['y'] + end_size['height'] // 2
        
        # 执行滑动操作
        self.swipe_between_points((start_x, start_y), (end_x, end_y), duration)

    def click_element(self, element: WebElement, timeout: int = DEFAULT_TIMEOUT):
        """
        点击元素，包含等待元素可点击的逻辑

        Args:
            element: 要点击的WebElement对象
            timeout: 等待超时时间(秒)
        """
        # 等待元素可点击
        wait = WebDriverWait(self.driver, timeout)
        clickable_element = wait.until(EC.element_to_be_clickable(element))

        # 点击元素
        clickable_element.click()

    def long_press_coordinates(self, coordinates, duration: int = 1000):
        """
        长按指定坐标

        Args:
            coordinates: 坐标点 (x, y)
            duration: 长按持续时间(毫秒)，默认1000毫秒
        """
        x, y = coordinates
        platform = self.driver.capabilities.get("platformName", "").lower()

        if "ios" in platform:
            # iOS 使用 mobile: touchAndHold
            self.driver.execute_script('mobile: touchAndHold', {
                'x': x,
                'y': y,
                'duration': duration / 1000  # iOS需要秒为单位
            })
        else:
            # Android 使用 Actions 实现长按
            actions = ActionBuilder(self.driver)
            actions.pointer_action.move_to_location(x, y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.pause(duration / 1000)  # 转换为秒
            actions.pointer_action.pointer_up()
            actions.perform()

    def long_press_element(self, element: WebElement, duration: int = 1000):
        """
        长按元素

        Args:
            element: 要长按的WebElement对象
            duration: 长按持续时间(毫秒)，默认1000毫秒
        """
        # 获取元素中心坐标
        location = element.location
        size = element.size
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 2

        # 调用坐标长按方法
        self.long_press_coordinates((center_x, center_y), duration)

    def text(self, text: str, enter: bool = True):
        """
        输入文本
        Args:
            text: 要输入的文本
            enter: 是否换行
        """
        time.sleep(1)
        platform = self.driver.capabilities.get("platformName", "").lower()
        escaped_text = text.replace("'", "\\'").replace('"', '\\"').replace(' ', '%s')
        if "ios" in platform:
            if enter:
                escaped_text += '\n'
            try:
                # 使用active_element
                active = self.driver.switch_to.active_element
                active.send_keys(escaped_text)
            except:
                    # 使用UIAutomation或XCUIElementType搜索输入框
                    try:
                        # 搜索当前页面所有文本框
                        textfields = self.driver.find_elements(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField')
                        textviews = self.driver.find_elements(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextView')

                        # 尝试向最后一个获得焦点的文本框输入
                        all_inputs = textfields + textviews
                        if all_inputs:
                            last_input = all_inputs[-1]  # 通常最后一个是最新的
                            last_input.send_keys(escaped_text)
                    except Exception as e:
                        # 如果所有方法都失败，抛出异常
                        raise Exception(f"所有输入方法都失败了: {str(e)}")
        else:
            # 安卓需要原生的输入框才可以使用 self.driver.execute_script('mobile: type', {'text': escaped_text})
            import subprocess
            subprocess.run(["adb", "shell", "input", "text", escaped_text],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            if enter:
                subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_BACK"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    def safe_click_by_text(self, xpath):
        try:
            element = self.driver.find_element(AppiumBy.XPATH, xpath)
            if element:
                element.click()
                return True
        except:
            pass
        return False

    def check_element_exist(self, xpath, expect=True, fail_msg=None):
        """
        检查元素存在性，根据期望结果判断通过或失败

        :param xpath: 元素xpath
        :param error: 自定义错误信息
        :param expect: 期望元素是否存在，True表示期望存在，False表示期望不存在
        :return: True表示符合期望，失败时抛异常
        """
        try:
            element = self.driver.find_element(AppiumBy.XPATH, xpath)
            print(element)
            print("==========")
            # 找到元素
            if expect:
                # 期望存在且确实存在 - 通过
                return True
            else:
                # 期望不存在但找到了 - 失败
                raise AssertionError(fail_msg)

        except NoSuchElementException:
            # 没找到元素
            if not expect:
                # 期望不存在且确实不存在 - 通过
                return True
            else:
                # 期望存在但没找到 - 失败
                raise AssertionError(fail_msg)

        except AssertionError:
            # 重新抛出AssertionError
            raise
        except Exception as e:
            # 其他异常
            error_msg = fail_msg or f"查找元素时发生错误: {xpath}"
            raise AssertionError(f"{error_msg}: {str(e)}")



