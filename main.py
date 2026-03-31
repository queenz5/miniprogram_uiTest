import shutil
import os
import argparse
import subprocess
import sys
from utils.ConfigParser_util import ConfigParser_util

def run_case(case_list):
    """
    执行测试用例（实时输出模式）
    Args:case_list: 测试用例列表
    """
    # 构造命令
    command = [sys.executable, "-m", "pytest"] + case_list.split() + ["-v"]
    
    try:
        print("开始执行测试...")
        print("=" * 50)

        # 实时输出模式 - 不捕获输出，直接显示在终端上
        result = subprocess.run(command)
        
        print("=" * 50)
        if result.returncode == 0:
            print("测试执行成功!")
            return True
        else:
            print("测试执行失败!")
            return False
            
    except Exception as e:
        print(f"错误: 执行pytest时出错: {str(e)}")
        return False

def get_test_case_path(platform):
    """
    获取测试用例配置文件路径
    Args:
        platform: 平台名称 ('android' 或 'ios')
    Returns:
        str: 配置文件路径
    """
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    if platform == "ios":
        return os.path.join(config_dir, 'testcases_ios.conf')
    else:  # android
        return os.path.join(config_dir, 'testcases_android.conf')

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='UI自动化测试执行器')
    parser.add_argument('--platform', choices=['android', 'ios'], default='android',help='指定测试平台 (默认: android)')
    args = parser.parse_args()
    
    # 创建报告文件夹
    reports_path = 'reports'
    if os.path.exists(reports_path):
        shutil.rmtree(reports_path)
    os.makedirs(reports_path)
    
    # 获取测试用例配置文件路径
    case_path = get_test_case_path(args.platform)
    try:
        # 读取测试用例
        config_parser = ConfigParser_util(case_path)
        case_list = config_parser.format_test_cases(platform=args.platform)
        if not case_list:
            print(f"警告: 在 {args.platform} 平台没有找到测试用例")
            return 0
        
        print(f"准备执行用例: {case_list}")
        
        # 执行测试
        success = run_case(case_list)
        
        # 返回执行结果
        return 0 if success else 1
        
    except Exception as e:
        print(f"错误: 执行测试时发生异常: {str(e)}")
        return 1

if __name__ == "__main__":
    '''
    # 获取启动参数,区分执行安卓还是IOS的用例，默认是执行安卓用例。
    # 安卓调用方式：python main.py --platform android
    # IOS 调用方式：python main.py --platform ios
    '''
    exit_code = main()
    sys.exit(exit_code)