"""
Appium OpenCV 工具类
封装基于OpenCV的图像识别方法
"""
from typing import Tuple, Optional
from config.testData import similarity
import os
from datetime import datetime

# 尝试导入OpenCV
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("警告: OpenCV未安装，find_image_OpenCV功能将不可用")

# 导入计算 scale factor 的函数
from utils.pytesseract_util import *
from PIL import Image

# 全局变量，用于存储OpenCV生成的所有截图路径及其时间戳
opencv_screenshot_paths = []  # 存储元组列表 (timestamp, screenshot_path)


def _scale_template_image(template_original, recorded_resolution, device_resolution):
    """
    根据录制分辨率和当前设备分辨率缩放模板图像
    
    Args:
        template_original: 原始模板图像
        recorded_resolution: 录制时的屏幕逻辑分辨率 (width, height)
        device_resolution: 当前设备截图后图片分辨率 (width, height)
        
    Returns:
        Tuple: (缩放后的模板图像, 使用的缩放因子)
    """
    template_scaled = template_original
    scale_factor_used = 1.0
    
    if recorded_resolution is not None and device_resolution is not None:
        try:
            recorded_w, recorded_h = recorded_resolution
            current_w, current_h = device_resolution
            
            # 获取原始模板图像尺寸
            template_orig_h, template_orig_w = template_original.shape[:2]
            
            # 判断分辨率是否不同
            if (recorded_w != current_w or recorded_h != current_h):
                print(f"需要进行缩放,当前屏幕尺寸{device_resolution},模版图片尺寸{recorded_resolution}")
                
                # 计算基于分辨率的预期缩放因子
                expected_scale_x = current_w / recorded_w
                expected_scale_y = current_h / recorded_h
                
                # 保持宽高比的缩放因子
                expected_scale_factor = min(expected_scale_x, expected_scale_y)
                
                # 在预期缩放因子附近进行小范围多尺度搜索
                # 这样结合了Airtest的多尺度搜索和您算法的性能优势
                min_scale = max(0.1, expected_scale_factor * 0.8)
                max_scale = min(2.0, expected_scale_factor * 1.2)
                scale_step = 0.05  # 较小的步长
                
                best_scale = expected_scale_factor
                best_quality = -1
                
                # 在小范围内搜索最佳缩放因子
                for scale in np.arange(min_scale, max_scale + scale_step, scale_step):
                    new_w = int(template_orig_w * scale)
                    new_h = int(template_orig_h * scale)
                    
                    # 检查尺寸有效性
                    if new_w > 10 and new_h > 10:
                        try:
                            # 选择插值方法
                            interpolation_method = _choose_interpolation_method(scale)
                            scaled_temp = cv2.resize(template_original, (new_w, new_h), 
                                                   interpolation=interpolation_method)
                            
                            # 简单的质量评估（基于尺寸合理性）
                            # 这里可以扩展为更复杂的质量评估
                            quality = 1.0 / (1.0 + abs(scale - expected_scale_factor))  # 越接近预期值质量越高
                            
                            if quality > best_quality:
                                best_quality = quality
                                best_scale = scale
                                template_scaled = scaled_temp
                        except cv2.error as e:
                            continue
                
                scale_factor_used = best_scale
                print(f"模板图像已缩放: {template_orig_w}x{template_orig_h} -> {template_scaled.shape[1]}x{template_scaled.shape[0]}, 缩放因子: {scale_factor_used:.2f}")
            else:
                print("录制分辨率与当前设备分辨率相同，无需缩放")
        except Exception as e:
            # 如果出现异常，使用原始模板
            print(f"缩放过程中出现异常: {e}, 使用原始模板")
            template_scaled = template_original
    
    return template_scaled, scale_factor_used


