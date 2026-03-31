
import os
import shutil

#新增用例，填这里的平台名称、测试用例模块/用例名称
platform = "android" # android or ios
moduleName = "view" # 填写conf 文件的模块名称

"""
这个文件的作用：
复制 f"testCase/{platform}/test_example.py"文件
重命名文件:命名为 f"testCase/{platform}/{moduleName}/test_{moduleName}.py"
修改类名称：将{testCaseName}.py 文件内容进行字符串替换，将类名“Test_example”替换成 f"Test_{moduleName}"
"""

src_file = f"testCase/{platform}/example/test_example.py"
dst_dir = f"testCase/{platform}/{moduleName}"
dst_file = f"testCase/{platform}/{moduleName}/test_{moduleName}.py"

# 判断目标文件夹是否存在
if os.path.exists(dst_file):
    print("用例文件已存在")
else:
    # 1. 复制文件
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src_file, dst_file)

    # 3. 替换 py 文件内容
    with open(dst_file, "r", encoding="utf-8") as f:
        py_content = f.read()
    py_content = py_content.replace("Test_example", f"Test_{moduleName}")
    with open(dst_file, "w", encoding="utf-8") as f:
        f.write(py_content)
    print("处理完成！")