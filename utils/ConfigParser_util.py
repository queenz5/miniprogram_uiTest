#!-*- coding: utf-8 -*-
import configparser
import os
import json
from collections import OrderedDict

class NewConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        # 保证 section 和 option 都是有序字典
        super().__init__(*args, dict_type=OrderedDict, **kwargs)

    #重写configparser.ConfigParser()方法，不将大写转换成小写
    def optionxform(self, optionstr):
        return optionstr


class ConfigParser_util:  
    def __init__(self,file):
        self.file = file
        self.newConfigParser = NewConfigParser()


    '''
    功能：读conf文件，返回dict类型
    参数：无
    '''
    def read_ConfigParser(self):
        self.newConfigParser.read(self.file,'utf8')
        data = json.loads(json.dumps(self.newConfigParser._sections,indent=2))
        return data
    
    '''
    功能：生成所有用例目录，用分号隔开。读conf文件，返回所有 main_key以及 main_key 下的 sub_key ，并拼接成字符串。
    例如： main_key1/sub_key1;main_key1/sub_key2;main_key2/sub_key2
    参数：无
    '''
    def format_test_cases(self,platform):
        caseObj = self.read_ConfigParser()
        result = []
        for outer_key, inner_dict in caseObj.items():
            for inner_key in inner_dict.keys():
                formatted_item = f"testCase/{platform}/{outer_key}/test_{outer_key}.py::Test_{outer_key}::test_{inner_key}"
                result.append(formatted_item)
        
        return " ".join(result)

    '''
    功能：根据指定的 main_key,sub_key,返回value
    参数：main_key,sub_key
    '''
    def get_value(self,main_key,sub_key):
        value = self.read_ConfigParser()[main_key][sub_key]
        return value

    '''
    功能：判断key是否存在
    参数：无
    '''  
    def hasKey(self,main_key,sub_key):
        value = self.read_ConfigParser()
        if main_key in value:
            value = self.read_ConfigParser()[main_key]
            if sub_key in value:
                return True
            else:
                return False
        else:
            return False

        
    '''
    功能：更新conf文件;
    参数：main_key,sub_key,value；
    '''
    def update_conf(self,main_key,sub_key,value):
        self.newConfigParser.read(self.file)
        if self.newConfigParser.__contains__(main_key) == False:
            self.newConfigParser.add_section(main_key)
        self.newConfigParser.set(main_key,sub_key,value)
        with open(self.file,'w') as fp:
            self.newConfigParser.write(fp)
    

if __name__ == "__main__":
    configPath = os.path.dirname(__file__) + '/../conf/testcases.conf'
    con_obj = ConfigParser_util(configPath)
    print (configPath)
    print (con_obj.hasKey("devices","ios1"))
    print (con_obj.read_ConfigParser())
    print (con_obj.format_test_cases())
    
    # print con_obj.get_value("staff_user2","param")
    # con_obj.update_conf("2s","3","4")