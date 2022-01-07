import json
from abc import ABC, abstractmethod
import IPy
import threading
from utils import log_model, snmp_model, thread_model



log = log_model.OperationLog()
sem=threading.Semaphore(4) #限制线程的最大数量为4个

class Equipment(ABC):
    """
    设备信息
    """
    def __init__(self, community, target, port):
        self.community = community
        self.target = target
        self.port = port

        self.SNID = None
        self.sysInformationDict = None
        self.routeInformationDict = None
        self.interfaceInformationDict = None
        self.relativeInformationDict = None
        self.neighborInformationDict = None

    @abstractmethod
    def getSNID(self):
        pass

    @log.classFuncDetail2Log('DEBUG')
    def getSysInformationDict(self):
        result = {}
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        result['sysSNID'] = self.getSNID()
        result['sysDescr'] = sn.getbulk(['1.3.6.1.2.1.1.1.0'])[0]
        result['sysObjectID'] = sn.getbulk(['1.3.6.1.2.1.1.2.0'])[0]
        result['sysUpTime'] = sn.getbulk(['1.3.6.1.2.1.1.3.0'])[0]
        result['sysContact'] = sn.getbulk(['1.3.6.1.2.1.1.4.0'])[0]
        result['sysName'] = sn.getbulk(['1.3.6.1.2.1.1.5.0'])[0]
        result['sysLocation'] = sn.getbulk(['1.3.6.1.2.1.1.6.0'])[0]
        result['sysSevices'] = sn.getbulk(['1.3.6.1.2.1.1.7.0'])[0]
        result['sysIfNumber'], result['sysForwarding'] = sn.getbulk(['1.3.6.1.2.1.2.1.0', '1.3.6.1.2.1.4.1.0'])
        return result

    @abstractmethod
    def getInterfaceInformationDict(self):
        pass

    @abstractmethod
    def getRouterInformationDict(self):
        pass

    @abstractmethod
    def getRelativeInformationDict(self):
        pass

    @abstractmethod
    def getAllInformation(self):
        pass



