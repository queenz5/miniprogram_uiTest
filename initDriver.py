"""
通用的驱动程序初始化工具函数。
"""
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from config.testData import  APPIUM_SERVER_URL,DEFAULT_TIMEOUT,ANDROID,IOS,ANDROID_CAPABILITIES,IOS_CAPABILITIES,demoAppid,apiServer
from urllib.parse import quote

class driver_util:
    # 全局计数器，从4开始计数，等于5时会执行1次 APP 冷启动，确保第一次执行时用例时 APP 会冷启动
    call_count = 4
    def __init__(self):
        pass

    def init_android_driver(self):
        """
        初始化 Android 驱动程序，默认不会打开应用，需要配合 android_startApplet 打开应用和启动小程序
        """
        # driver 初始化
        options = UiAutomator2Options()
        options.platform_name = ANDROID_CAPABILITIES["platformName"]
        options.platform_version = ANDROID_CAPABILITIES["platformVersion"]
        options.device_name = ANDROID_CAPABILITIES["deviceName"]
        # options.app_package = ANDROID_CAPABILITIES["bundleId"]
        # options.app_activity = ANDROID_CAPABILITIES["appActivity"]
        options.automation_name = ANDROID_CAPABILITIES["automationName"]
        options.no_reset = ANDROID_CAPABILITIES["noReset"]
        options.full_reset = ANDROID_CAPABILITIES["fullReset"]
        driver = webdriver.Remote(
            command_executor=APPIUM_SERVER_URL,
            options=options
        )
        return driver

    def android_startApplet(self,driver,pathAndQuery = '', appId = demoAppid, apiServer = apiServer, startApplet = True, startType = 'hot'):
        """
        传参数给 APP，APP接收到参数后打开小程序的指定页面
        driver:安卓驱动实例，由 init_android_driver 生成
        pathAndQuery:小程序启动参数，非必填，默认是空字符串，格式：path?query1=abc&query2=def
        appId:小程序的 appId，非必填，默认是 testData 设置的 appid
        apiServer:小程序的域名，非必填，默认是 testData 设置的域名
        startApplet:设置成 False 则只启动 APP ，不打开小程序
        startType: 设置成'cold',会执行 APP 冷启动，默认值是 'hot'
        """
        # 处理小程序启动参数
        path = None
        query = None
        extras = [],
        if not startApplet:
            extras = []
        elif '?' in pathAndQuery:
            path, query = pathAndQuery.split('?', 1)
            extras = [['s', 'apiServer', f'{quote(apiServer)}'], ['s', 'appId', f'{quote(appId)}'],['s', 'path', f'{quote(path)}'], ['s', 'query', f'{quote(query)}']]
        elif pathAndQuery != '' and '?' not in pathAndQuery:
            path = pathAndQuery
            extras = [['s', 'apiServer', f'{quote(apiServer)}'], ['s', 'appId', f'{quote(appId)}'],['s', 'path', f'{quote(path)}']]
        else:
            extras = [['s', 'apiServer', f'{quote(apiServer)}'], ['s', 'appId', f'{quote(appId)}']]

        # 启动APP并打开小程序
        try:
            # call_count=5 或者  startType=="cold" 时，会执行一次 APP 冷启动
            driver_util.call_count += 1
            coldStart = False
            if driver_util.call_count == 5 or startType=="cold":
                try:
                    driver.terminate_app(ANDROID_CAPABILITIES["bundleId"])
                    coldStart = True
                except Exception as e:
                    print(f"终止应用时出错: {e}")
                driver_util.call_count = 0

            # 构造启动参数
            start_args = {
                'intent': f"-n {ANDROID_CAPABILITIES['bundleId']}/{ANDROID_CAPABILITIES['appActivity']}",
                'extras': extras,
            }

            # 启动应用并传递参数
            driver.execute_script('mobile: startActivity', start_args)
            if coldStart:
                time.sleep(2)
        except Exception as e:
            print(f"启动应用时出错: {e}")

    def init_ios_driver(self):
        """
        初始化iOS驱动程序。默认不会打开应用，需要配合 ios_startApplet 打开应用和启动小程序
        """
        # driver 初始化
        options = XCUITestOptions()
        options.platform_name = IOS_CAPABILITIES["platformName"]
        options.platform_version = IOS_CAPABILITIES["platformVersion"]
        options.device_name = IOS_CAPABILITIES["deviceName"]
        options.udid = IOS_CAPABILITIES["udid"]
        options.automation_name = IOS_CAPABILITIES["automationName"]
        options.no_reset = IOS_CAPABILITIES["noReset"]
        options.full_reset = IOS_CAPABILITIES["fullReset"]
        options.show_xcode_log = True
        driver = webdriver.Remote(
            command_executor=APPIUM_SERVER_URL,
            options=options
        )
        return driver

    def ios_startApplet(self,driver,pathAndQuery = '', appId = demoAppid, apiServer = apiServer, startApplet = True, startType = 'hot'):
        """
        传参数给 APP，APP接收到参数后打开小程序的指定页面
        driver:IOS 驱动实例，由 init_ios_driver 生成
        pathAndQuery:小程序启动参数，非必填，默认是空字符串，格式：path?query1=abc&query2=def
        appId:小程序的 appId，非必填，默认是 testData 设置的 appid
        apiServer:小程序的域名，非必填，默认是 testData 设置的域名
        startApplet:设置成 False 则只启动 APP ，不打开小程序
        startType: 设置成'cold',会执行 APP 冷启动，默认值是 'hot'
        """
        # 处理小程序启动参数
        path = None
        query = None
        url = '',
        if not startApplet:
            url=''
        elif '?' in pathAndQuery:
            path, query = pathAndQuery.split('?', 1)
            apiServer_and_path_and_query = f"apiServer={quote(apiServer)}&path={quote(path)}&query={quote(query)}"
            url = f"{IOS_CAPABILITIES['scheme']}://applet/appid/{appId}?{apiServer_and_path_and_query}"
        elif pathAndQuery != '' and '?' not in pathAndQuery:
            path = pathAndQuery
            apiServer_and_path_and_query = f"apiServer={quote(apiServer)}&path={quote(path)}"
            url = f"{IOS_CAPABILITIES['scheme']}://applet/appid/{appId}?{apiServer_and_path_and_query}"
        else:
            apiServer_and_path_and_query = f"apiServer={quote(apiServer)}"
            url = f"{IOS_CAPABILITIES['scheme']}://applet/appid/{appId}?{apiServer_and_path_and_query}"

        # 启动APP并打开小程序
        try:
            # call_count=5 或者  startType=="cold" 时，会执行一次 APP 冷启动
            driver_util.call_count += 1
            coldStart = False
            if driver_util.call_count == 5 or startType=="cold":
                try:
                    driver.terminate_app(IOS_CAPABILITIES["bundleId"])
                    coldStart = True
                except Exception as e:
                    print(f"终止应用时出错: {e}")
                driver_util.call_count = 0

            # 构造启动参数
            launch_params = {
                'bundleId': IOS_CAPABILITIES["bundleId"],
                'url':url
            }
            # 启动应用并传递参数，如果是只启动APP不打开小程序，则使用 launchApp 方式打开，否则使用deepLink scheme 方式打开
            if url != '':
                driver.execute_script('mobile: deepLink', launch_params)
            else:
                driver.execute_script('mobile: launchApp', launch_params)
            if coldStart:
                time.sleep(3)
        except Exception as e:
            print(f"启动应用时出错: {e}")

    def startApplet(self,driver,pathAndQuery = '', appId = demoAppid, apiServer = apiServer, startApplet = True, startType = 'hot'):
        platform = driver.capabilities.get("platformName", "").lower()
        if "ios" in platform:
            # 调用 IOS 启动方法
            driver_util.ios_startApplet(self,driver,pathAndQuery, appId, apiServer, startApplet, startType)
        else:
            # 调用 安卓 启动方法
            driver_util.android_startApplet(self, driver, pathAndQuery, appId, apiServer, startApplet, startType)