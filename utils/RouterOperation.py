import json
from utils import LogOperation, TableOperation, SnmpOperation
import IPy

log = LogOperation.OperationLog()

class OperationRouter:
    """
    单台路由器相关操作
    """

    def __init__(self, community, target, port):
        self.community = community
        self.target = target
        self.port = port

        self.routerSysInformationDict = None
        self.routerRouteInformationDict = None
        self.routerInterfaceInformationDict = None
        self.routerRelativeInformationDict = None
        self.routerAllInformationDict = None
        self.routerNeighborInformationDict = None

    @log.classFuncDetail2Log('DEBUG')
    def getRouterInterfaceListAndIp(self):
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            [interfaceIpList, interfaceIdList] = sn.walk(['1.3.6.1.2.1.4.20.1.1', '1.3.6.1.2.1.4.20.1.2'])
            oidList = []
            for interfaceId in interfaceIdList:
                oidList.append('1.3.6.1.2.1.2.2.1.2.' + interfaceId)
            interfaceDescList = sn.getbulk(oidList)
            # print(list(zip(interfaceIpList,interfaceDescList)))
            return [interfaceIpList, interfaceDescList]

    @log.classFuncDetail2Log('DEBUG')
    def getRouterName(self):
            print(self.target)
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            name = sn.getbulk(['1.3.6.1.2.1.1.5.0'])
            if (bool(name)):
                return name[0]
            else:
                return None

    @log.classFuncDetail2Log('DEBUG')
    def getRouterSNID(self):
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.16777216'])
            if ID[0].startswith("No Such") or not bool(ID[0]):
                ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.67108867'])
                if ID[0].startswith("No Such") or not bool(ID[0]):
                    ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.2'])
                    if ID[0].startswith("No Such") or not bool(ID[0]):
                        ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.1'])
                        if ID[0].startswith("No Such") or not bool(ID[0]):
                            ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.1207967776'])
                            if ID[0].startswith("No Such") or not bool(ID[0]):
                                ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.9'])
                                if ID[0].startswith("No Such") or not bool(ID[0]):
                                    ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.603979777'])
                                    if ID[0].startswith("No Such") or not bool(ID[0]):
                                        ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.69992457'])
                                        if ID[0].startswith("No Such") or not bool(ID[0]):
                                            sn.walk(['1.3.6.1.2.1.47.1.1.1.1.11'])
                                            ID = sn.getbulk(['1.3.6.1.2.1.47.1.1.1.1.11.1207967776'])
                                            if ID[0].startswith("No Such"):
                                                result = ID[0] + self.getRouterName()
                                                return result
            print(ID[0])
            return ID[0]

    @log.classFuncDetail2Log('DEBUG')
    def getRouterForwarding(self):
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            name = sn.getbulk(['1.3.6.1.2.1.4.1.0'])
            if (bool(name)):
                return name[0]
            else:
                return None

    @log.classFuncDetail2Log('DEBUG')
    def getRouterNexthopsListAndType(self):
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            [NexthopsList, NexthopsType] = sn.walk(['1.3.6.1.2.1.4.21.1.7', '1.3.6.1.2.1.4.21.1.8'])
            # print(list(zip(NexthopsList, NexthopsType)))
            return [NexthopsList, NexthopsType]

    @log.classFuncDetail2Log('DEBUG')
    def getRouterSysInformationDict(self):
        #print('function getRouterSysInformationDict')
            result = {}
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            print(sn.walk(['1.3.6.1.2.1.1'])[0])
            result['sysSNID'] = self.getRouterSNID()
            result['sysDescr'] = sn.getbulk(['1.3.6.1.2.1.1.1.0'])[0]
            result['sysObjectID'] = sn.getbulk(['1.3.6.1.2.1.1.2.0'])[0]
            result['sysUpTime'] = sn.getbulk(['1.3.6.1.2.1.1.3.0'])[0]
            result['sysContact'] = sn.getbulk(['1.3.6.1.2.1.1.4.0'])[0]
            result['sysName'] = sn.getbulk(['1.3.6.1.2.1.1.5.0'])[0]
            result['sysLocation'] = sn.getbulk(['1.3.6.1.2.1.1.6.0'])[0]
            result['sysSevices'] = sn.getbulk(['1.3.6.1.2.1.1.7.0'])[0]
            result['sysIfNumber'], result['sysForwarding'] = sn.getbulk(['1.3.6.1.2.1.2.1.0', '1.3.6.1.2.1.4.1.0'])
            return result

    @log.classFuncDetail2Log('DEBUG')
    def getRouterInterfaceInformationDict(self):
        #print('function getRouterInterfaceInformationDict')
            result = {}
            interface = {}
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            result['sysSnID'] = self.getRouterSNID()
            result['interfaceID'], result['interfaceName'], result['interfacePhysAddress'], result[
                'interfaceAdminStatus'], \
            result['interfaceOperStatus'], result['interfaceLastChange'], result['interfaceDesc'] = sn.walk(
                ['1.3.6.1.2.1.2.2.1.1', '1.3.6.1.2.1.2.2.1.2', '1.3.6.1.2.1.2.2.1.6', '1.3.6.1.2.1.2.2.1.7',
                 '1.3.6.1.2.1.2.2.1.8', '1.3.6.1.2.1.2.2.1.9', '1.3.6.1.2.1.31.1.1.1.18'])
            for i in range(len(result['interfaceID'])):
                temp = {}
                temp['interfaceUniqueID'], temp['interfaceID'], temp['interfaceName'], temp['interfacePhysAddress'], \
                temp['interfaceAdminStatus'], \
                temp['interfaceOperStatus'], temp['interfaceLastChange'], temp['interfaceDesc'] = result[
                                                                                                      'sysSnID'] + 'InterfaceID' + \
                                                                                                  result['interfaceID'][
                                                                                                      i], \
                                                                                                  result['interfaceID'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfaceName'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfacePhysAddress'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfaceAdminStatus'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfaceOperStatus'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfaceLastChange'][
                                                                                                      i], \
                                                                                                  result[
                                                                                                      'interfaceDesc'][
                                                                                                      i]
                temp['interfaceIP'] = ''
                temp['interfaceNetmask'] = ''
                interface[result['interfaceID'][i]] = temp
            result['interfaceIP'], result['interfaceNetmask'], ipInterfaces = sn.walk(
                ['1.3.6.1.2.1.4.20.1.1', '1.3.6.1.2.1.4.20.1.3', '1.3.6.1.2.1.4.20.1.2'])
            for i in range(len(ipInterfaces)):
                interface[ipInterfaces[i]]['interfaceIP'] = result['interfaceIP'][i]
                interface[ipInterfaces[i]]['interfaceNetmask'] = result['interfaceNetmask'][i]
            if ('0' not in interface):
                interface['0'] = {}
                interface['0']['interfaceUniqueID'] = result['sysSnID'] + 'SpecialInterface'
                interface['0']['interfaceID'] = '0'
                interface['0']['interfaceName'] = 'SpecialInterface'
                interface['0']['interfacePhysAddress'] = '0x000000000000'
                interface['0']['interfaceAdminStatus'] = ''
                interface['0']['interfaceOperStatus'] = ''
                interface['0']['interfaceLastChange'] = ''
                interface['0']['interfaceDesc'] = ''
                interface['0']['interfaceNetmask'] = ''
                interface['0']['interfaceIP'] = 'No Interface Ip Be Selected.'
            return interface

    @log.classFuncDetail2Log('DEBUG')
    def getWhichInterfaceDestinationIPOut(self, ipaddress, dataDict):
        maxNet = IPy.IP('0.0.0.0')
        resultIfIndex = ''
        resultIfIp = ''
        """
                    "11": {
                        "routerUniqueID": "G1MQ38C70049C192.167.7.0",
                        "routerDest": "192.167.7.0",
                        "routerIfIndex": "0",
                        "routerIfIP": "No Interface Ip Be Selected.",
                        "routerNextHop": "192.167.25.34",
                        "routerMask": "255.255.255.128"
                    },
        """
        for key, routerDict in dataDict.items():
            if (ipaddress in IPy.IP(routerDict['routerDest']).make_net(routerDict['routerMask'])):
                if (IPy.IP(routerDict['routerMask']) >= maxNet):
                    maxNet = IPy.IP(routerDict['routerMask'])
                    resultIfIndex = routerDict['routerIfIndex']
                    resultIfIp = routerDict['routerIfIP']
        return resultIfIndex,resultIfIp

    @log.classFuncDetail2Log('DEBUG')
    def getRouterRouterInformationDict(self):
        #print('function getRouterRouterInformationDict')
            if not self.routerInterfaceInformationDict:
                self.routerInterfaceInformationDict = self.getRouterInterfaceInformationDict()
            result = {}
            router = {}
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            result['sysSnID'] = self.getRouterSNID()
            result['routerDest'], result['routerIfIndex'], result['routerNextHop'], \
            result['routerMask'] = sn.walk(
                ['1.3.6.1.2.1.4.21.1.1', '1.3.6.1.2.1.4.21.1.2', '1.3.6.1.2.1.4.21.1.7',
                 '1.3.6.1.2.1.4.21.1.11'])
            for i in range(len(result['routerDest'])):
                temp = {}
                temp['routerUniqueID'], temp['routerDest'], temp['routerIfIndex'], temp['routerIfIP'], temp[
                    'routerNextHop'], \
                temp['routerMask'] = result['sysSnID'] + 'Router' + result['routerDest'][i], result['routerDest'][i], \
                                     result['routerIfIndex'][i], \
                                     self.routerInterfaceInformationDict[result['routerIfIndex'][i]]['interfaceIP'], \
                                     result['routerNextHop'][i], \
                                     result['routerMask'][i]
                router[str(i)] = temp
            for key,routerDict in router.items():
                if(routerDict['routerIfIndex'] == '0'):
                    routerDict['routerIfIndex'],routerDict['routerIfIP'] = self.getWhichInterfaceDestinationIPOut(routerDict['routerNextHop'],router)
            return router

    @log.classFuncDetail2Log('DEBUG')
    def getRouterRelativeInformationDict(self, terminalSnmpUnenabledList=None):
            if not self.routerInterfaceInformationDict:
                self.routerInterfaceInformationDict = self.getRouterInterfaceInformationDict()
            result = {}
            relative = {}
            sn = SnmpOperation.OperationSnmp(self.community, self.target, self.port)
            result['sysSnID'] = self.getRouterSNID()
            result['localInterfaceID'], result['peerInterfaceIP'], \
            result['peerInterfacePhysAddress'] = sn.walk(
                ['1.3.6.1.2.1.4.22.1.1', '1.3.6.1.2.1.4.22.1.3',
                 '1.3.6.1.2.1.4.22.1.2'])
            for i in range(len(result['localInterfaceID'])):
                temp = {}
                temp['relativeUniqueID'], temp['localInterfaceID'], temp['localInterfaceIP'], temp['peerInterfaceIP'], \
                temp[
                    'peerInterfacePhysAddress'] \
                    = result['sysSnID'] + 'RelativeIP' + result['peerInterfaceIP'][i], result['localInterfaceID'][i], \
                      self.routerInterfaceInformationDict[result['localInterfaceID'][i]]['interfaceIP'], \
                      result['peerInterfaceIP'][i], \
                      result['peerInterfacePhysAddress'][i]
                temp['peerSysName'] = ''
                temp['peerSysForwarding'] = ''
                relative[temp['peerInterfaceIP']] = temp
            return  relative
            # for terminalSnmpUnenabled in terminalSnmpUnenabledList:
            #     relative[terminalSnmpUnenabled]['peerSysName'] = 'unknown'
            #     relative[terminalSnmpUnenabled]['peerSysForwarding'] = 'unknown'
            # for i in relative:
            #     if(relative[i]['peerSysName']):
            #         continue
            #     else:
            #         rt = OperationRouter('1q3e!Q#E',relative[i]['peerInterfaceIP'], '161')
            #         relative[i]['peerSysName'] = rt.getRouterName()
            #         if(relative[i]['peerSysName']):
            #             relative[i]['peerSysForwarding'] = rt.getRouterForwarding()
            #         else:
            #             continue
            # return [interfacedict, relative]

    @log.classFuncDetail2Log('DEBUG')
    def getRouterNeighborInformationDict(self, whiteList=None):
        #print('function getRouterNeighborInformationDict')
            if not self.routerRouteInformationDict:
                self.routerRouteInformationDict = self.getRouterRouterInformationDict()
            if not self.routerSysInformationDict:
                self.routerSysInformationDict = self.getRouterSysInformationDict()
            if not self.routerRelativeInformationDict:
                self.routerRelativeInformationDict = self.getRouterRelativeInformationDict()
            resultIP = {}
            resultIP['unreachable'] = []
            resultIP['reachable'] = []
            routerSelf = []
            for i in range(len(self.routerRouteInformationDict)):
                if (self.routerRouteInformationDict[str(i)]['routerNextHop'] == '0.0.0.0' or self.routerRouteInformationDict[str(i)][
                    'routerNextHop'] == '127.0.0.1' or self.routerRouteInformationDict[str(i)]['routerNextHop'] in resultIP or
                        self.routerRouteInformationDict[str(i)]['routerNextHop'] in [i[0] for i in resultIP['reachable']] or
                        self.routerRouteInformationDict[str(i)][
                            'routerNextHop'] in [i[0] for i in resultIP['unreachable']] or self.routerRouteInformationDict[str(i)][
                            'routerNextHop'] in whiteList or self.routerRouteInformationDict[str(i)]['routerNextHop'] in routerSelf):
                    continue
                else:
                    rt = OperationRouter('1q3e!Q#E', self.routerRouteInformationDict[str(i)]['routerNextHop'], '161')
                    nexthopName = rt.getRouterName()
                    if not nexthopName:
                        resultIP['unreachable'].append([self.routerRouteInformationDict[str(i)]['routerNextHop'], None, None])
                        continue
                    nexthopID = rt.getRouterSNID()
                    if (nexthopName == self.routerSysInformationDict['sysName']):
                        routerSelf.append(self.routerRouteInformationDict[str(i)]['routerNextHop'])
                        continue
                    else:
                        if (nexthopName and nexthopID):
                            resultIP['reachable'].append([self.routerRouteInformationDict[str(i)]['routerNextHop'], nexthopName, nexthopID])
                        elif (nexthopName):
                            resultIP['reachable'].append([self.routerRouteInformationDict[str(i)]['routerNextHop'], nexthopName, None])
                        else:
                            resultIP['unreachable'].append([self.routerRouteInformationDict[str(i)]['routerNextHop'], None, None])
            return resultIP
        #     resultIP = {}
        #     resultIP['unreachable'] = []
        #     resultIP['reachable'] = []
        #     return resultIP
    @log.classFuncDetail2Log('DEBUG')
    def getRouterAllInformation(self, whiteList=None):
        routerAllInformationDict = {}
        if not self.routerInterfaceInformationDict:
            self.routerInterfaceInformationDict = self.getRouterInterfaceInformationDict()
        if not self.routerSysInformationDict:
            self.routerSysInformationDict= self.getRouterSysInformationDict()
        if not self.routerRelativeInformationDict:
            self.routerRelativeInformationDict = self.getRouterRelativeInformationDict()
        if not self.routerRouteInformationDict:
            self.routerRouteInformationDict = self.getRouterRouterInformationDict()
        if not self.routerNeighborInformationDict:
            self.routerNeighborInformationDict = self.getRouterNeighborInformationDict(whiteList)
        routerAllInformationDict['equipmentSysInformation'] = self.routerSysInformationDict
        routerAllInformationDict['equipmentInterfaceInformation'] = self.routerInterfaceInformationDict
        routerAllInformationDict['equipmentRouterInformation'] = self.routerRouteInformationDict
        routerAllInformationDict['equipment2equipment'] = self.routerRelativeInformationDict
        routerAllInformationDict['neighborDict'] = self.routerNeighborInformationDict
        routerAllInformationJson = json.dumps(routerAllInformationDict, ensure_ascii=False, indent=4)
        #print(routerAllInformationJson)
        return [routerAllInformationJson, routerAllInformationDict]



def main():
    # rt = OperationRouter('1q3e!Q#E','10.46.97.252','161')
    # rts = OperationRouters('1q3e!Q#E','10.46.97.252','161')
    # list1,list2 = rts.getRouterInterfaceListAndIp()
    # print(list(zip(list1,list2)))
    rt = OperationRouter('1q3e!Q#E', '10.46.79.126', '161')
    log = LogOperation.OperationLog()
    dataJson, dataDict = rt.getRouterAllInformation()
    tb = TableOperation.OperationTable()
    tb.createTableAll()
    tb.insertDictionary2Database(dataDict)


if __name__ == '__main__':
    main()
