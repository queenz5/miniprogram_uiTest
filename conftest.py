"""
用于为测试结果生成HTML报告的插件。
此conftest.py文件配置pytest-html插件以生成详细的测试报告。
"""

import pytest
import os
from datetime import datetime
import base64


def pytest_configure(config):
    """使用自定义设置配置pytest。"""
    # 如果reports目录不存在则创建
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # 设置HTML报告配置
    config.option.htmlpath = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    config.option.self_contained_html = True


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在测试失败时向报告中添加截图。"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    
    if report.when == 'call':
        # 在失败时添加截图
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 获取测试类中的driver实例
            if hasattr(item.instance, 'driver'):
                driver = item.instance.driver
                try:
                    screenshot_dir = 'reports/screenShot'
                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)
                    
                    # 生成截图文件名
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_name = f"{item.name}_{timestamp}.png"
                    screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                    
                    # 截图并保存
                    driver.get_screenshot_as_file(screenshot_path)
                    
                    # 使用绝对路径确保截图可以正确显示
                    abs_screenshot_path = os.path.abspath(screenshot_path)
                    
                    # 添加截图到报告
                    extra.append(pytest_html.extras.png(abs_screenshot_path, "失败截图"))
                except Exception as e:
                    print(f"截图失败: {str(e)}")

        # 收集 pytesseract_util.py 和 openCv_util.py 中存储的截图路径，按时间戳合并并按顺序添加
        combined_screenshots = []
        
        # 检查 pytesseract_util.py 中存储的截图路径列表
        try:
            # 动态导入 pytesseract_util 模块来获取 ocr_screenshot_paths
            from utils.pytesseract_util import ocr_screenshot_paths
            if ocr_screenshot_paths:
                # 添加PaddleOCR截图到合并列表
                for timestamp, screenshot_path in ocr_screenshot_paths:
                    combined_screenshots.append((timestamp, "PaddleOCR", screenshot_path))
        except ImportError:
            # 如果模块不可导入，则跳过
            pass
        except Exception as e:
            print(f"检查PaddleOCR截图失败: {str(e)}")
        
        # 检查 openCv_util.py 中存储的截图路径列表
        try:
            # 动态导入 openCv_util 模块来获取 opencv_screenshot_paths
            from utils.openCv_util import opencv_screenshot_paths
            if opencv_screenshot_paths:
                # 添加OpenCV截图到合并列表
                for timestamp, screenshot_path in opencv_screenshot_paths:
                    combined_screenshots.append((timestamp, "OpenCV", screenshot_path))
        except ImportError:
            # 如果模块不可导入，则跳过
            pass
        except Exception as e:
            print(f"检查OpenCV截图失败: {str(e)}")
        
        # 按时间戳排序
        combined_screenshots.sort(key=lambda x: x[0])
        
        # 按时间顺序添加截图到报告
        for i, (timestamp, source, screenshot_path) in enumerate(combined_screenshots):
            if os.path.exists(screenshot_path):
                # 使用绝对路径确保截图可以正确显示
                abs_image_path = os.path.abspath(screenshot_path)
                # 添加截图到报告，按时间顺序命名
                imageName = screenshot_path.split('screenShot/')[-1]
                extra.append(pytest_html.extras.png(abs_image_path, f"{source} {imageName} ({timestamp.strftime('%H:%M:%S.%f')[:-3]})"))
        
        # 清空所有列表，避免在后续报告中重复添加
        try:
            import utils.pytesseract_util
            utils.pytesseract_util.ocr_screenshot_paths = []
        except ImportError:
            pass
        
        try:
            import utils.openCv_util
            utils.openCv_util.opencv_screenshot_paths = []
        except ImportError:
            pass
        
        report.extra = extra
