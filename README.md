# UI自动化测试框架

本项目是一个基于Appium和pytest的移动端UI自动化测试框架，支持Android和iOS平台的应用测试。

## 项目特点

- **跨平台支持**：同时支持Android和iOS应用测试
- **图像识别**：集成OpenCV和PaddleOCR实现图像和文本识别
- **智能断言**：提供丰富的断言工具类
- **报告生成**：自动生成详细的HTML测试报告
- **配置灵活**：支持多设备、多应用的配置管理
- **易于扩展**：模块化设计，便于功能扩展

## 项目结构

```
ui_automation_project/
│
├── README.md                   # 项目说明文档
├── requirements.txt            # Python依赖包列表
├── conftest.py                # pytest配置文件
├── initDriver.py              # Appium驱动初始化
├── createCase.py              # 测试用例生成工具
├── main.py                    # 主程序入口
├── config/                    # 配置文件目录
│   ├── testcases_android.conf # Android测试用例配置
│   ├── testcases_ios.conf     # iOS测试用例配置
│   └── testData.py            # 测试数据配置
├── testCase/                  # 测试用例目录
│   ├── android/               # Android测试用例
│   ├── ios/                   # iOS测试用例
│   └── test_report_integration.py # 报告集成测试
├── utils/                     # 工具类目录
│   ├── base.py                # 基础页面对象类
│   ├── assertUtil.py          # 断言工具类
│   ├── openCv_util.py         # OpenCV图像识别工具
│   ├── pytesseract_util.py    # OCR文本识别工具
│   └── ConfigParser_util.py   # 配置解析工具
└── reports/                   # 测试报告目录
```

## 环境要求

### 基础环境
- Python 3.7或更高版本
- Node.js和npm
- Appium服务器 2.0+

### 移动端环境
- **Android测试**：Android SDK、ADB工具
- **iOS测试**：Xcode、XCUITest驱动

### Python依赖
```
pytest>=6.0.0
Appium-Python-Client>=2.0.0
pytest-html>=3.0.0
opencv-python
numpy
paddleocr
paddlepaddle
pillow
```

## 安装配置

### 1. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 2. 安装Appium
```bash
# 全局安装Appium服务器
npm install -g appium

# 安装必要的驱动
appium driver install xcuitest  # iOS驱动
appium driver install uiautomator2  # Android驱动

# 安装图像识别插件
appium plugin install images
```

### 3. 配置设备信息
编辑 `config/testData.py` 文件，配置您的设备信息：

```python
# Android设备配置示例
ANDROID_CAPABILITIES = {
    "platformName": "Android",
    "platformVersion": "15",  # 安卓系统版本号
    "deviceName": "27c514x",  # adb devices 命令查询到的设备号
    "bundleId": "com.xxx.xxx",  # app bundleId
    "appActivity": "com.xxx.xxx.MainActivity",  # 设置应用的主Activity
    "automationName": "UiAutomator2",
    "noReset":True, # 设置 False 表示需要清楚应用缓存，但不卸载APP
    "fullReset": False,  # 设置 True 表示需要卸载APP
}

# iOS设备配置示例
IOS_CAPABILITIES = {
    "platformName": "iOS",
    "deviceName": "xxx的iPhone",  # 设备实际名称
    "bundleId": "com.xxx.xxx",  # 已安装应用的bundle ID
    "automationName": "XCUITest",
    "noReset": True,  # 设置 False 表示需要清楚应用缓存，但不卸载APP
    "fullReset": False,  # 设置 True 表示需要卸载APP
    "udid": "xxxxxx-00154DA03AB9802E",  # 设备的唯一标识符
    "platformVersion": "26.0",  # 设备实际的系统版本
    "scheme":"xxxxxxcec7395563d7" #scheme id
}
```

## 核心功能

### 1. 元素定位与操作
```python
from utils.base import Base

# 初始化Base类
base = Base(driver)

# 多种定位方式
element = base.find_element_by_id("element_id")
element = base.find_element_by_xpath("//xpath")
element = base.find_element_by_accessibility_id("accessibility_id")

# 智能点击
base.click_element(element)
base.click_element_by_id("element_id")

# 灵活滑动
base.swipe_between_points((100, 200), (300, 400))  # 坐标间滑动
base.swipe_from_element_to_coordinates(element, (300, 400))  # 元素到坐标
```

### 2. 图像识别功能

图像截图需要用 Airtest IDE  截图，Airtest IDE 截图会带上 resolution 分辨率参数，resolution 参数很重要，需要传给find_image_in_screen方法：
- Airtest IDE 下载地址 : https://airtest.netease.com/index.html
- Airtest IDE 截图后的图片信息：Template(r"tpl1758530632434.png", record_pos=(-0.422, -0.806), resolution=(1080, 2120))

```python
from utils.openCv_util import find_image_in_screen

# 图像匹配
result = find_image_in_screen(
    driver=driver,
    template_path="template.png",  # 模板图像路径
    threshold=0.8,                 # 相似度阈值
    resolution=(1080, 1920),       # 录制时分辨率
    position=5,                    # 返回位置(1-9宫格)
    rgb=False                      # 是否使用RGB匹配
)

# 返回结果包含坐标、尺寸和相似度信息
if result["isExits"]:
   (x, y) = result["target_coords"]
```

