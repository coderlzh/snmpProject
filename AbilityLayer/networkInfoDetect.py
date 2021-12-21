from utils import log_model, equip_model,cmdb_model,table_model,message_model,thread_model
import argparse
import json
import collections
from configparser import ConfigParser

CONFIGFILE = '../config/project.ini'
config = ConfigParser()
config.read(CONFIGFILE)
COMMUNITY = config['detection'].get('Community')
TARGET = config['detection'].get('Target')
PORT = config['detection'].get('Port')


def getTargetInfo(community,target,port,NeighborName):
    log.info(' Process Start To Get '+NeighborName + ' Information !')
    rt = equip_model.Router(community, target, port)
    dataJson, dataDict = rt.getAllInformation(whiteList=[])
    log.info(' Process End !')
    return dataJson, dataDict

def createThreads(community,port,inLevelNeighbor):
    threads = []
    for NeighborIP, NeighborName, NeighborSNID in inLevelNeighbor:
        if (NeighborName):
            t = thread_model.MyThread(target=getTargetInfo, args=(community,NeighborIP,port,NeighborName))
            threads.append(t)
    return threads

log = log_model.OperationLog()
@log.Detail2Log('DEBUG')
def networkInfoDetect(community=COMMUNITY,target=TARGET,port=PORT):
    rt = equip_model.Router(community, target, port)
    detection =rt.getName()
    snID = rt.getSNID()
    networkDict = {}
    neighborDiscovery = [[target, detection, snID]]
    inLevelNeighbor = neighborDiscovery
    nextLevelNeighbor = []
    while inLevelNeighbor:
        threads = createThreads(community, port, inLevelNeighbor)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        for t in threads:
            dataJson,dataDict = t.get_result()
            networkDict[t.get_args()] = dataDict
            for router in dataDict['neighborDict']['reachable']:
                if (router[2] in [i[2] for i in neighborDiscovery]):
                    continue
                else:
                    neighborDiscovery.append(router)
                    nextLevelNeighbor.append(router)
            for router in dataDict['neighborDict']['unreachable']:
                if (router in neighborDiscovery):
                    continue
                else:
                    neighborDiscovery.append(router)
                    nextLevelNeighbor.append(router)
        inLevelNeighbor = nextLevelNeighbor
        nextLevelNeighbor = []
    log.info('neighborDiscovery' + str(neighborDiscovery))
    log.resultPrint(str(neighborDiscovery))
    log.networkJsonPrint(json.dumps(networkDict, ensure_ascii=False, indent=4))
    to = table_model.OperationTable()
    dictUpdateList, dictInsertList, infoUpdateList, infoInsertList = to.insertTreeDict2Database()
    ms = message_model.OperationMessage()
    ReceiverList = []
    MessageSendFinal = ms.sendMessage2Kafka(ReceiverList)
    MessageJson = ms.message2json(MessageSendFinal)
    return MessageJson


def main():
    parser = argparse.ArgumentParser(description='本脚本通过snmp协议实现网络拓扑的发现与各路由器及活终端的监控')
    parser.add_argument('-C', '--community', help='set target router snmp community',default=COMMUNITY)
    parser.add_argument('-T', '--target', help='set target router ', default=TARGET)
    parser.add_argument('-P', '--port', help='set target router snmp port', default=PORT)
    args = parser.parse_args()
    log.info('start')
    #whiteList = log.getWhiteListIP('./test.log')
    rt = equip_model.Router(args.community, args.target, args.port)
    print("######################################")
    print('接入位置为：')
    detection =rt.getName()
    snID = rt.getSNID()
    neighborDiscovery = [[args.target, detection,snID]]
    #tb = TableOperation.OperationTable()
    cm = cmdb_model.OprationCMDB()
    #print(tb.createTableAll())
    print("######################################")
    print('发现开始：')
    networkDict = {}
    #neighborNameList = [detection]
    for NeighborIP,NeighborName,NeighborSNID in neighborDiscovery:
        if(NeighborName):
            rt = equip_model.Router('1q3e!Q#E', NeighborIP, '161')
            print('正在获取设备'+ NeighborIP +'的详细信息')
            try:
                dataJson,dataDict = rt.getAllInformation(whiteList=[])
                networkDict[NeighborName] = dataDict
                #cm.AllInformationPOST(dataDict)
                #tb.insertDictionary2Database(dataDict)
            except Exception as e:
                log.error(str(e))
                log.error("Get DataDict Error: " + NeighborName +" SNMPWALK TIME OUT! PLEASE CHECK IT.")
                continue
            for router in dataDict['neighborDict']['reachable']:
                if(router[2] in [i[2] for i in neighborDiscovery]):
                    continue
                else:
                    neighborDiscovery.append(router)
            for router in dataDict['neighborDict']['unreachable']:
                if(router in neighborDiscovery):
                    continue
                else:
                    neighborDiscovery.append(router)
            print(neighborDiscovery)
        else:
            #tb.insertSysName2Database(NeighborIP)
            continue
    #log.logPrint(str(neighborDiscovery))
    log.resultPrint(str(neighborDiscovery))
    log.networkJsonPrint(json.dumps(networkDict, ensure_ascii=False, indent=4))
    log.info('end')
if __name__ == '__main__':
    networkInfoDetect()