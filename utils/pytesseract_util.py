# -*- encoding=utf8 -*-
__author__ = "ftjk-peng"

import os
from PIL import Image, ImageDraw
import string
from paddleocr import PaddleOCR
import random
import time
from datetime import datetime

# 全局变量，用于存储PaddleOCR生成的所有截图路径及其时间戳
ocr_screenshot_paths = []  # 存储元组列表 (timestamp, screenshot_path)

def calculate_scale_factor(driver, screenshot_path):
    """
    计算屏幕截图像素与Appium逻辑坐标的缩放因子 (Scale Factor)。
    
    Args:
        driver: Appium WebDriver 实例。
        screenshot_path: 屏幕截图的文件路径。
        
    Returns:
        float: 计算出的 Scale Factor。
    """
    # 获取逻辑分辨率 (Appium 坐标系)
    window_size = driver.get_window_size()
    logical_width = window_size['width']
    logical_height = window_size['height']
    
    # 获取截图的物理像素分辨率
    with Image.open(screenshot_path) as screenshot_img:
        pixel_width, pixel_height = screenshot_img.size
        
    # 计算 Scale Factor
    scale_factor_width = pixel_width / logical_width
    scale_factor_height = pixel_height / logical_height
    
    # 理论上这两个值应该相等或非常接近
    # 取一个平均值或检查它们是否接近
    if abs(scale_factor_width - scale_factor_height) < 0.1: # 容差
        scale_factor = (scale_factor_width + scale_factor_height) / 2.0
    else:
        # 如果不一致，记录警告并取宽度的比率作为近似值
        print(f"警告：截图宽高比与逻辑宽高比不匹配。截图: {pixel_width}x{pixel_height}, 逻辑: {logical_width}x{logical_height}")
        scale_factor = scale_factor_width # 或使用 height，根据实际情况调整策略

    return scale_factor


def find_text_in_screen_PaddleOCR(driver, target_text, lang="en", target_text_index=1):
    """
    识别图片中目标文案的坐标。
    
    :param driver: Appium WebDriver 实例
    :param target_text: 需要查找的字符串
    :param lang: 语言，默认是英文"en"，支持['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari']
    :param target_text_index: 目标文本的索引（从1开始），用于指定要查找第几个匹配的文本
    :return: 包含查找结果的字典，包括是否存在、文本内容、数量、目标坐标和截图路径
    """
    # 创建保存截图的文件夹
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screenShot_path = os.path.join(current_dir, '..', 'reports/screenShot')
    os.makedirs(screenShot_path, exist_ok=True)

    imageName = f"{generate_random_string()}_screenshot.png"
    screenshot_filename = os.path.join(screenShot_path, imageName)
    
    # 截屏
    driver.save_screenshot(screenshot_filename)
    # 将截图路径和时间戳添加到全局列表，以便在conftest.py中按时间顺序捕获并添加到报告
    global ocr_screenshot_paths
    timestamp = datetime.now()
    ocr_screenshot_paths.append((timestamp, screenshot_filename))
    
    if not os.access(screenshot_filename, os.F_OK):
        print("截图路径错误:", screenshot_filename)
        return {'isExits': False, 'text': '', 'count': 0, 'target_coords': None, 'screenshot_path': None}

    try:
        print("------开始文字识别------")
        ocr = PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=False)
        ocr_result = ocr.ocr(screenshot_filename, cls=True)
        print("------结束文字识别2------")
    except Exception as e:
        print(f"OCR识别失败: {e}")
        return {'isExits': False, 'text': str(e), 'count': 0, 'target_coords': None, 'screenshot_path': screenshot_filename}

    text = str(ocr_result)
    isExits = target_text in text
    count = text.count(target_text) if isExits else 0
    target_coords = None
    target_boxes_to_draw = []

    if isExits:
        n = 0
        # 遍历识别结果，找到目标文字的坐标
        for line in ocr_result:
            for word_info in line:
                # 获取识别结果的文字信息
                if target_text in word_info[1][0]:
                    # 获取文字的边界框坐标
                    box = word_info[0]
                    # 获取文字的中心点坐标
                    x1, y1 = box[0]
                    x2, y2 = box[2]
                    center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
                    
                    n += 1
                    # 注意：target_text_index 是从 1 开始计数的
                    if n == target_text_index:
                        target_coords = (center_x, center_y)
                        target_boxes_to_draw = [box] # 只保留当前索引对应的框用于标注
                        break
            # 如果找到了指定索引的文本，则跳出外层循环
            if target_coords and n == target_text_index:
                break
            else:
                isExits=False

        # 在截图上绘制红色矩形框并覆盖保存原图
        # 只有在成功找到对应索引的坐标时才进行标注
        if target_coords and target_boxes_to_draw:
            try:
                # 读取截图
                screenshot_img = Image.open(screenshot_filename)
                draw = ImageDraw.Draw(screenshot_img)
                
                # 绘制指定索引的文字框
                for box in target_boxes_to_draw:
                    # PIL的polygon需要一个点的元组列表
                    points = [(int(point[0]), int(point[1])) for point in box]
                    draw.polygon(points, outline="red", width=2)
                    
                # 覆盖保存标注后的图像到原文件
                screenshot_img.save(screenshot_filename)
            except Exception as e:
                print(f"保存标注截图时出错: {e}")
        
        # OCR 识别出来的坐标和appium的坐标体系不一致，需要进行转换
        # 无论 iOS 还是 Android 都需要转换
        if target_coords:
            try:
                # 使用新封装的方法计算 Scale Factor
                scale_factor = calculate_scale_factor(driver, screenshot_filename)
                # 使用动态计算的 Scale Factor 进行坐标转换
                target_coords = (int(target_coords[0] / scale_factor), int(target_coords[1] / scale_factor))
            except Exception as e:
                print(f"坐标转换失败: {e}")
                # 如果转换失败，返回原始坐标（可能不准确）
                # target_coords 保持不变

    print(f"{'找到' if isExits else '未找到'}目标文字 '{target_text}'，原始截图已保存到: {imageName}")
    return {
        'isExits': isExits, 
        'text': text, 
        'count': count, 
        'target_coords': target_coords, 
        'screenshot_path': screenshot_filename
    }


# 加了 wait_time 重试参数
def find_text_in_screen(driver, target_text, lang="en", target_text_index=1, wait_time=1):
    for i in range(wait_time):
        time.sleep(1)
        result = find_text_in_screen_PaddleOCR(driver, target_text, lang, target_text_index)
        if result['isExits']:
            break
    return result


def generate_random_string(length=5):
    """
    生成一个指定长度的随机字符串，包含大小写字母和数字。
    :param length: 字符串的长度，默认为5。
    :return: 一个随机字符串。
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == '__main__':
    print("")