### 3. OCR文本识别
```python
from utils.pytesseract_util import find_text_in_screen

# 文本识别
result = find_text_in_screen(
    driver=driver,
    target_text="目标文本",
    lang="zh",           # 语言设置
    target_text_index=1  # 文本索引
)

# 返回结果包含文本位置和识别置信度
if result["isExits"]:
    (x, y) = result["target_coords"]
```

### 4. 智能断言
```python
from utils.assertUtil import AssertionUtil

# 初始化断言工具
assertion = AssertionUtil(driver)

# 元素存在断言
assertion.check_component_exist((AppiumBy.ID, "login_button"))

# 图像存在断言
assertion.check_image_exist(driver, "login_button.png", threshold=0.8)

# 文本存在断言
assertion.check_text_exist(driver, "登录", lang="zh")
```

## 运行测试

### 1. 启动Appium服务器
```bash
# 启动Appium服务器并启用图像识别插件
appium --log-level debug
```

### 2. 运行测试用例
```bash
# 运行所有测试
python main.py

# 或者指定用例文件运行
pytest testCase/ios/example/test_example.py -v

# 或者指定用例运行
pytest testCase/ios/example/test_example.py::Test_example::test_valid_logi -v

# 或者使用pytest运行
pytest testCase/ -v --html=reports/report.html
```

### 3. 生成测试报告
测试报告会自动生成在 `reports/` 目录下，包含：
- 测试执行结果
- 失败用例截图
- 执行时间统计
- 环境信息

## 最佳实践

### 1. 使用模版创建用例
```bash
python createCase.py 
```
```python
#通过模版创建用例需要填平台名称、测试用例模块。如下配置，填写后会得到testCase/ios/view/test_view.py 用例文件
platform = "ios" # android or ios
moduleName = "view" # 填写conf 文件的模块名称
```

### 2. 测试用例编写
```python
class Test_view:
    @classmethod
    def setup_class(self):
        self.driver_util = driver_util()
        self.driver = self.driver_util.init_ios_driver()
        self.base = Base(self.driver)
        self.assertionUtil = AssertionUtil(self.driver)

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

    def setup_method(self):
        # 每个用例执行前会执行的方法
        pass

    
    def test_view(self):
        """
        第一个测试用例 view
        pytest 用例的名称是以 test_ 开头的，后面的 view 就是用例方法的名称
        """
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = '/pages/component/view/view?case=row')

    def test_view_column(self):
        """
        第二个测试用例 view_column 
        """
        self.driver_util.startApplet(driver=self.driver,pathAndQuery='/pages/component/view/view?case=column')

```

### 3. 配置管理
使用配置文件管理不同环境的设置：
# config/testData.py

## 故障排除

### 常见问题

1. **设备连接问题**
   ```bash
   # 检查Android设备连接
   adb devices
   
   # 检查iOS设备连接
   xcrun xctrace list devices
   ```

2. **Appium驱动问题**
   ```bash
   # 查看已安装的驱动
   appium driver list
   
   # 重新安装驱动
   appium driver uninstall xcuitest
   appium driver install xcuitest
   ```

3. **图像识别问题**
   - 确保模板图像清晰度足够
   - 调整相似度阈值参数
   - 检查设备分辨率是否匹配

### 调试技巧

1. **使用Appium Inspector**
   - 下载地址：https://github.com/appium/appium-inspector/releases
   - 用于查看元素属性和构建定位器

2. **Appium Inspector 默认服务器地址**
   - APPIUM_SERVER_URL = "http://127.0.0.1:4723"

3. **Appium Inspector 设备配置示例**

   **Android设备配置示例：**
   ```json
   {
   "platformName": "Android",
   "appium:automationName": "UiAutomator2",
   "appium:platformVersion": "15",
   "appium:udid": "27c514xx",
   "appium:noReset": true
   }
   ```

   **iOS设备配置示例：**
   ```json
   {
   "platformName": "iOS",
   "appium:automationName": "XCUITest",
   "appium:deviceName": "iPhone 11",
   "appium:platformVersion": "26.0",
   "appium:bundleId": "com.xxx.xxx",
   "appium:udid": "xxxxxx-00154DA03AB9802E",
   "appium:noReset": true
   }
   ```

4. **日志分析**
   ```bash
   # 启动详细日志模式
   appium --log-level debug
   ```

## 扩展开发

### 添加新功能
1. 在 `utils/` 目录下创建新的工具类
2. 继承 `Base` 类以复用基础功能
3. 在测试用例中导入并使用

### 自定义断言
```python
# 在assertUtil.py中添加自定义断言方法
def check_custom_condition(self, condition, expect=True, fail_msg=None):
    if fail_msg is None:
        fail_msg = f"自定义条件检查失败: {condition}"
    assert condition == expect, fail_msg
```
