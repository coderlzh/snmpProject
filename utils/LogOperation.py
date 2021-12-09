import os
import re
import traceback
from utils import ToolOperation

class OperationLog:
    """
    日志相关操作
    """

    def __init__(self):
        pass

    def classFuncDetail2Log(self,prefix):
        def decorator(func):
            def wrapper(*args, **kargs):
                self.logPrint('['+ ToolOperation.getTime()  +'] ' + prefix + ' || FUNCTION {'+ func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ +'} BE EXCUTED.' )
                try:
                    res = func(*args, **kargs)
                    self.logPrint(
                        '[' + ToolOperation.getTime() + '] ' + prefix + ' || FUNCTION {' + func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ + '} EXCUTE SUCCESSFULLY. ')
                    return res
                except:
                    self.logPrint(
                        '[' + ToolOperation.getTime() + '] ' + 'WARN || FUNCTION {' + func.__name__ + '} IN CLASS {' + args[0].__class__.__name__ + '} EXCUTE FAILED UNEXPECTLY. RAISE THE ERROE : \n' + traceback.format_exc())
            return wrapper
        return decorator

    def logPrint(self, string):
        filePath = '../logs/snmp-python' + ToolOperation.getDate() + '.log'
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
    log = OperationLog()
    log.resultPrint('1111')


if __name__ == '__main__':
    main()