class Router(Equipment):
    """
    单台路由器相关操作
    """

    def __init__(self, community, target, port):
        super().__init__(community, target, port)



    @log.classFuncDetail2Log('DEBUG')
    def __getRouterInterfaceListAndIp(self):
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        [interfaceIpList, interfaceIdList] = sn.walk(['1.3.6.1.2.1.4.20.1.1', '1.3.6.1.2.1.4.20.1.2'])
        oidList = []
        for interfaceId in interfaceIdList:
            oidList.append('1.3.6.1.2.1.2.2.1.2.' + interfaceId)
        interfaceDescList = sn.getbulk(oidList)
        # print(list(zip(interfaceIpList,interfaceDescList)))
        return [interfaceIpList, interfaceDescList]

    @log.classFuncDetail2Log('DEBUG')
    def getName(self):
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        name = sn.getbulk(['1.3.6.1.2.1.1.5.0'])
        if (bool(name)):
            return name[0]
        else:
            return None

    @log.classFuncDetail2Log('DEBUG')
    def getSNID(self):
        if self.SNID:
            return self.SNID
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
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
                                            result = ID[0] + self.getName()
                                            self.SNID = result
                                            return result
        self.SNID = ID[0]
        return ID[0]

    @log.classFuncDetail2Log('DEBUG')
    def __getRouterForwarding(self):
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        name = sn.getbulk(['1.3.6.1.2.1.4.1.0'])
        if (bool(name)):
            return name[0]
        else:
            return None

    @log.classFuncDetail2Log('DEBUG')
    def getRouterNexthopsListAndType(self):
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        [NexthopsList, NexthopsType] = sn.walk(['1.3.6.1.2.1.4.21.1.7', '1.3.6.1.2.1.4.21.1.8'])
        # print(list(zip(NexthopsList, NexthopsType)))
        return [NexthopsList, NexthopsType]

    @log.classFuncDetail2Log('DEBUG')
    @log.classFuncDetail2Log('DEBUG')
    def getInterfaceInformationDict(self):
        # print('function getInterfaceInformationDict')
        result = {}
        interface = {}
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        result['sysSnID'] = self.getSNID()
        result['interfaceID'], result['interfaceName'], result['interfacePhysAddress'], result[
            'interfaceAdminStatus'], \
        result['interfaceOperStatus'], result['interfaceLastChange'], result['interfaceDesc'] = sn.walk(
            ['1.3.6.1.2.1.2.2.1.1', '1.3.6.1.2.1.2.2.1.2', '1.3.6.1.2.1.2.2.1.6', '1.3.6.1.2.1.2.2.1.7',
             '1.3.6.1.2.1.2.2.1.8', '1.3.6.1.2.1.2.2.1.9', '1.3.6.1.2.1.31.1.1.1.18'])
        for i in range(len(result['interfaceID'])):
            temp = {}
            temp['interfaceUniqueID'], temp['interfaceID'], temp['interfaceName'], temp['interfacePhysAddress'], \
            temp['interfaceAdminStatus'], temp['interfaceOperStatus'], temp['interfaceLastChange'], temp[
                'interfaceDesc'] = result['sysSnID'] + 'InterfaceID' + result['interfaceID'][i], result['interfaceID'][
                i], \
                                   result['interfaceName'][i], result['interfacePhysAddress'][i], \
                                   result['interfaceAdminStatus'][i], \
                                   result['interfaceOperStatus'][i], result['interfaceLastChange'][i], \
                                   result['interfaceDesc'][i]
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
    def __getWhichInterfaceDestinationIPOut(self, ipaddress, dataDict):
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
        return resultIfIndex, resultIfIp

    @log.classFuncDetail2Log('DEBUG')
    def getRouterInformationDict(self):
        # print('function getRouterInformationDict')
        if not self.interfaceInformationDict:
            self.interfaceInformationDict = self.getInterfaceInformationDict()
        result = {}
        router = {}
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        result['sysSnID'] = self.getSNID()
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
                                 self.interfaceInformationDict[result['routerIfIndex'][i]]['interfaceIP'], \
                                 result['routerNextHop'][i], \
                                 result['routerMask'][i]
            router[str(i)] = temp
        for key, routerDict in router.items():
            if (routerDict['routerIfIndex'] == '0'):
                routerDict['routerIfIndex'], routerDict['routerIfIP'] = self.__getWhichInterfaceDestinationIPOut(
                    routerDict['routerNextHop'], router)
        return router

    @log.classFuncDetail2Log('DEBUG')
    def getRelativeInformationDict(self, terminalSnmpUnenabledList=None):
        if not self.interfaceInformationDict:
            self.interfaceInformationDict = self.getInterfaceInformationDict()
        result = {}
        relative = {}
        sn = snmp_model.OperationSnmp(self.community, self.target, self.port)
        result['sysSnID'] = self.getSNID()
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
                  self.interfaceInformationDict[result['localInterfaceID'][i]]['interfaceIP'], \
                  result['peerInterfaceIP'][i], \
                  result['peerInterfacePhysAddress'][i]
            temp['peerSysName'] = ''
            temp['peerSysForwarding'] = ''
            relative[temp['peerInterfaceIP']] = temp
        return relative
        # for terminalSnmpUnenabled in terminalSnmpUnenabledList:
        #     relative[terminalSnmpUnenabled]['peerSysName'] = 'unknown'
        #     relative[terminalSnmpUnenabled]['peerSysForwarding'] = 'unknown'
        # for i in relative:
        #     if(relative[i]['peerSysName']):
        #         continue
        #     else:
        #         rt = OperationRouter('1q3e!Q#E',relative[i]['peerInterfaceIP'], '161')
        #         relative[i]['peerSysName'] = rt.getName()
        #         if(relative[i]['peerSysName']):
        #             relative[i]['peerSysForwarding'] = rt.__getRouterForwarding()
        #         else:
        #             continue
        # return [interfacedict, relative]

    @log.classFuncDetail2Log('DEBUG')
    def getRouterNeighborInformationDict(self, whiteList=None):
        # print('function getRouterNeighborInformationDict')
        if not self.routeInformationDict:
            self.routeInformationDict = self.getRouterInformationDict()
        if not self.sysInformationDict:
            self.sysInformationDict = self.getSysInformationDict()
        if not self.relativeInformationDict:
            self.relativeInformationDict = self.getRelativeInformationDict()
        resultIP = {}
        resultIP['unreachable'] = []
        resultIP['reachable'] = []
        threads = []
        def functest(community, target, port):
            with sem:
                rt = Router(community, target, port)
                nexthopID = None
                nexthopName = rt.getName()
                if nexthopName:
                    nexthopID = rt.getSNID()
                return nexthopName,nexthopID,target
        tempList = []
        for i in range(len(self.routeInformationDict)):
            if (self.routeInformationDict[str(i)]['routerNextHop'] == '0.0.0.0' or self.routeInformationDict[str(i)][
                'routerNextHop'] == '127.0.0.1' or self.routeInformationDict[str(i)]['routerNextHop'] in tempList):
                continue
            else:
                #log.info(str(self.routeInformationDict[str(i)]['routerNextHop']))
                tempList.append(self.routeInformationDict[str(i)]['routerNextHop'])
                t = thread_model.MyThread(target=functest, args=(self.community,self.routeInformationDict[str(i)]['routerNextHop'],self.port))
                threads.append(t)
        for t in threads:
            log.info(t.args[1])
            t.start()
        for t in threads:
            t.join()
        for t in threads:
            nexthopName, nexthopID ,nexthopIP = t.get_result()
            if (nexthopIP in [i[0] for i in resultIP['reachable']] or nexthopIP in [i[0] for i in resultIP['unreachable']] or nexthopIP in whiteList):
                continue
            if not nexthopName:
                resultIP['unreachable'].append([nexthopIP, None, None])
                continue
            else:
                if (nexthopName and nexthopID):
                    resultIP['reachable'].append(
                        [nexthopIP, nexthopName, nexthopID])
                elif (nexthopName):
                    resultIP['reachable'].append(
                        [nexthopIP, nexthopName, None])
                else:
                    resultIP['unreachable'].append(
                        [nexthopIP, None, None])
        return resultIP

    #     resultIP = {}
    #     resultIP['unreachable'] = []
    #     resultIP['reachable'] = []
    #     return resultIP
    @log.classFuncDetail2Log('DEBUG')
    def getAllInformation(self, whiteList=None):
        routerAllInformationDict = {}
        if not self.sysInformationDict:
            self.sysInformationDict = self.getSysInformationDict()
        while not self.sysInformationDict['sysSNID']:
            self.sysInformationDict['sysSNID'] = self.getSNID()
        if not self.interfaceInformationDict:
            self.interfaceInformationDict = self.getInterfaceInformationDict()
        if not self.relativeInformationDict:
            self.relativeInformationDict = self.getRelativeInformationDict()
        if not self.routeInformationDict:
            self.routeInformationDict = self.getRouterInformationDict()
        if not self.neighborInformationDict:
            self.neighborInformationDict = self.getRouterNeighborInformationDict(whiteList)

        routerAllInformationDict['equipmentSysInformation'] = self.sysInformationDict
        routerAllInformationDict['equipmentInterfaceInformation'] = self.interfaceInformationDict
        routerAllInformationDict['equipmentRouterInformation'] = self.routeInformationDict
        routerAllInformationDict['equipment2equipment'] = self.relativeInformationDict
        routerAllInformationDict['neighborDict'] = self.neighborInformationDict
        routerAllInformationJson = json.dumps(routerAllInformationDict, ensure_ascii=False, indent=4)
        # print(routerAllInformationJson)
        return [routerAllInformationJson, routerAllInformationDict]


def main():
    # rt = OperationRouter('1q3e!Q#E','10.46.97.252','161')
    # rts = OperationRouters('1q3e!Q#E','10.46.97.252','161')
    # list1,list2 = rts.__getRouterInterfaceListAndIp()
    # print(list(zip(list1,list2)))
    rt = Router('1q3e!Q#E', '10.46.79.126', '161')
    log = log_model.OperationLog()
    dataJson, dataDict = rt.getAllInformation()
    print(dataJson)


if __name__ == '__main__':
    main()
