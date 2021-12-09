from utils import LogOperation, RouterOperation,CMDBOperation
import argparse
import json

def excuteByInterface(community='1q3e!Q#E',target='10.46.79.126',port='161'):
    log = LogOperation.OperationLog()
    rt = RouterOperation.OperationRouter(community, target, port)
    detection =rt.getRouterName()
    snID = rt.getRouterSNID()
    neighborDiscovery = [[target, detection, snID]]
    networkDict = {}
    for NeighborIP, NeighborName, NeighborSNID in neighborDiscovery:
        if (NeighborName):
            rt = RouterOperation.OperationRouter('1q3e!Q#E', NeighborIP, '161')
            try:
                dataJson, dataDict = rt.getRouterAllInformation(whiteList=[])
                networkDict[NeighborName] = dataDict
                # cm.AllInformationPOST(dataDict)
                # tb.insertDictionary2Database(dataDict)
            except Exception as e:
                log.logPrint(str(e))
                log.logPrint("Get DataDict Error! " + NeighborName + " SNMPWALK TIME OUT! PLEASE CHECK IT.")
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
        else:
            # tb.insertSysName2Database(NeighborIP)
            continue
    #log.logPrint(str(neighborDiscovery))
    log.resultPrint(str(neighborDiscovery))
    log.networkJsonPrint(json.dumps(networkDict, ensure_ascii=False, indent=4))

def main():
    parser = argparse.ArgumentParser(description='本脚本通过snmp协议实现网络拓扑的发现与各路由器及活终端的监控')
    parser.add_argument('-C', '--community', help='set target router snmp community',default='1q3e!Q#E')
    parser.add_argument('-T', '--target', help='set target router ', default='10.46.79.126')
    parser.add_argument('-P', '--port', help='set target router snmp port', default='161')
    args = parser.parse_args()
    log = LogOperation.OperationLog()
    #whiteList = log.getWhiteListIP('./test.log')
    rt = RouterOperation.OperationRouter(args.community, args.target, args.port)
    print("######################################")
    print('接入位置为：')
    detection =rt.getRouterName()
    snID = rt.getRouterSNID()
    neighborDiscovery = [[args.target, detection,snID]]
    #tb = TableOperation.OperationTable()
    cm = CMDBOperation.OprationCMDB()
    #print(tb.createTableAll())
    print("######################################")
    print('发现开始：')
    networkDict = {}
    #neighborNameList = [detection]
    for NeighborIP,NeighborName,NeighborSNID in neighborDiscovery:
        if(NeighborName):
            rt = RouterOperation.OperationRouter('1q3e!Q#E', NeighborIP, '161')
            print('正在获取设备'+ NeighborIP +'的详细信息')
            try:
                dataJson,dataDict = rt.getRouterAllInformation(whiteList=[])
                log.logPrint(dataJson)
                networkDict[NeighborName] = dataDict
                #cm.AllInformationPOST(dataDict)
                #tb.insertDictionary2Database(dataDict)
            except Exception as e:
                print(e)
                log.logPrint(str(e))
                log.logPrint("Get DataDict Error! " + NeighborName +" SNMPWALK TIME OUT! PLEASE CHECK IT.")
                print("Get DataDict Error: " + NeighborName +" SNMPWALK TIME OUT! PLEASE CHECK IT.")
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

if __name__ == '__main__':
    main()