import argparse
import json
from configparser import ConfigParser
import requests
from utils import log_model, equip_model, cmdb_model, table_model, message_model, network_model
from utils.tool_model import getTime


CONFIGFILE = '../config/project.ini'
config = ConfigParser()
config.read(CONFIGFILE)
COMMUNITY = config['detection'].get('Community')
TARGET = config['detection'].get('Target')
PORT = config['detection'].get('Port')



log = log_model.OperationLog()


@log.Detail2Log('DEBUG')
def hostListPOST():
    hostList = []
    net = network_model.OperationNetwork('../logs/networkInformation.txt')
    net.networkInfo_update()
    netDeviceInformationDict,_ = net.getNetDeviceInformationTreeDict()
    """
    [
        {
            "deviceType": 0,
            "heartbreakTime": "2021-12-24T02:37:02.014Z",
            "ip": "string",
            "mac": "string"
        }
    ]
    """
    for network,infoDict in netDeviceInformationDict.items():
        for ip,info in infoDict['host'].items():
            temp = {}
            temp["ip"] = ip
            mac, deviceType_string = info.split('/ ')
            temp["mac"] = mac
            if(deviceType_string.startswith('Micro') or deviceType_string.startswith('REALTEK') or deviceType_string.startswith('LCFC')):
                temp["deviceType"] = 1
            elif(deviceType_string.startswith('VM')):
                temp["deviceType"] = 2
            else:
                temp["deviceType"] = -1
            temp["heartbreakTime"] = getTime()
            hostList.append(temp)
    log.info(json.dumps(netDeviceInformationDict,indent=4))
    data = json.dumps(hostList, ensure_ascii=False,indent=4)
    url = 'http://10.46.97.234:9025/nlbomc-software-security/host/updateHost'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=data.encode("utf-8"), headers=headers)
    log.info(str(response.status_code))
    log.info(str(response.text))





@log.Detail2Log('DEBUG')
def networkInfoPOST():
    net = network_model.OperationNetwork('../logs/networkInformation.txt')
    net.networkInfo_update()
    to = table_model.OperationTable()
    dictUpdateList, dictInsertList, infoUpdateList, infoInsertList = to.insertTreeDict2Database()
    #ms = message_model.OperationMessage()
    #ReceiverList = []
    #MessageSendFinal = ms.sendMessage2Kafka(ReceiverList)
    #MessageJson = ms.message2json(MessageSendFinal)
    #return MessageJson


def main():
    parser = argparse.ArgumentParser(description='本脚本通过snmp协议实现网络拓扑的发现与各路由器及活终端的监控')
    parser.add_argument('-C', '--community', help='set target router snmp community', default=COMMUNITY)
    parser.add_argument('-T', '--target', help='set target router ', default=TARGET)
    parser.add_argument('-P', '--port', help='set target router snmp port', default=PORT)
    args = parser.parse_args()
    log.info('start')
    # whiteList = log.getWhiteListIP('./test.log')
    rt = equip_model.Router(args.community, args.target, args.port)
    print("######################################")
    print('接入位置为：')
    detection = rt.getName()
    snID = rt.getSNID()
    neighborDiscovery = [[args.target, detection, snID]]
    # tb = TableOperation.OperationTable()
    cm = cmdb_model.OprationCMDB()
    # print(tb.createTableAll())
    print("######################################")
    print('发现开始：')
    networkDict = {}
    # neighborNameList = [detection]
    for NeighborIP, NeighborName, NeighborSNID in neighborDiscovery:
        if (NeighborName):
            rt = equip_model.Router('1q3e!Q#E', NeighborIP, '161')
            print('正在获取设备' + NeighborIP + '的详细信息')
            try:
                dataJson, dataDict = rt.getAllInformation(whiteList=[])
                networkDict[NeighborName] = dataDict
                # cm.AllInformationPOST(dataDict)
                # tb.insertDictionary2Database(dataDict)
            except Exception as e:
                log.error(str(e))
                log.error("Get DataDict Error: " + NeighborName + " SNMPWALK TIME OUT! PLEASE CHECK IT.")
                continue
            for router in dataDict['neighborDict']['reachable']:
                if (router[2] in [i[2] for i in neighborDiscovery]):
                    continue
                else:
                    neighborDiscovery.append(router)
            for router in dataDict['neighborDict']['unreachable']:
                if (router in neighborDiscovery):
                    continue
                else:
                    neighborDiscovery.append(router)
            print(neighborDiscovery)
        else:
            # tb.insertSysName2Database(NeighborIP)
            continue
    # log.logPrint(str(neighborDiscovery))
    log.resultPrint(str(neighborDiscovery))
    log.networkJsonPrint(json.dumps(networkDict, ensure_ascii=False, indent=4))
    log.info('end')


if __name__ == '__main__':
    hostListPOST()
