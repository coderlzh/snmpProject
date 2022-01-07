import IPy
import json
import threading
from utils import log_model,equip_model,thread_model
from configparser import ConfigParser

CONFIGFILE = '../config/project.ini'
config = ConfigParser()
config.read(CONFIGFILE)
COMMUNITY = config['detection'].get('Community')
TARGET = config['detection'].get('Target')
PORT = config['detection'].get('Port')

log = log_model.OperationLog()
sem=threading.Semaphore(4) #限制线程的最大数量为4个
class OperationNetwork:
    """
    网络相关操作
    """

    def __init__(self,filePath):
        self.filePath = filePath
        self.vrrpDeviceStatic = {} #静态分析产生的可能正确的VRRP设备信息字典，足以满足日常分析，可以减少消耗
        self.networkDict = None
        self.netInformationDict = None
        self.edgeNetInformationDict = None
        self.netDirectInformationDict = None
        self.edgeNetInformationDict = None
        self.edgeDeviceInformationDict = None
        self.macInformationDict = None

    @log.classFuncDetail2Log('DEBUG')
    def __getTargetInfo(self, community, target, port, neighborName):
        with sem:
            log.info(' Process Start To Get ' + neighborName + ' Information !')
            rt = equip_model.Router(community, target, port)
            dataJson, dataDict = rt.getAllInformation(whiteList=[])
            log.info(' Process End !')
            return dataJson, dataDict

    @log.classFuncDetail2Log('DEBUG')
    def __createThreads(self,community, port, inLevelNeighbor):
        threads = []
        for NeighborIP, NeighborName, NeighborSNID in inLevelNeighbor:
            if (NeighborName):
                t = thread_model.MyThread(target=self.__getTargetInfo, args=(community, NeighborIP, port, NeighborName))
                threads.append(t)
        return threads

    @log.classFuncDetail2Log('DEBUG')
    def networkInfo_update(self):
        rt = equip_model.Router(COMMUNITY, TARGET, PORT)
        detection = rt.getName()
        snID = rt.getSNID()
        networkDict = {}
        neighborDiscovery = [[TARGET, detection, snID]]
        inLevelNeighbor = neighborDiscovery
        nextLevelNeighbor = []
        while inLevelNeighbor:
            threads = self.__createThreads(COMMUNITY, PORT, inLevelNeighbor)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            for t in threads:
                dataJson, dataDict = t.get_result()
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
        log.info(' neighborDiscovery' + str(neighborDiscovery))
        log.resultPrint(str(neighborDiscovery))
        log.networkJsonPrint(json.dumps(networkDict, ensure_ascii=False, indent=4))

    @log.classFuncDetail2Log('DEBUG')
    def networkDict_get(self) -> dict:
        """
        解析Json文本并返回采集到的全网信息
        :return: type=字典 data={sysName:设备信息}
        """
        with open(self.filePath, 'r+') as f:
            networkDict = json.loads(f.read())
        return networkDict

    @log.classFuncDetail2Log('DEBUG')
    def getMacInfromationDict(self) -> dict:
        """
        解析Json文本并返回MAC地址与厂家对应表
        :return: type=字典 data={mac:厂家}
        """
        with open('../logs/mac.log', 'r+') as f:
            macInfromationDict = json.loads(f.read())
        return macInfromationDict

    @log.classFuncDetail2Log('DEBUG')
    def checkIP(self, ipaddress:str) -> bool:
        """
        检查入参IP的合法性，对于非IP类型的字符串和特殊类型IP，比如127.0.0.1和0.0.0.0返回False
        :param ipaddress: type=str data=''
        :return: type=bool data=True Or False
        """
        try:
            IPy.IP(ipaddress)
            if(ipaddress.startswith('127') or ipaddress == '0.0.0.0'):
                return False
            return True
        except Exception as e:
            return False

    @log.classFuncDetail2Log('DEBUG')
    def checkTypeOfParam(self, param: str) -> str:
        """
        检查参数类型，将字符串整理并分类为 'IP' 'NETWORK' 'Unvalid Param' 'SYSNAME'四类
        :param param: type=str data=''
        :return: type=str data=IP' Or 'NETWORK' Or 'Unvalid Param' Or 'SYSNAME'
        """
        if not self.networkDict:
            self.networkDict =self.networkDict_get()
        if (self.checkIP(param)):
            if IPy.IP(param).netmask() != IPy.IP('255.255.255.255'):
                return 'NETWORK'
            else:
                return 'IP'
        else:
            if(param == '127.0.0.1' or param == '0.0.0.0'):
                return 'Unvalid Param'
            elif param in self.networkDict:
                return 'SYSNAME'
            else:
                return 'Unvalid Param'

    @log.classFuncDetail2Log('DEBUG')
    def getVrrpDeviceDict(self) -> None:
        """
        获取网络中存在的虚拟网段IP和对应的设备，目前这个函数做的还不准，后续看有没有办法完善吧
        :return: type=None data=None
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        for sysname, sysnameDict in self.networkDict.items():
            broadcastList = []
            #print(sysname)
            if (sysnameDict['equipmentInterfaceInformation']):
                for id, interfaceDict in self.networkDict[sysname]['equipmentInterfaceInformation'].items():
                    if (self.checkIP(interfaceDict['interfaceIP'])):
                        broadcastList.append(interfaceDict['interfaceIP'])
                        broadcastList.append(IPy.IP(interfaceDict['interfaceIP']).make_net(interfaceDict['interfaceNetmask']).broadcast().strNormal(0))
                        broadcastList.append(IPy.IP(interfaceDict['interfaceIP']).make_net(
                            interfaceDict['interfaceNetmask']).strNormal(0))
                #print(broadcastList)
            if (sysnameDict['equipmentRouterInformation']):
                for key, routerDict in sysnameDict['equipmentRouterInformation'].items():
                    if(routerDict['routerDest'].startswith('127') or routerDict['routerDest'] =='0.0.0.0' or routerDict['routerDest'] =='255.255.255.255'):
                        continue
                    if (routerDict['routerNextHop'] == '127.0.0.1' and routerDict['routerDest'] != routerDict['routerIfIP']):
                        if (routerDict['routerDest'] in broadcastList):
                            continue
                        #print(routerDict['routerDest'])
                        #print(sysname)
                        sysnameList = []
                        sysnameList.insert(0, sysname)

                        self.vrrpDeviceStatic[routerDict['routerDest']] = {'sysname': sysnameList}
        for IP in list(self.vrrpDeviceStatic):
            for sysname, sysnameDict in self.networkDict.items():
                if (sysnameDict['equipment2equipment']):
                    try:
                        if not sysnameDict['equipment2equipment'][IP]['peerInterfacePhysAddress'].startswith('0x00005e0001'):
                            self.vrrpDeviceStatic.pop(IP)
                        else:
                            self.vrrpDeviceStatic[IP]['sysname'].append(sysname)
                    except:
                        continue
        #print(json.dumps(self.vrrpDeviceStatic, ensure_ascii='utf-8', indent=4))

    @log.classFuncDetail2Log('DEBUG')
    def getInformationOfParam(self, param: str, paramType: str) -> list:
        """
        根据参数和参数类型获取参数对应的 设备名称,SNID,IP 用来在路径发现中进行一个路径的寻找
        :param param: type=str data=''
        :param paramType: type=str data='IP' Or 'NETWORK'  Or 'SYSNAME'
        :return: type= [str,str,str,str]
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        if(paramType == 'IP'):
            if (param == '127.0.0.1' or param == '0.0.0.0'):
                return ['', param, '', 'IP']
            if param in self.vrrpDeviceStatic:
                sysSNID = self.getSNIDBySysName(self.vrrpDeviceStatic[param]['sysname'][0])
                return [self.vrrpDeviceStatic[param]['sysname'][0], param, sysSNID,'IP']
            for sysname, sysnameDict in self.networkDict.items():
                if (sysnameDict['equipmentInterfaceInformation']):
                    for interfaceID, interfaceDict in sysnameDict['equipmentInterfaceInformation'].items():
                        if (interfaceDict['interfaceIP'] == param):
                            if (sysnameDict['equipmentSysInformation']):
                                return [sysname, param, sysnameDict['equipmentSysInformation']['sysSNID'], 'IP']
                            else:
                                return [sysname, param, '', 'IP']
        elif(paramType == 'NETWORK'):
            netDirectInformationDictBeSelected = self.getNetDirectInformationBeSelected(param)
            sysnameList = []
            IPdetectList = []
            SNIDList = []
            for IP, IPDict in netDirectInformationDictBeSelected.items():
                for sysname, IPdetect in IPDict.items():
                    if sysname not in sysnameList:
                        sysnameList.append(sysname)
                        IPdetectList.append(IPdetect)
                        SNIDList.append(self.getSNIDBySysName(sysname))
            return [sysnameList, IPdetectList, SNIDList, 'NETWORK']
        elif (paramType == 'SYSNAME'):
            interfaceIPList = []
            if (self.networkDict[param]['equipmentInterfaceInformation']):
                for interfaceID, interfaceDict in self.networkDict[param]['equipmentInterfaceInformation'].items():
                    if(self.checkIP(interfaceDict['interfaceIP'])):
                        interfaceIPList.append(interfaceDict['interfaceIP'])
            if (self.networkDict[param]['equipmentSysInformation']):
                return [param, interfaceIPList, self.networkDict[param]['equipmentSysInformation']['sysSNID'], 'SYSNAME']
            else:
                return [param, interfaceIPList, '', 'SYSNAME']
        else:
            return [param, '' , '', paramType]

    @log.classFuncDetail2Log('DEBUG')
    def getDeviceNetInformationFromDict(self, sysname: str) -> dict:
        """
        获取设备各接口及其对应网段信息
        :param sysname: type=str data=''
        :return: type=dict data={network:interfaceIP}
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        netDeviceInformationDict = {}
        if(self.networkDict[sysname]['equipmentInterfaceInformation']):
            for InterfaceID, InterfaceDict in self.networkDict[sysname]['equipmentInterfaceInformation'].items():
                if(self.checkIP(InterfaceDict['interfaceIP'])):
                    netDeviceInformationDict[IPy.IP(InterfaceDict['interfaceIP']).make_net(InterfaceDict['interfaceNetmask']).strNormal(1)] = InterfaceDict['interfaceIP']
        return netDeviceInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getNetInformationFromDict(self) -> dict:
        """
        根据路由表获取全网的网段信息，可以获得到逻辑上存在的网络以及前往对应网路的设备SYSNAME及接口IP
        :return: type=dict data={network:{sysname:interfaceIP}}
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        netInformationDict = {}
        for sysname, sysnameDict in self.networkDict.items():
            for key, routerDict in sysnameDict['equipmentRouterInformation'].items():
                if not routerDict['routerDest'] == '0.0.0.0' and not routerDict['routerDest'].startswith('127'):
                    temp = IPy.IP(routerDict['routerDest']).make_net(routerDict['routerMask']).strNormal(1)
                    try:
                        netInformationDict[temp][sysname] = routerDict['routerIfIP']
                    except:
                        netInformationDict[temp] = {sysname: routerDict['routerIfIP']}
        return netInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getNetInformationBeSelected(self, netBeSelected: str) -> dict:
        """
        获取特定网段的信息
        :param netBeSelected: type=str data='network/mask'
        :return: type=dict data={network:{sysname:interfaceIP}}
        """
        netInformationBeSelected = {}
        if not self.netInformationDict:
            self.netInformationDict = self.getNetInformationFromDict()
        for net, netDict in self.netInformationDict.items():
            if (IPy.IP(net) in IPy.IP(netBeSelected)):
                netInformationBeSelected[net] = netDict
        return netInformationBeSelected

    @log.classFuncDetail2Log('DEBUG')
    def getNetDirectInformationFromDict(self) -> dict:
        """
        根据设备接口表获取设备的直连网段信息，非路由表。
        :return: type=dict data={network:{sysname:interfaceIP}}
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        netDirectInformationDict = {}
        for sysname, sysnameDict in self.networkDict.items():
            for interfaceID, interfaceDict in sysnameDict['equipmentInterfaceInformation'].items():
                if interfaceDict["interfaceIP"] and not interfaceDict["interfaceIP"].startswith('No'):
                    temp = IPy.IP(interfaceDict["interfaceIP"]).make_net(interfaceDict["interfaceNetmask"]).strNormal(1)
                    try:
                        netDirectInformationDict[temp][sysname] = interfaceDict["interfaceIP"]
                    except:
                        netDirectInformationDict[temp] = {sysname: interfaceDict["interfaceIP"]}
        return netDirectInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getNetDirectInformationBeSelected(self, netBeSelected: str) -> dict:
        """
        获取特定直连网段的信息
        :param netBeSelected: type=str data='network/mask'
        :return: type=dict data={network:{sysname:interfaceIP}}
        """
        netDirectInformationBeSelected = {}
        if not self.netDirectInformationDict:
            self.netDirectInformationDict = self.getNetDirectInformationFromDict()
        for net, netDict in self.netDirectInformationDict.items():
            if (IPy.IP(net) in IPy.IP(netBeSelected)):
                netDirectInformationBeSelected[net] = netDict
        return netDirectInformationBeSelected

    @log.classFuncDetail2Log('DEBUG')
    def __getIFDestinationIPInDirect(self, ipaddress: str , dataDict: dict) -> str:
        """
        用来判断目标IP在设备的MAC表中是否有相关的类型，这是对于一些设备不会产生自己接口对应直连网段的路由信息而导致在寻找直连设备
        失败的补充方法,同时因为直连网段的优先级高于路由表其他路由优先级，所以在寻找时，会优先考虑该方法
        :param ipaddress: type=str data=IP
        :param dataDict: type=dict data = {'equipement2equipement':{}}
        :return: type=str data=ipaddress
        """
        for key in dataDict:
            if (ipaddress == key):
                return ipaddress

    @log.classFuncDetail2Log('DEBUG')
    def getWhichRouterDestinationIPIn(self, ipaddress: str, dataDict: dict) -> str:
        """
        获取目标IP所在路由并返回下一跳
        :param ipaddress: type=str data=IP
        :param dataDict: type=dict data = {'equipementRouterinformation':{}}
        :return: type=str data=ipaddress
        """
        maxNet = IPy.IP('0.0.0.0')
        result = ''
        default = ''
        for key, routerDict in dataDict.items():
            if (ipaddress in IPy.IP(routerDict['routerDest']).make_net(routerDict['routerMask'])):
                if (IPy.IP(routerDict['routerMask']) >= maxNet):
                    maxNet = IPy.IP(routerDict['routerMask'])
                    if (routerDict['routerNextHop'] == routerDict['routerIfIP']):
                        print('目标设备%s处于接口%s直连网段内，将由接口%s转发,' % (
                            ipaddress, routerDict['routerIfIP'], routerDict['routerIfIP']), end='')
                        for tempKey, tempRouterDict in dataDict.items():
                            if tempRouterDict['routerIfIP'] == routerDict['routerIfIP'] and tempRouterDict[
                                'routerNextHop'] != routerDict['routerIfIP'] and tempRouterDict[
                                'routerNextHop'] != '127.0.0.1':
                                if (tempRouterDict['routerDest'] == '0.0.0.0'):
                                    default = tempRouterDict['routerNextHop']
                                if (tempRouterDict['routerNextHop'] == ipaddress):
                                    print('下一跳设备为%s' % (tempRouterDict['routerNextHop']))
                                    return tempRouterDict['routerNextHop']
                        if not default:
                            print('本设备未从路由表中找到合适的下一跳，初步估计该路由不存在，请检查。')
                        else:
                            print('下一跳设备可能为%s' % (default))
                            return default
                    elif(routerDict['routerNextHop'] == '0.0.0.0' and routerDict['routerIfIP'] == ''):
                        print('匹配到出接口为%s，此条目为黑洞路由，目标IP经此设备不可达，该路径不成立'%(routerDict['routerIfIndex']))
                        result = ''
                    else:
                        result = routerDict['routerNextHop']
        return result

    @log.classFuncDetail2Log('DEBUG')
    def pathTraceIP(self, sourceDict:dict, destinationDict:dict) -> list:
        """
        同traceroute，返回值第4位为0表示路径不成立，为1表示路径成立
        :param sourceDict: type=dict data={Sysname':'','IP':'','SNID':''}
        :param destinationDict: type=dict data={Sysname':'','IP':'','SNID':''}
        :return: type=list data=[IPList, sysNameList, SNIDList, 0 Or 1]
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        sysNameList = [sourceDict['Sysname']]
        IPList = [sourceDict['IP']]
        SNIDList = [sourceDict['SNID']]
        if not sourceDict['Sysname'] or not sourceDict['IP']:
            print('源IP或SYSNAME对应的设备不存在，请检查sourceIP或SYSNAME')
            return ['', '', '', 1]
        elif not sourceDict['SNID']:
            print('源IP设备的SNID采集失败，请注意。')
            return ['', '', '', 1]
        if not destinationDict['Sysname'] or not destinationDict['IP']:
            print('目的IP或SYSNAME对应的设备不存在，请检查destinationIP或SYSNAME')
            return ['', '', '', 1]
        elif not destinationDict['SNID']:
            print('目的IP设备的SNID采集失败，请注意。')
            return ['', '', '', 1]
        nextHopSysname, nextHopIP, nextHopSNID = sourceDict['Sysname'], sourceDict['IP'], sourceDict['SNID']
        while (True):
            print(nextHopSysname, nextHopIP, nextHopSNID)
            if (nextHopSNID == destinationDict['SNID']):
                break
            nextHop = self.__getIFDestinationIPInDirect(destinationDict['IP'],
                                                      self.networkDict[nextHopSysname]['equipment2equipment'])
            if not nextHop:
                nextHop = self.getWhichRouterDestinationIPIn(destinationDict['IP'],
                                                             self.networkDict[nextHopSysname]['equipmentRouterInformation'])
            if not nextHop:
                print('Route in %s to %s not found!' % (nextHopSysname, destinationDict['IP']))
                return [IPList, sysNameList, SNIDList, 1]
            nextHopSysname, nextHopIP, nextHopSNID, nextHopType = self.getInformationOfParam(nextHop ,'IP')
            if not nextHopSysname or not nextHopIP or not nextHopSNID:
                IPList.append(nextHopIP)
                break
            elif (nextHopSNID in SNIDList):
                print('在%s的路由存在环路，请检查。' % (nextHopSysname))
                sysNameList.append(nextHopSysname)
                IPList.append(nextHopIP)
                SNIDList.append(nextHopSNID)
                break
            else:
                sysNameList.append(nextHopSysname)
                IPList.append(nextHopIP)
                SNIDList.append(nextHopSNID)
        if (len(IPList) != len(sysNameList)):
            print(IPList[-1] + '对应的设备不存在，请检查')
            return [IPList, sysNameList, SNIDList, 1]
        else:
            return [IPList, sysNameList, SNIDList, 0]

    @log.classFuncDetail2Log('DEBUG')
    def getSNIDBySysName(self, param: str) -> str:
        """
        根据设备的sysName获取设备的SNID
        :param param: type=str,data=sysname
        :return: type=str,data=sysname
        """
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        try:
            for sysname, dataDict in self.networkDict.items():
                if (param == sysname):
                    return dataDict['equipmentSysInformation']['sysSNID']
        except:
            return ''

    @log.classFuncDetail2Log('DEBUG')
    def tracertToDestination(self,sourceDict,destinationType,destination):
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        minimumIPList = []
        minimumsysNameList = []
        minimumSNIDList = []
        minStep = 255
        if destinationType == 'IP':
            destinationSysname, destinationIP, destinationSNID, destinationType = self.getInformationOfParam(
                destination, 'IP')
            destinationDict = {'Sysname': destinationSysname, 'IP': destinationIP, 'SNID': destinationSNID}
            minimumIPList, minimumsysNameList, minimumSNIDList, resultType = self.pathTraceIP(sourceDict,
                                                                                              destinationDict)
        elif destinationType == 'NETWORK':
            destinationSysname, destinationIP, destinationSNID, destinationType = self.getInformationOfParam(
                destination, 'NETWORK')
            for i in range(len(destinationIP)):
                print('选取目标设备IP，当前设置目的IP为%s，设备名称为%s：' % (destinationIP[i], destinationSysname[i]))
                destinationSNID = self.getSNIDBySysName(destinationSysname[i])
                destinationDict = {'Sysname': destinationSysname[i], 'IP': destinationIP[i], 'SNID': destinationSNID}
                IPList, sysNameList, SNIDList, resultType = self.pathTraceIP(sourceDict, destinationDict)
                if resultType == 0:
                    temp = min(len(sysNameList), minStep)
                    if (temp < minStep):
                        minStep = temp
                        minimumIPList, minimumsysNameList, minimumSNIDList = IPList, sysNameList, SNIDList
            if not minimumIPList:
                print('目标%s不可达，请检查路由配置。' % (destination))
                return minimumIPList, minimumsysNameList, minimumSNIDList
        else:
            destinationSysname, destinationIP, destinationSNID, destinationType = self.getInformationOfParam(
                destination, 'SYSNAME')
            print(destinationIP)
            for i in range(len(destinationIP)):
                print('选取目标设备IP，当前设置目的IP为%s，设备名称为%s：' % (destinationIP[i], destinationSysname))

                destinationDict = {'Sysname': destinationSysname, 'IP': destinationIP[i], 'SNID': destinationSNID}
                IPList, sysNameList, SNIDList, resultType = self.pathTraceIP(sourceDict, destinationDict)
                if resultType == 0:
                    temp = min(len(sysNameList), minStep)
                    if (temp < minStep):
                        minStep = temp
                        minimumIPList, minimumsysNameList, minimumSNIDList = IPList, sysNameList, SNIDList
            if not minimumIPList:
                print('目标%s不可达，请检查路由配置。' % (destination))
                return minimumIPList, minimumsysNameList, minimumSNIDList
        return minimumIPList, minimumsysNameList, minimumSNIDList

    @log.classFuncDetail2Log('DEBUG')
    def pathTrace(self, source, destination):
        print('正在寻找 %s 到 %s 经过的设备......' % (source, destination))
        result = []
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        sourceType = self.checkTypeOfParam(source)
        #def getInformationOfParam(self, param, paramType, networkDict)
        destinationType = self.checkTypeOfParam(destination)
        if sourceType == 'IP':
            sourceSysname, sourceIP, sourceSNID, sourceType = self.getInformationOfParam(source,
                                                                                         self.checkTypeOfParam(source))
            sourceDict = {'Sysname': sourceSysname, 'IP': sourceIP, 'SNID': sourceSNID}
            return self.tracertToDestination(sourceDict, destinationType, destination)
        elif sourceType == 'NETWORK':
            NetDirectInformationBeSelected = self.getNetDirectInformationBeSelected(
                source)
            sourceSysname, sourceIP, sourceSNID, sourceType = self.getInformationOfParam(source,
                                                                                         self.checkTypeOfParam(source))
            NetDirectInformationBeSelected = self.getNetDirectInformationBeSelected(
                destination)
            if not NetDirectInformationBeSelected:
                print('目的网段无直接接入接口，请检查。')
                return result
            for i in range(len(sourceIP)):
                print('切换源为设备%s' % (sourceSysname[i]))
                sourceDict = {'Sysname': sourceSysname[i], 'IP': sourceIP[i], 'SNID': sourceSNID[i]}
                result.append(self.tracertToDestination(sourceDict, destinationType, destination))
            return result
        else:
            sourceSysname, sourceIP, sourceSNID, sourceType = self.getInformationOfParam(source,
                                                                                         self.checkTypeOfParam(source))

            sourceDict = {'Sysname': sourceSysname, 'IP': sourceIP[0], 'SNID': sourceSNID}
            return self.tracertToDestination(sourceDict, destinationType, destination)

    @log.classFuncDetail2Log('DEBUG')
    def getDeviceConnectedDict(self,param:str) -> dict:
        """
        获取设备直连的设备
        :param param: type=str data=sysname
        :return: type=dict data={network:{sysname:interfaceIP}}
        """
        netDict = {}
        deviceNetInformationDict = self.getDeviceNetInformationFromDict(param)
        for NETWORK in deviceNetInformationDict.keys():
            if self.checkTypeOfParam(NETWORK) == 'NETWORK':
                netDirectInformationBeSelected = self.getNetDirectInformationBeSelected(NETWORK)
                netDict[NETWORK] = netDirectInformationBeSelected
        return netDict

    @log.classFuncDetail2Log('DEBUG')
    def getEdgeNetInformationDict(self):
        if not self.netDirectInformationDict:
            self.netDirectInformationDict = self.getNetDirectInformationFromDict()
        edgeNetInformationDict ={}
        for key in self.netDirectInformationDict:
            if(self.checkTypeOfParam(key) == 'NETWORK' and eval(key.split('/')[1])<30):
                #if(len(self.netDirectInformationDict[key])<=2):
               edgeNetInformationDict[key] = self.netDirectInformationDict[key]
        return edgeNetInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getCommonPrefixLength(self,string1,string2):
        length = 0
        for i in range(len(string1)):
            if(string1[i] == string2[i]):
                length += 1
            else:
                break
        return length

    @log.classFuncDetail2Log('DEBUG')
    def getLongestCommonPrefix(self,strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ['',32]
        if len(strs) == 1:
            return ['',32]
        s1 = min(strs)
        s2 = max(strs)
        for i, c in enumerate(s1):
            if c != s2[i]:
                return [s1[:i],i]
        return [s1,len(s1)]

    @log.classFuncDetail2Log('DEBUG')
    def getSuperNetworkInformationDict(self, netList, prefixList):
        superNetworkInformationDict ={}
        [commonPrefix,preLen] = self.getLongestCommonPrefix(netList)
        if(preLen == 32):
            IPy.IP(hex(int(netList[0], 2))).strNormal(0) + '/' + str(prefixList[0])
            superNetworkInformationDict['name'] = IPy.IP(hex(int(netList[0], 2))).strNormal(0) + '/' + str(prefixList[0])
            return superNetworkInformationDict
        else:
            part0List = []
            part1List = []
            part0PreList = []
            part1PreList = []
            for i in range(len(netList)):
                if(netList[i][preLen] == '1'):
                    part1List.append(netList[i])
                    part1PreList.append(prefixList[i])
                else:
                    part0List.append(netList[i])
                    part0PreList.append(prefixList[i])
            name = IPy.IP(hex(int(commonPrefix + '0' * (32 - preLen), 2))).strNormal(0)+'/'+str(preLen)
            superNetworkInformationDict['name'] = name
            superNetworkInformationDict['children'] = []
            #key1 = IPy.IP(hex(int(commonPrefix + '0' + '0' * (32 - preLen - 1), 2))).strNormal(0)+'/'+str(preLen+1)
            #key2 = IPy.IP(hex(int(commonPrefix + '1' + '0' * (32 - preLen - 1), 2))).strNormal(0) + '/' + str(preLen+1)
            superNetworkInformationDict['children'].append(self.getSuperNetworkInformationDict(part0List,part0PreList))
            superNetworkInformationDict['children'].append(self.getSuperNetworkInformationDict(part1List,part1PreList))
            return superNetworkInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def comboSuperNetAndDeviceInformation(self,superNetworkInformationDict: dict,deviceInformationDict: dict) ->dict:
        """
        组合父网段信息和网段设备信息形成可以载入数据库的字典
        :param superNetworkInformationDict: 父网段字典树
        :param deviceInformationDict: 设备信息字典
        :return: 携带更多信息的组合网段字典树
        """
        def get4IP(network):
            netIP = network.split('/')[0]
            ipList = netIP.split('.')
            ipList[3] = str(int(ipList[3]) + 1)
            startIP = '.'.join(ipList)
            broIP = IPy.IP(network).broadcast().strNormal(1)
            ipList = broIP.split('.')
            ipList[3] = str(int(ipList[3]) - 1)
            endIP = '.'.join(ipList)
            return netIP,startIP,broIP,endIP


        def dfs(dictBeSelect):
            try:
                dictBeSelect['used'] = 0
                temp = 0
                for child in dictBeSelect['children']:
                    dictBeSelect['netip'], dictBeSelect['startip'], dictBeSelect['broip'], dictBeSelect[
                            'endip'] = get4IP(dictBeSelect['name'])
                    dictBeSelect['total'] = 2**(32-eval(dictBeSelect['name'].split('/')[1]))-2
                    if(child['name'] == dictBeSelect['name']):
                        temp = deviceInformationDict[child['name']]['used']
                    dictBeSelect['used'] += dfs(child)
                    if(eval(dictBeSelect['name'].split('/')[1])-eval(child['name'].split('/')[1]) == -1):
                        dictBeSelect['used'] -= 1
                if temp:
                    dictBeSelect['used'] = temp
                dictBeSelect['netmask'] = IPy.IP(dictBeSelect['name']).netmask().strNormal(1)
                dictBeSelect['free'] = dictBeSelect['total'] - dictBeSelect['used']
                return dictBeSelect['used']+2
            except Exception as e:
                dictBeSelect['total'] = deviceInformationDict[dictBeSelect['name']]['total']
                dictBeSelect['used'] = deviceInformationDict[dictBeSelect['name']]['used']
                dictBeSelect['free'] = dictBeSelect['total'] - dictBeSelect['used']
                dictBeSelect['netmask'] = IPy.IP(dictBeSelect['name']).netmask().strNormal(1)
                dictBeSelect['netip'], dictBeSelect['startip'], dictBeSelect['broip'], dictBeSelect['endip']= get4IP(dictBeSelect['name'])
                return dictBeSelect['used']+2
        dfs(superNetworkInformationDict)
        return superNetworkInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getEdgeDeviceInformationTreeDict(self):
        edgeDeviceInformationDict = {}
        if not self.edgeNetInformationDict:
            self.edgeNetInformationDict = self.getEdgeNetInformationDict()
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        if not self.macInformationDict:
            self.macInformationDict = self.getMacInfromationDict()
        for network, netDict in self.edgeNetInformationDict.items():
            for sysName, localInterfaceIP in netDict.items():
                if(self.networkDict[sysName]['equipmentInterfaceInformation']):
                    for interfaceID,interfaceDict in self.networkDict[sysName]['equipmentInterfaceInformation'].items():
                        if(interfaceDict['interfaceIP'] == localInterfaceIP):
                            try:
                                macAndTypeList = [sysName,interfaceDict["interfacePhysAddress"], self.macInformationDict[
                                    interfaceDict["interfacePhysAddress"][0:8].upper()]]
                            except:
                                macAndTypeList = [sysName,interfaceDict["interfacePhysAddress"], 'None']
                            try:
                                try:
                                    edgeDeviceInformationDict[network]['networkDevice'][localInterfaceIP] = \
                                        edgeDeviceInformationDict[network]['networkDevice'][localInterfaceIP] + '&' + (
                                            '/'.join(macAndTypeList))
                                except:
                                    edgeDeviceInformationDict[network]['networkDevice'][localInterfaceIP] = '/ '.join(
                                        macAndTypeList)
                                    edgeDeviceInformationDict[network]['used'] += 1
                            except:
                                edgeDeviceInformationDict[network] = {'total':2**(32-eval(network.split('/')[1]))-2,'used':1,'networkDevice':{},'host':{}}
                                edgeDeviceInformationDict[network]['networkDevice'] = {localInterfaceIP:'/ '.join(macAndTypeList)}
        for network,netDict in self.edgeNetInformationDict.items():
            for sysName,localInterfaceIP in netDict.items():
                for peerInterfaceIP,relativeDict in self.networkDict[sysName]['equipment2equipment'].items():
                    if(relativeDict["localInterfaceIP"] == localInterfaceIP and relativeDict["peerInterfaceIP"] not in edgeDeviceInformationDict[network]['networkDevice']):
                        try:
                            macAndTypeList = [relativeDict["peerInterfacePhysAddress"],self.macInformationDict[relativeDict["peerInterfacePhysAddress"][0:8].upper()]]
                        except:
                            macAndTypeList = [relativeDict["peerInterfacePhysAddress"],'None']
                        try:
                            edgeDeviceInformationDict[network]['host'][peerInterfaceIP]
                            continue
                        except:
                            edgeDeviceInformationDict[network]['host'][peerInterfaceIP] = '/ '.join(macAndTypeList)
                            edgeDeviceInformationDict[network]['used'] +=1
            if not edgeDeviceInformationDict[network]['host']:
                edgeDeviceInformationDict.pop(network)
        netList = list(edgeDeviceInformationDict.keys())
        #print(netList)
        prefixList = []
        for i in range(len(netList)):
            prefixList.append(netList[i].split('/')[1])
            netList[i] = IPy.IP(netList[i]).strBin()
        superNetworkInformationDict = self.getSuperNetworkInformationDict(netList,prefixList)
        self.comboSuperNetAndDeviceInformation(superNetworkInformationDict,edgeDeviceInformationDict)
        return edgeDeviceInformationDict,superNetworkInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def getNetDeviceInformationTreeDict(self):
        netDeviceInformationDict = {}
        if not self.netDirectInformationDict:
            self.netDirectInformationDict = self.getNetDirectInformationFromDict()
        if not self.networkDict:
            self.networkDict = self.networkDict_get()
        if not self.macInformationDict:
            self.macInformationDict = self.getMacInfromationDict()
        for key in self.netDirectInformationDict:
            if(self.checkTypeOfParam(key) == 'NETWORK'):
                netDeviceInformationDict[key] = {}
        for network, netDict in self.netDirectInformationDict.items():
            if (self.checkTypeOfParam(network) != 'NETWORK'):
                continue
            for sysName, localInterfaceIP in netDict.items():
                if(self.networkDict[sysName]['equipmentInterfaceInformation']):
                    for interfaceID,interfaceDict in self.networkDict[sysName]['equipmentInterfaceInformation'].items():
                        if(interfaceDict['interfaceIP'] == localInterfaceIP):
                            try:
                                macAndTypeList = [sysName,interfaceDict["interfacePhysAddress"], self.macInformationDict[
                                    interfaceDict["interfacePhysAddress"][0:8].upper()]]
                            except:
                                macAndTypeList = [sysName,interfaceDict["interfacePhysAddress"], 'None']
                            try:
                                try:
                                    netDeviceInformationDict[network]['networkDevice'][localInterfaceIP] = \
                                    netDeviceInformationDict[network]['networkDevice'][localInterfaceIP] + '&' + (
                                        '/ '.join(macAndTypeList))
                                except:
                                    netDeviceInformationDict[network]['networkDevice'][localInterfaceIP] = '/ '.join(macAndTypeList)
                                    netDeviceInformationDict[network]['used'] +=1
                            except:
                                netDeviceInformationDict[network] = {'total':2**(32-eval(network.split('/')[1]))-2,'used':1,'networkDevice':{},'host':{}}
                                netDeviceInformationDict[network]['networkDevice'] = {localInterfaceIP:'/ '.join(macAndTypeList)}
        for network,netDict in self.netDirectInformationDict.items():
            if (self.checkTypeOfParam(network) != 'NETWORK'):
                continue
            for sysName,localInterfaceIP in netDict.items():
                for peerInterfaceIP,relativeDict in self.networkDict[sysName]['equipment2equipment'].items():
                    if(relativeDict["localInterfaceIP"] == localInterfaceIP and relativeDict["peerInterfaceIP"] not in netDeviceInformationDict[network]['networkDevice']):
                        try:
                            macAndTypeList = [relativeDict["peerInterfacePhysAddress"],self.macInformationDict[relativeDict["peerInterfacePhysAddress"][0:8].upper()]]
                        except:
                            macAndTypeList = [relativeDict["peerInterfacePhysAddress"],'None']
                        try:
                            netDeviceInformationDict[network]['host'][peerInterfaceIP]
                            continue
                        except:
                            netDeviceInformationDict[network]['host'][peerInterfaceIP] = '/ '.join(macAndTypeList)
                            netDeviceInformationDict[network]['used'] +=1
        #print(json.dumps(self.netDirectInformationDict, ensure_ascii='utf-8', indent=4))
        netList = list(netDeviceInformationDict.keys())
        #print(netList)
        prefixList = []
        for i in range(len(netList)):
            prefixList.append(netList[i].split('/')[1])
            netList[i] = IPy.IP(netList[i]).strBin()
        superNetworkInformationDict = self.getSuperNetworkInformationDict(netList, prefixList)
        self.comboSuperNetAndDeviceInformation(superNetworkInformationDict,netDeviceInformationDict)
        #print(json.dumps(netDeviceInformationDict, ensure_ascii='utf-8', indent=4))
        return netDeviceInformationDict,superNetworkInformationDict

    @log.classFuncDetail2Log('DEBUG')
    def compareDevicesLevel(self,paramONE,paramTWO,preList=None):
        if not self.netDirectInformationDict:
            self.netDirectInformationDict = self.getNetDirectInformationFromDict()
        print(paramONE,paramTWO)
        if (paramONE == paramTWO):
            return 100
        if not preList:
            preList = []
        counts = 100
        print('preList: ',end= '')
        print(preList)
        netDict1 = self.getDeviceConnectedDict(paramONE,self.netDirectInformationDict)
        netDict2 = self.getDeviceConnectedDict(paramTWO,self.netDirectInformationDict)
        print('netDict1: ', end='')
        print(netDict1)
        print('netDict2: ',end= '')
        print(netDict2)
        part = len(netDict1)+len(netDict2)
        resultDict1 = {}
        resultDict2 = {}
        for NETWORK1 in netDict1:
            if NETWORK1 not in netDict2:
                if(netDict1[NETWORK1]):
                    try:
                        netDict1[NETWORK1][NETWORK1]
                    except:
                        continue
                    for sysName in netDict1[NETWORK1][NETWORK1].keys():
                        if sysName != paramONE:
                            if sysName != paramTWO:
                                if sysName not in preList:
                                    resultDict1[NETWORK1] = {sysName: netDict1[NETWORK1][NETWORK1][sysName]}
            else:
                part -= 1
        for NETWORK2 in netDict2:
            if NETWORK2 not in netDict1:
                if (netDict2[NETWORK2]):
                    try:
                        netDict2[NETWORK2][NETWORK2]
                    except:
                        continue
                    for sysName in netDict2[NETWORK2][NETWORK2].keys():
                        if sysName != paramTWO:
                            if sysName != paramONE:
                                if sysName not in preList:
                                    resultDict2[NETWORK2] = {sysName: netDict2[NETWORK2][NETWORK2][sysName]}
        print('resultDict1:  ', end='')
        print(resultDict1)
        print('resultDict2:  ', end='')
        print(resultDict2)
        similarNetDict = {}
        if(len(resultDict1) > len(resultDict2)):
            resultDictTemp = resultDict1
            resultDict1 =resultDict2
            resultDict2 = resultDictTemp
        if(resultDict1 == None and resultDict2 == None):
            print('%s和%s属于同层次设备'%(paramONE
                                        ,paramTWO))
            return 100
        for NETWORK1 in resultDict1:
            mostSimilarNet = NETWORK1
            maxLength = 0
            for NETWORK2 in resultDict2:
                length = self.getCommonPrefixLength(IPy.IP(NETWORK1).strBin(),IPy.IP(NETWORK2).strBin())
                if(length > maxLength):
                    maxLength = length
                    mostSimilarNet = NETWORK2
            similarNetDict[NETWORK1] = mostSimilarNet
        print(similarNetDict)
        for NETWORK in similarNetDict:
            for sysName1 in list(resultDict1[NETWORK].keys()):
                try:
                    resultDict2[similarNetDict[NETWORK]]
                except:
                    continue
                for sysName2 in list(resultDict2[similarNetDict[NETWORK]].keys()):
                    preList = preList + [paramONE, paramTWO]
                    counts = counts - 2*(100-self.compareDevicesLevel(sysName1,sysName2,preList))/(part)
                    resultDict2[similarNetDict[NETWORK]].pop(sysName2)
                    resultDict1[NETWORK].pop(sysName1)
                    if (resultDict1[NETWORK] == {}):
                        resultDict1.pop(NETWORK)
                    if (resultDict2[similarNetDict[NETWORK]] == {}):
                        resultDict2.pop(similarNetDict[NETWORK])
        if(resultDict2):
            #print('总连接数：',end='')
            #print(part)
            #print('不同连接数：',end='')
            #print(2*(len(resultDict2)+len(resultDict1)))
            for i in resultDict2:
                print(resultDict2[i].keys(),'')
            counts = counts - 2*(len(resultDict2)+len(resultDict1))*(100-0)/(part)
        #print('counts: ',end='')
        #print(counts)
        return counts


def main():
    net = OperationNetwork('../logs/networkInformation.txt')
    net.networkInfo_update()
    #net.getVrrpDeviceDict()
    # netDirectInformation = net.getNetDirectInformationFromDict()
    #net.getNetInformationFromDict()
    #print(net.getDeviceConnectedDict("ZYZX-WS-C05-DMZ-S9306-1",netDirectInformation))
    #print(json.dumps(net.getEdgeNetInformationDict(), ensure_ascii='utf-8', indent=4))
    #net.getEdgeDeviceInformationDict()
    #net.getNetDeviceInformationTreeDict()
    #print(net.checkTypeOfParam('127.0.0.0/8'))
    print(json.dumps(net.getNetDeviceInformationTreeDict(), ensure_ascii='utf-8', indent=4))
    #print(json.dumps(net.getEdgeDeviceInformationDict(), ensure_ascii='utf-8', indent=4))
    #print(json.dumps(net.getNetDirectInformationFromDict(), ensure_ascii='utf-8', indent=4))
    #print(json.dumps(net.getNetDirectInformationBeSelected("10.47.146.128/29"), ensure_ascii='utf-8', indent=4))
    #print(json.dumps(net.getDeviceNetInformationFromDict('FZFJ-WS-1F-C12-OA-CORE-NE40E-1'), ensure_ascii='utf-8',indent=4))
    #print(json.dumps(net.vrrpDeviceStatic, ensure_ascii='utf-8', indent=4))
    # param1 = 'FJFZ-SJ-CORE-4Fnan-E27-S9306-1'
    # param2 = 'FJFZ-SJ-CORE-4Fnan-E28-S9306-2'
    #net.compareDevicesLevel(param1,param2,netDirectInformation)
    #print(net.compareDevicesLevel('FJFZ-RJY-CORE-CLOUD-D05-S9310-1', 'FJFZ-RJY-CORE-D05/D06-H3C7610',netDirectInformation))
    #print(net.compareDevicesLevel('FJFZ-SJ-CORE-4Fnan-E27-S9306-1', 'FJFZ-SJ-CORE-4Fnan-E28-S9306-2',netDirectInformation))
    #！！！！！！！
    #print(net.compareDevicesLevel('FJFZ-RJY-PC-3F-JR-ZXR5952-3', 'FJFZ-WS-PC-7F-JR-5352-2',netDirectInformation))
    #问题出现了
    #param1 = ['FJFZ-WS-CORE-C01-E8000E-1']
    #param2 = ['FJFZ-WS-CORE-C02-E8000E-2']
    #print(net.checkDeviceList(param1,param2,[],[],netDirectInformation))
    #print(net.pathTrace('FJFZ-RJY-CORE-CLOUD-D06-S9310-2', '10.47.146.126'))
    #print(json.dumps(net.pathTrace('ZYZX-WS-C05-DMZ-S9306-1', '172.20.176.137'), ensure_ascii='utf-8', indent=4))


if __name__ == '__main__':
    main()
