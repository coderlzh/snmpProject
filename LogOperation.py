import os
import re


class OperationLog:
    """
    日志相关操作
    """

    def __init__(self):
        pass

    def logPrint(self, string):
        try:
            with open('./snmp-python.log', 'a+') as f:
                f.write(string + '\n')
        except:
            os.mknod("./snmp-python.log")
            with open('./snmp-python.log', 'a+') as f:
                f.write(string + '\n')

    def networkJsonPrint(self, string):
        try:

            with open('./networkInformation.txt', 'w') as f:
                f.write(string + '\n')
        except:
            os.mknod("./networkInformation.txt")
            with open('./networkInformation.txt', 'w') as f:
                f.write(string + '\n')

    def resultPrint(self, string):
        try:
            with open('./result.txt', 'w') as f:
                f.write(string + '\n')
        except:
            os.mknod("./result.txt")
            with open('./result.txt', 'w') as f:
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
    pass


if __name__ == '__main__':
    main()