def _choose_interpolation_method(scale_factor):
    """
    根据缩放比例选择最优的插值方法
    
    Args:
        scale_factor: 缩放比例
        
    Returns:
        int: OpenCV插值方法常量
    """
    if scale_factor > 1.5:
        # 放大图像，使用立方插值获得更好的质量
        return cv2.INTER_CUBIC
    elif scale_factor < 0.5:
        # 大幅缩小图像，使用区域插值
        return cv2.INTER_AREA
    elif scale_factor < 1.0:
        # 轻微缩小，使用线性插值
        return cv2.INTER_LINEAR
    else:
        # 轻微放大或接近原尺寸，使用线性插值
        return cv2.INTER_LINEAR


def find_image_OpenCV(
    driver, 
    template_path: str, 
    threshold: float = similarity,
    match_method: int = None,
    resolution: Optional[Tuple[int, int]] = None,
    position: int = 5,
    rgb: bool = False
):
    """
    使用OpenCV技术查找图像，可调整相似度，根据屏幕分辨率自动缩放模板图片。

    Args:
        driver: Appium WebDriver 实例。
        template_path: 模板图像路径。
        threshold: 相似度阈值 (0-1.0)，默认0.8。
        match_method: OpenCV匹配方法，默认使用cv2.TM_CCOEFF_NORMED。
        resolution: 录制时的屏幕逻辑分辨率 (width, height)。
                    例如: (828, 1792)。
        position: 返回坐标的位置，将识别到的目标区域划分为9宫格(3x3)。
                 1 2 3
                 4 5 6  (默认为5，即中心位置)
                 7 8 9
        rgb: 是否使用RGB颜色校验，默认为False。

    Returns:
        Tuple[int, int, int, int, float, Tuple[int, int]] | None:
            (x, y, width, height, similarity, target_coords) 或 None（未找到）。
            注意：返回的坐标是基于Appium坐标系的。
            target_coords: 根据position参数计算出的目标点击坐标。

    Raises:
        ImportError: 如果OpenCV未安装。
        FileNotFoundError: 如果模板图像不存在。
        ValueError: 如果position参数不在1-9范围内。
    """
    if not OPENCV_AVAILABLE:
        raise ImportError("OpenCV未安装，请运行: pip install opencv-python")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '..',template_path)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板图像不存在: {template_path}")

    # 验证position参数
    if position < 1 or position > 9:
        raise ValueError("position参数必须在1-9之间")

    if match_method is None:
        match_method = cv2.TM_CCOEFF_NORMED

    try:
        # 1. 获取目标屏幕截图
        #设置截图保存路径
        screenShot_path = os.path.join(current_dir, '..','reports/screenShot')
        os.makedirs(screenShot_path, exist_ok=True)
        imageName = f"{generate_random_string()}_screenshot.png"
        save_path = os.path.join(screenShot_path, imageName)
        driver.save_screenshot(save_path)
        # 将截图路径和时间戳添加到全局列表，以便在conftest.py中按时间顺序捕获并添加到报告
        global opencv_screenshot_paths
        timestamp = datetime.now()
        opencv_screenshot_paths.append((timestamp, save_path))

        screenshot_img_pil = Image.open(save_path)
        screenshot_cv = cv2.cvtColor(np.array(screenshot_img_pil), cv2.COLOR_RGB2BGR)
        screenshot_h, screenshot_w = screenshot_cv.shape[:2]
        device_resolution = (screenshot_w,screenshot_h)

        # 2. 读取原始模板图像
        template_original = cv2.imread(template_path)
        if template_original is None:
            raise FileNotFoundError(f"无法读取模板图像: {template_path}")

        # 3. 缩放原始模版图像：目标屏幕分辨率 和 resolution 不一致时进行缩放
        template_scaled, scale_factor_used = _scale_template_image(template_original, resolution, device_resolution)

        # 4. 执行模版匹配
        try:
            if rgb:
                # 分别对每个颜色通道进行匹配
                b_match = cv2.matchTemplate(screenshot_cv[:, :, 0], template_scaled[:, :, 0], match_method)
                g_match = cv2.matchTemplate(screenshot_cv[:, :, 1], template_scaled[:, :, 1], match_method)
                r_match = cv2.matchTemplate(screenshot_cv[:, :, 2], template_scaled[:, :, 2], match_method)

                # 计算平均相似度
                result = (b_match + g_match + r_match) / 3
            else:
                result = cv2.matchTemplate(screenshot_cv, template_scaled, match_method)
        except cv2.error:
            raise RuntimeError("模板匹配失败")

        # 5. 分析匹配结果是否满足条件
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 确定相似度值
        if match_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            similarity = 1 - min_val
        else:
            similarity = max_val

        # 检查匹配结果是否满足阈值
        if similarity >= threshold:
            # 获取匹配位置
            match_loc = min_loc if match_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] else max_loc
            x, y = match_loc
            h, w = template_scaled.shape[:2]

            # 计算目标点击坐标
            # 将匹配到的区域划分为3x3的网格，根据position参数确定点击位置
            grid_w = w // 3
            grid_h = h // 3

            # 计算9宫格中各个位置的坐标
            positions_coords = {
                1: (x + grid_w // 2, y + grid_h // 2),
                2: (x + grid_w + grid_w // 2, y + grid_h // 2),
                3: (x + 2 * grid_w + grid_w // 2, y + grid_h // 2),
                4: (x + grid_w // 2, y + grid_h + grid_h // 2),
                5: (x + grid_w + grid_w // 2, y + grid_h + grid_h // 2),
                6: (x + 2 * grid_w + grid_w // 2, y + grid_h + grid_h // 2),
                7: (x + grid_w // 2, y + 2 * grid_h + grid_h // 2),
                8: (x + grid_w + grid_w // 2, y + 2 * grid_h + grid_h // 2),
                9: (x + 2 * grid_w + grid_w // 2, y + 2 * grid_h + grid_h // 2)
            }

            # 获取目标点击坐标
            target_coords = positions_coords[position]

            # 6. 绘制和保存结果
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            annotated_screenshot = screenshot_cv.copy()
            cv2.rectangle(annotated_screenshot, top_left, bottom_right, (0, 0, 255), 2)
            cv2.putText(annotated_screenshot,str(round(similarity, 3)), (x+5, y+5),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0),2)

            annotated_image_rgb = cv2.cvtColor(annotated_screenshot, cv2.COLOR_BGR2RGB)
            annotated_pil_image = Image.fromarray(annotated_image_rgb)
            annotated_pil_image.save(save_path, "PNG")

            # 坐标转换
            scale_factor = calculate_scale_factor(driver, save_path)
            converted_x = int(x / scale_factor)
            converted_y = int(y / scale_factor)
            converted_w = int(w / scale_factor)
            converted_h = int(h / scale_factor)
            converted_target_x = int(target_coords[0] / scale_factor)
            converted_target_y = int(target_coords[1] / scale_factor)
            target_coords = (converted_target_x, converted_target_y)
            print(f"识别成功后的图片保存至路径：{imageName}。相似度{similarity},坐标转换比例{scale_factor}")

            return  {
                'isExits': True,
                'converted_x': converted_x,
                'converted_y': converted_y,
                'converted_w': converted_w,
                'converted_h': converted_h,
                'similarity':similarity,
                'target_coords': target_coords,
                'screenshot_path': save_path,
            }
        print(f"没有找到目标图片，截图已保存至: {imageName}")
        return {
                'isExits': False,
                'screenshot_path': save_path,
            }

    except Exception as e:
        raise RuntimeError(f"OpenCV图像匹配失败: {str(e)}")

# 加了 wait_time 重试参数
def find_image_in_screen(driver,template_path: str,threshold: float = similarity,match_method: int = None,resolution: Optional[Tuple[int, int]] = None,position: int = 5,rgb: bool = False,wait_time=1):
    for i in range(wait_time):
        time.sleep(1)
        result=find_image_OpenCV(driver,template_path,threshold,match_method,resolution,position,rgb)
        if result["isExits"] == True:
            break
    return result