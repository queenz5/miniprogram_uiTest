import pytest
from initDriver import driver_util
from utils.base import Base
from utils.pytesseract_util import *
from utils.assertUtil import AssertionUtil


class Test_File:
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

    def test_file(self):
        testCaseDescription = "测试用例：\n\
        case1:saveFile保存临时文件到本地成功\n\
        case2:getSavedFileList获取该小程序下已保存的本地缓存文件列表成功\n\
        case3:getSavedFileInfo获取该小程序下已保存的本地缓存文件信息成功\n\
        case4:getFileInfo获取该小程序下的 本地临时文件或本地缓存文件信息成功\n\
        case5:removeSavedFile删除该小程序下已保存的本地缓存文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/File/index')
        self.assertionUtil.check_text_exist(self.driver, "saveFile_test_success", "ch", wait_time=5, fail_msg="saveFile测试失败")
        self.assertionUtil.check_text_exist(self.driver, "getSavedFileList_test_success", "ch", fail_msg="getSavedFileList测试失败")
        self.assertionUtil.check_text_exist(self.driver, "getSavedFileinfo_test_success", "ch", fail_msg="getSavedFileinfo测试失败")
        self.assertionUtil.check_text_exist(self.driver, "getFileinfo_test_success", "ch", fail_msg="getFileinfo测试失败")
        self.assertionUtil.check_text_exist(self.driver, "removeSavedFile_test_success", "ch", fail_msg="removeSavedFile测试失败")

    def test_FileSystemManager(self):
        testCaseDescription = "测试用例：\n\
        case1:FileSystemManager.access判断本地文件地址temp、store、usr地址判断正确\n\
        case2:FileSystemManager.accessSync判断本地文件地址temp、store、usr地址判断正确\n\
        case3:FileSystemManager.saveFile保存临时文件到本地成功\n\
        case4:FileSystemManager.saveFileSync保存临时文件到本地成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=access')
        self.assertionUtil.check_text_exist(self.driver, "access_ok", "ch", wait_time=5,
                                            fail_msg="access测试失败")
        self.assertionUtil.check_text_exist(self.driver, "accessSync_ok", "ch",
                                            fail_msg="accessSync测试失败")
        self.assertionUtil.check_text_exist(self.driver, "saveFile/saveFileSync_success", "ch",
                                            fail_msg="saveFile测试失败")

    def test_FileSystemManager2(self):
        testCaseDescription = "测试用例：\n\
        case5:FileSystemManager.open打开文件，返回文件描述符正确\n\
        case6:FileSystemManager.openSync打开文件，返回文件描述符正确\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=open')
        self.assertionUtil.check_text_exist(self.driver, "open/openSync_success", "ch", wait_time=5,
                                            fail_msg="open测试失败")

    def test_FileSystemManager3(self):
        testCaseDescription = "测试用例：\n\
        case7:FileSystemManager.appendFile在文件结尾追加内容成功\n\
        case8:FileSystemManager.appendFileSync在文件结尾追加内容成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=appendFile')
        self.assertionUtil.check_text_exist(self.driver, "appendFile/appendFileSync_success", "ch", wait_time=5,
                                            fail_msg="appendFile测试失败")

    def test_FileSystemManager4(self):
        testCaseDescription = "测试用例：\n\
        case9:FileSystemManager.close关闭文件成功\n\
        case10:FileSystemManager.closeSync关闭文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=close')
        self.assertionUtil.check_text_exist(self.driver, "close/closeSync_success", "ch", wait_time=5,
                                            fail_msg="close测试失败")

    def test_FileSystemManager5(self):
        testCaseDescription = "测试用例：\n\
        case11:FileSystemManager.copyFile复制文件成功\n\
        case12:FileSystemManager.copyFileSync复制文件成功\n\
        case13:FileSystemManager.readFile读取本地文件内容成功\n\
        case14:FileSystemManager.readFileSync读取本地文件内容成功\n\
        case15:FileSystemManager.writeFile写文件成功\n\
        case16:FileSystemManager.writeFileSync写文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=copy')
        self.assertionUtil.check_text_exist(self.driver, "copy/copySync_success", "ch", wait_time=5,
                                            fail_msg="copy测试失败")
        self.assertionUtil.check_text_exist(self.driver, "readFile/readFileSync_success", "ch",
                                            fail_msg="readFile测试失败")
        self.assertionUtil.check_text_exist(self.driver, "writeFile/writeFileSync_success", "ch",
                                            fail_msg="writeFile测试失败")

    def test_FileSystemManager6(self):
        testCaseDescription = "测试用例：\n\
        case17:FileSystemManager.fstat获取文件的状态信息成功\n\
        case18:FileSystemManager.fstatSync获取文件的状态信息成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=fstat')
        self.assertionUtil.check_text_exist(self.driver, "fstat/fstatSync_success", "ch", wait_time=5,
                                            fail_msg="fstat测试失败")

    def test_FileSystemManager7(self):
        testCaseDescription = "测试用例：\n\
        case19:FileSystemManager.ftruncate对文件内容进行截断操作成功\n\
        case20:FileSystemManager.ftruncateSync对文件内容进行截断操作成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=ftruncate')
        self.assertionUtil.check_text_exist(self.driver, "ftruncate/ftruncateSync_success", "ch", wait_time=5,
                                            fail_msg="ftruncate测试失败")

    def test_FileSystemManager8(self):
        testCaseDescription = "测试用例：\n\
        case21:FileSystemManager.mkdir创建目录成功\n\
        case22:FileSystemManager.mkdirSync创建目录成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=mkdir')
        self.assertionUtil.check_text_exist(self.driver, "mkdir/mkdirSync_success", "ch", wait_time=5,
                                            fail_msg="mkdir测试失败")

    def test_FileSystemManager9(self):
        testCaseDescription = "测试用例：\n\
        case23:FileSystemManager.read读文件成功\n\
        case24:FileSystemManager.readSync读文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=read')
        self.assertionUtil.check_text_exist(self.driver, "read/readSync_success", "ch", wait_time=5,
                                            fail_msg="read/readSync测试失败")

    def test_FileSystemManager10(self):
        testCaseDescription = "测试用例：\n\
        case25:FileSystemManager.readdir读取目录内文件列表成功\n\
        case26:FileSystemManager.readdirSync读取目录内文件列表成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=readdir')
        self.assertionUtil.check_text_exist(self.driver, "readdir/readdirSync_success", "ch", wait_time=5,
                                            fail_msg="readdir/readdirSync测试失败")

    def test_FileSystemManager11(self):
        testCaseDescription = "测试用例：\n\
        case27:FileSystemManager.removeSavedFile删除该小程序下已保存的本地缓存文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=removeSavedFile')
        self.assertionUtil.check_text_exist(self.driver, "removeSavedFile_success", "ch", wait_time=5,
                                            fail_msg="removeSavedFile测试失败")

    def test_FileSystemManager12(self):
        testCaseDescription = "测试用例：\n\
        case28:FileSystemManager.rename重命名文件成功\n\
        case29:FileSystemManager.renameSync重命名文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=rename')
        self.assertionUtil.check_text_exist(self.driver, "rename/renameSync_success", "ch", wait_time=5,
                                            fail_msg="rename/renameSync测试失败")

    def test_FileSystemManager13(self):
        testCaseDescription = "测试用例：\n\
        case30:FileSystemManager.rmdir删除目录成功\n\
        case31:FileSystemManager.rmdirSync删除目录成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=rmdir')
        self.assertionUtil.check_text_exist(self.driver, "rmdir/rmdirSync_success", "ch", wait_time=5,
                                            fail_msg="rmdir/rmdirSync测试失败")

    def test_FileSystemManager14(self):
        testCaseDescription = "测试用例：\n\
        case32:FileSystemManager.stat获取文件 Stats 对象成功\n\
        case33:FileSystemManager.statSync获取文件 Stats 对象成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=stat')
        self.assertionUtil.check_text_exist(self.driver, "stat/statSync_success", "ch", wait_time=5,
                                            fail_msg="stat/statSync测试失败")

    def test_FileSystemManager15(self):
        testCaseDescription = "测试用例：\n\
        case34:FileSystemManager.truncate对文件内容进行截断操作成功\n\
        case35:FileSystemManager.truncateSync对文件内容进行截断操作成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=truncate')
        self.assertionUtil.check_text_exist(self.driver, "truncate/truncateSync_success", "ch", wait_time=5,
                                            fail_msg="truncate/truncateSync测试失败")

    def test_FileSystemManager16(self):
        testCaseDescription = "测试用例：\n\
        case36:FileSystemManager.unlink删除文件成功\n\
        case37:FileSystemManager.unlinkSync删除文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=unlink')
        self.assertionUtil.check_text_exist(self.driver, "unlink/unlinkSync_success", "ch", wait_time=5,
                                            fail_msg="unlink/unlinkSync测试失败")

    def test_FileSystemManager17(self):
        testCaseDescription = "测试用例：\n\
        case38:FileSystemManager.write写入文件成功\n\
        case39:FileSystemManager.writeSync写入文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=write')
        self.assertionUtil.check_text_exist(self.driver, "write/writeSync_success", "ch", wait_time=5,
                                            fail_msg="write/writeSync测试失败")

    def test_FileSystemManager18(self):
        testCaseDescription = "测试用例：\n\
        case40:FileSystemManager.unzip解压文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=unzip')
        self.assertionUtil.check_text_exist(self.driver, "unzip_success", "ch", wait_time=5,
                                            fail_msg="unzip测试失败")

    def test_FileSystemManager19(self):
        testCaseDescription = "测试用例：\n\
        case41:FileSystemManager.getSavedFileList获取该小程序下已保存的本地缓存文件列表成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=getSavedFileList')
        self.assertionUtil.check_text_exist(self.driver, "getSavedFileList_success", "ch", wait_time=5,
                                            fail_msg="getSavedFileList测试失败")

    def test_FileSystemManager20(self):
        testCaseDescription = "测试用例：\n\
        case42:FileSystemManager.getFileInfo获取该小程序下的 本地临时文件或本地缓存文件信息成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=getFileInfo')
        self.assertionUtil.check_text_exist(self.driver, "getFileinfo_success", "ch", wait_time=5,
                                            fail_msg="getFileinfo测试失败")

    def test_FileSystemManager21(self):
        testCaseDescription = "测试用例：\n\
        case43:FileSystemManager.readZipEntry读取压缩包内的文件成功\n\
        "
        print(testCaseDescription)
        self.driver_util.startApplet(driver=self.driver,pathAndQuery = 'packageAPI/pages/FileSystemManager/writefile?testCase=readZipEntry')
        self.assertionUtil.check_text_exist(self.driver, "readZipEntry_success", "ch", wait_time=5,
                                            fail_msg="readZipEntry测试失败")