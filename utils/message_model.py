
import re
import json
from utils import log_model

log = log_model.OperationLog()
class OperationMessage:
    """
    信息相关操作
    """

    def __init__(self):
        pass

    @log.classFuncDetail2Log('DEBUG')
    def message2json(self,messagedict):
        return json.dumps(messagedict, ensure_ascii=False)

    @log.classFuncDetail2Log('DEBUG')
    def findDateFromMessage(self,message):
        date = re.search(r"([a-z]+(\s\s|\s)\d{1,2})", str(message), re.I).group()
        return date

    @log.classFuncDetail2Log('DEBUG')
    def findTimeFromMessage(self,message):
        time = re.search(r"([a-z]+(\s\s|\s)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\d{4})", str(message), re.I).group()
        return time

    @log.classFuncDetail2Log('DEBUG')
    def findTypeFromMessage(self,message):
        type = re.search(r'(\S+?)\s%%', message, re.I).group()
        return type[:-3]

    @log.classFuncDetail2Log('DEBUG')
    def findDetailFromMessage(self,message):
        patt = r'(.+?):\s'
        detail = re.sub(patt, "", message)
        patt = r'-'
        detail = re.sub(patt, "", detail)
        detail = re.findall(r'([a-z]+?):(.+?);``', detail)
        return detail

    @log.classFuncDetail2Log('DEBUG')
    def message2dict(self,date,type, time, detail):
        messagedict = {}
        messagedict['date'] = date
        messagedict['tabletype'] = type
        messagedict['time'] = time
        for i in detail:
            messagedict[i[0]] = i[1]
        return messagedict

    @log.classFuncDetail2Log('DEBUG')
    def messageGet(self,filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    @log.classFuncDetail2Log('DEBUG')
    def messageTranslate(self,messageDict):
        messageSend = {}
        messageSend['源IP'] = messageDict['sourceip']
        if(messageDict['logtype'] == 'attackprotect'):
            messageSend['目的IP'] = messageDict['destinationip']
            messageSend['攻击类型'] = messageDict['attacktype']
            messageSend['协议'] = messageDict['protocolname']
            if(messageDict['event'] == 'block'):
                messageSend['动作'] = '阻断'
            elif(messageDict['event'] == 'alert'):
                messageSend['动作'] = '告警'
        return messageSend

    @log.classFuncDetail2Log('DEBUG')
    def sendMessage2Kafka(self,receiverlist):
        message = {}
        message['type'] = 'note'
        message['content'] = '网络设备信息更新完毕，请注意检查。'
        message['receiver'] = '18344971196'
        #message['receiver'] ='|'.join(reciverlist)
        return message

    @log.classFuncDetail2Log('DEBUG')
    def messageProcess(self,message):
        date = self.findDateFromMessage(message)
        time = self.findTimeFromMessage(message)
        type = self.findTypeFromMessage(message)
        detail = self.findDetailFromMessage(message)
        messagedict = self.message2dict(date,type, time, detail)
        return messagedict

def main():
    pass

if __name__ == '__main__':
    main()
