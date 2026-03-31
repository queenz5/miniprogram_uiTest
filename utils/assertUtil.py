"""
Appium测试断言工具类
封装常用的断言方法，提供更直观的断言接口
"""

from typing import Any, Union
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.base import Base
from  config.testData import similarity

class AssertionUtil:
    def __init__(self, driver):
        """
        初始化断言工具
        
        Args:
            driver: Appium WebDriver实例
        """
        self.driver = driver
    
    def check_equal(self, value: Any, expect: Any = True, fail_msg: str = None):
        """
        检查值是否等于期望值
        
        Args:
            value: 实际值
            expect: 期望值，默认为True
            fail_msg: 失败时的自定义消息
        """
        if fail_msg is None:
            fail_msg = f"断言失败: 实际值 '{value}' 不等于期望值 '{expect}'"
        
        assert value == expect, fail_msg
    
    def check_component_exist(self, component: tuple, expect_exist: bool = True, 
                            wait_time: int = 10, scroll_target: Union[tuple, WebElement] = None):
        """
        检查组件是否存在
        
        Args:
            component: 组件定位器 (By, locator)
            expect_exist: 期望组件存在与否，默认为True
            wait_time: 等待时间（秒）
            scroll_target: 滚动目标，用于在滚动后查找组件
        """
        try:
            # 如果指定了滚动目标，先滚动到目标位置
            if scroll_target is not None:
                try:
                    scroll_element = self.driver.find_element(*scroll_target)
                    # 滚动到目标元素
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_element)
                    time.sleep(1)
                except:
                    pass  # 滚动失败不影响主要逻辑
            
            # 等待元素出现
            if wait_time > 0:
                wait = WebDriverWait(self.driver, wait_time)
                if expect_exist:
                    # 等待元素出现并可定位
                    wait.until(EC.presence_of_element_located(component))
                else:
                    # 等待元素消失
                    try:
                        wait.until_not(EC.presence_of_element_located(component))
                    except TimeoutException:
                        # 如果元素仍然存在，检查是否可见
                        try:
                            element = self.driver.find_element(*component)
                            assert not element.is_displayed(), f"组件 {component} 仍然存在且可见"
                        except NoSuchElementException:
                            # 元素不存在，符合期望
                            pass
            
            # 查找元素
            element = self.driver.find_element(*component)
            
            # 检查元素是否可见
            if expect_exist:
                assert element.is_displayed(), f"组件 {component} 存在但不可见"
            else:
                assert not element.is_displayed(), f"组件 {component} 仍然存在且可见"
                
        except TimeoutException:
            if expect_exist:
                assert False, f"组件 {component} 在 {wait_time} 秒内未找到"
            # 如果期望不存在，超时意味着元素不存在，符合期望
        except NoSuchElementException:
            if expect_exist:
                assert False, f"组件 {component} 未找到"
            # 如果期望不存在，找不到元素符合期望
        except Exception as e:
            if expect_exist:
                assert False, f"检查组件 {component} 时发生错误: {str(e)}"

    def check_text_exist(self, driver, target_text, lang="en", target_text_index=1, wait_time=1, expect=True, fail_msg=None):
        """
        检查文本是否存在
        
        Args:
            driver: Appium WebDriver实例
            target_text: 目标文本内容
            lang: 语言设置，默认为"en"
            target_text_index: 目标文本索引，默认为1
            wait_time: 等待时间（秒），默认为1
            expect: 期望文本存在与否，默认为True
            fail_msg: 失败时的自定义消息
        """
        # 调用Base类的find_text方法查找文本
        result = Base.find_text(driver, target_text, lang, target_text_index, wait_time)
        # 使用check_equal方法验证查找结果是否符合期望
        AssertionUtil.check_equal(self, result["isExits"], expect, fail_msg)

    def check_image_exist(self, driver, template_path, threshold: float = similarity, match_method: int = None,
                         resolution=None, position: int = 5, rgb: bool = False, wait_time=1, expect=True, fail_msg: str = None):
        """
        检查图像是否存在
        
        Args:
            driver: Appium WebDriver实例
            template_path: 模板图像路径
            threshold: 图像匹配阈值，默认为0.7
            match_method: 图像匹配方法
            resolution: 录制时的屏幕分辨率
            position: 匹配位置参数，默认为5（中心位置）
            rgb: 是否使用RGB颜色匹配，默认为False
            wait_time: 等待时间（秒），默认为1
            expect: 期望图像存在与否，默认为True
            fail_msg: 失败时的自定义消息
        """
        # 调用Base类的find_image方法查找图像
        result = Base.find_image(driver, template_path, threshold, match_method, resolution, position, rgb, wait_time)
        # 使用check_equal方法验证查找结果是否符合期望
        AssertionUtil.check_equal(self, result["isExits"], expect, fail_msg)