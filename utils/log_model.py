import os
import re
import traceback
import functools
from utils import tool_model
from configparser import ConfigParser


CONFIGFILE = '../config/project.ini'
config = ConfigParser()
config.read(CONFIGFILE)

FilePath = config['log'].get('FilePath')

'''
DEBUG：程序调试bug时使用
INFO：程序正常运行时使用
WARNING：程序未按预期运行时使用，但并不是错误，如:用户登录密码错误
ERROR：程序出错误时使用，如:IO操作失败
CRITICAL：特别严重的问题，导致程序不能再继续运行时使用，如:磁盘空间为空，一般很少使 用
默认的是WARNING等级，当在WARNING或WARNING之上等级的才记录日志信息。
'''
configDict = {'DEBUG': 1,'INFO': 2 ,'WARNING':3,'ERROR':4,'CRITICAL':5}
Priority = configDict[config['log'].get('Priority')]

class OperationLog:
    """
    日志相关操作
    """

    def __init__(self):
        pass

    def classFuncDetail2Log(self,prefix):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kargs):
                if hasattr(self, prefix.lower()):
                    logFunc = getattr(self, prefix.lower())
                else:
                    raise
                logFunc(' FUNCTION {'+ func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ +'} BE EXCUTED.')
                try:
                    res = func(*args, **kargs)
                    logFunc(
                        ' FUNCTION {' + func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ + '} EXCUTE SUCCESSFULLY. ')
                    logFunc(
                        ' RETURN THE RESULT: \n' + str(res))
                    return res
                except:
                    self.error(
                        ' FUNCTION {' + func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ + '} EXCUTE FAILED UNEXPECTEDLY. RAISE THE ERROE : \n' + traceback.format_exc())
            return wrapper
        return decorator

    def Detail2Log(self,prefix):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kargs):
                logFunc = getattr(self, prefix.lower())
                logFunc(' FUNCTION {'+ func.__name__ + '} BE EXCUTED.')
                try:
                    res = func(*args, **kargs)
                    logFunc(
                        ' FUNCTION {' + func.__name__ + '} EXCUTE SUCCESSFULLY.')
                    logFunc(
                         ' RETURN THE RESULT: \n' + str(res))
                    return res
                except:
                    self.error(
                        ' FUNCTION {' + func.__name__ + '} EXCUTE FAILED UNEXPECTEDLY. RAISE THE ERROE : \n' + traceback.format_exc())
            return wrapper
        return decorator

    def info(self, string):
        if(Priority > 2):
            return
        filePath = FilePath + "snmp-python" + tool_model.getDate() + '.log'
        string = '[' + tool_model.getTime() + '] INFO ||' + string
        print(string)
        try:
            with open(filePath, 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod(filePath)
            with open(filePath, 'a+') as f:
                f.write(string + '\n')

    def debug(self, string):
        if(Priority > 1):
            return
        filePath = FilePath + "snmp-python" + tool_model.getDate() + '.log'
        string = '[' + tool_model.getTime() + '] DEBUG ||' + string
        print(string)
        try:
            with open(filePath, 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod(filePath)
            with open(filePath, 'a+') as f:
                f.write(string + '\n')

    def warn(self, string):
        if(Priority > 3):
            return
        filePath = FilePath + "snmp-python" + tool_model.getDate() + '.log'
        string = '[' + tool_model.getTime() + '] WARN ||' + string
        print(string)
        try:
            with open(filePath, 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod(filePath)
            with open(filePath, 'a+') as f:
                f.write(string + '\n')

    def error(self, string):
        if(Priority > 4):
            return
        filePath = FilePath + "snmp-python" + tool_model.getDate() + '.log'
        string = '[' + tool_model.getTime() + '] ERROR ||' + string
        print(string)
        try:
            with open(filePath, 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod(filePath)
            with open(filePath, 'a+') as f:
                f.write(string + '\n')

    def critical(self, string):
        filePath = FilePath + "snmp-python" + tool_model.getDate() + '.log'
        string = '[' + tool_model.getTime() + '] CRITICAL ||' + string
        print(string)
        try:
            with open(filePath, 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod(filePath)
            with open(filePath, 'a+') as f:
                f.write(string + '\n')

    def networkJsonPrint(self, string):
        try:
            with open('../logs/networkInformation.txt', 'w') as f:
                f.write(string + '\n')
        except:
            os.mknod("../logs/networkInformation.txt")
            with open('../logs/networkInformation.txt', 'w') as f:
                f.write(string + '\n')

    def resultPrint(self, string):
        try:
            with open('../logs/result.txt', 'w') as f:
                f.write(string + '\n')
        except:
            os.mknod("../logs/result.txt")
            with open('../logs/result.txt', 'w') as f:
                f.write(string + '\n')

    def getWhiteListIP(self, filepath):
        with open(filepath, 'r+') as f:
            str1 = f.read()
            pattern = re.compile(
                r'\[\'((([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5]))\', None, None\]')
            result = pattern.finditer(str1)
            whiteList = []
            for i in result:
                whiteList.append(i.group(1))
            return whiteList


def main():
    #log = OperationLog()
    #log.resultPrint('1111')
    cm = utils.cmdb_model.OprationCMDB()
    print(type(cm))


if __name__ == '__main__':
    main()
