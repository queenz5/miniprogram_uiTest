"""
存放公共数据
"""


bundleId = 'com.xxx.xxx'
demoAppid = '617270d176abb100010e79b3'

apiServer = 'https://xxx-testing.xxx.club'
similarity = 0.7 #默认图片相似度

# Appium服务器URL
APPIUM_SERVER_URL = "http://localhost:4723"
# WebDriverWait的默认超时时间
DEFAULT_TIMEOUT = 10
# 平台名称
ANDROID = "Android"
IOS = "iOS"

# 安卓设备信息
ANDROID_CAPABILITIES = {
    "platformName": ANDROID,
    "platformVersion": "15",  # 安卓系统版本号
    "deviceName": "27c514b",  # adb devices 命令查询到的设备号
    "bundleId": "com.xxx.finosprite",  # app bundleId
    "appActivity": "com.xxx.xxx.MainActivity",  # 设置应用的主Activity
    "automationName": "UiAutomator2",
    "noReset":True, # 设置 False 表示需要清楚应用缓存，但不卸载APP
    "fullReset": False,  # 设置 True 表示需要卸载APP
}

# IOS设备信息
IOS_CAPABILITIES = {
    "platformName": IOS,
    "deviceName": "xxx的iPhone",  # 设备实际名称
    "bundleId": "com.xxx.xxx",  # 已安装应用的bundle ID
    "automationName": "XCUITest",
    "noReset": True,  # 设置 False 表示需要清楚应用缓存，但不卸载APP
    "fullReset": False,  # 设置 True 表示需要卸载APP
    # "platformVersion": "15.7.9",  # 设备实际的系统版本 
    "udid": "xxxxxx-00154DA03AB9802E",  # 设备的唯一标识符
    "platformVersion": "26.0",  # 设备实际的系统版本
    "scheme":"xxxxxxcec7395563d7"
}