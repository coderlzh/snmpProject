from utils import mysql_model, network_model
import time
from utils import log_model
from abc import ABC, abstractmethod
from utils.tool_model import getTime

log = log_model.OperationLog()

#    __
#   (_    _   _  _    _
#   __） |\| | \/ \  | )
#                   |


class Table(ABC):
    pass


class OperationTable:
    """
    数据表相关操作相关操作
    """

    def __init__(self):
        pass

    @log.classFuncDetail2Log('DEBUG')
    def dropExsistTable(self, table):
        sql = 'drop table if exists %s' % (table)
        Operation = mysql_model.OperationMysql()
        res = Operation.drop_one(sql)
        if (res):
            return res

    @log.classFuncDetail2Log('DEBUG')
    def createTableEquipmentSysInformation(self):
        Operation = mysql_model.OperationMysql()
        sql = "CREATE TABLE IF NOT EXISTS equipmentSysInformation%s(\
        sysSnID VARCHAR(255) NOT NULL COMMENT '设备唯一标识符',\
        sysDescr VARCHAR(255) NOT NULL COMMENT '设备的描述 OID:1.3.6.1.2.1.1.1.0(get)',\
        sysObjectID VARCHAR(100) NOT NULL COMMENT '设备厂商授权标识符 OID:1.3.6.1.2.1.1.2.0(get)',\
        sysUpTime VARCHAR(100) NOT NULL COMMENT '设备重启后的时间量 OID:1.3.6.1.2.1.1.3.0(get)',\
        sysContact VARCHAR(255) NOT NULL COMMENT '设备提供机构 OID:1.3.6.1.2.1.1.4.0(get)',\
        sysName VARCHAR(255) NOT NULL COMMENT '设备名称 OID:1.3.6.1.2.1.1.5.0(get)',\
        sysLocation VARCHAR(255) NOT NULL COMMENT '设备物理位置 OID:1.3.6.1.2.1.1.6.0(get)',\
        sysIfNumber INT NOT NULL COMMENT'设备接口总量 OID:1.3.6.1.2.1.2.1.0(get)',\
        sysForwarding INT NOT NULL COMMENT'设备转发状态。exp：转发设备(1)、非转发设备(2) OID:1.3.6.1.2.1.4.1.0(get)',\
        sysSevices INT NOT NULL COMMENT '设备工作于OSI的层次。exp：物理层、数据链路层、网络层(78)、传输层、表示层、会话层、应用层 OID:1.3.6.1.2.1.1.7.0(get)',\
        PRIMARY KEY (sysSnID)\
        )DEFAULT CHARSET=utf8;" % (time.strftime('%Y%m%d'))
        res = Operation.create_one(sql)
        if not res:
            print('Create table equipmentSysInformation%s sucessfully.' % (time.strftime('%Y%m%d')))
            return 0
        else:
            print(res)
            return 1

    @log.classFuncDetail2Log('DEBUG')
    def createTableEquipmentInterfaceInformation(self):
        Operation = mysql_model.OperationMysql()
        sql = "CREATE TABLE IF NOT EXISTS equipmentInterfaceInformation%s(\
        sysName VARCHAR(255) NOT NULL COMMENT '设备名称 OID:1.3.6.1.2.1.1.5.0(get)',\
        interfaceUniqueID VARCHAR(255) NOT NULL COMMENT '接口唯一标识符 由SN码和接口ID组成',\
        interfaceID INT NOT NULL COMMENT '设备接口ID OID:1.3.6.1.2.1.2.2.1.1(walk)',\
        interfaceName VARCHAR(255) NOT NULL COMMENT '接口名称 OID:1.3.6.1.2.1.2.2.1.2(walk)',\
        interfaceIP VARCHAR(100) COMMENT '接口IP OID:1.3.6.1.2.1.4.20.1.1(walk) 1.3.6.1.2.1.4.20.1.2(walk)',\
        interfaceNetmask VARCHAR(100) COMMENT '接口网络地址掩码 OID:1.3.6.1.2.1.4.20.1.3(walk)',\
        interfaceAdminStatus INT NOT NULL COMMENT '接口管理状态 OID:1.3.6.1.2.1.2.2.1.7(walk)',\
        interfaceOperStatus INT NOT NULL COMMENT '接口操作状态 OID:1.3.6.1.2.1.2.2.1.8(walk)',\
        interfaceLastChange INT NOT NULL COMMENT '接口状态最后变更时间 OID:1.3.6.1.2.1.2.2.1.9(walk)',\
        interfacePhysAddress VARCHAR(100) NOT NULL COMMENT '接口MAC地址 OID:1.3.6.1.2.1.2.2.1.6(walk)',\
        interfaceDesc VARCHAR(255) NOT NULL COMMENT '接口描述 OID:1.3.6.1.2.1.31.1.1.1.18(walk)',\
        PRIMARY KEY (interfaceUniqueID )\
        )DEFAULT CHARSET=utf8;" % (time.strftime('%Y%m%d'))
        res = Operation.create_one(sql)
        if not res:
            print('Create table equipmentInterfaceInformation%s sucessfully.' % (time.strftime('%Y%m%d')))
            return 0
        else:
            print(res)
            return 1

    @log.classFuncDetail2Log('DEBUG')
    def createTableEquipmentRouterInformation(self):
        Operation = mysql_model.OperationMysql()
        sql = "CREATE TABLE IF NOT EXISTS equipmentRouterInformation%s(\
        sysName VARCHAR(255) NOT NULL COMMENT '设备名称 OID:1.3.6.1.2.1.1.5.0(get)',\
        routerUniqueID VARCHAR(255) NOT NULL COMMENT '路由唯一标识符 由SN码和路由目的组成',\
        routerDest VARCHAR(100) NOT NULL COMMENT '路由目的IP OID:1.3.6.1.2.1.4.21.1.1(walk)',\
        routerIfIndex INT NOT NULL COMMENT '路由出接口ID OID:1.3.6.1.2.1.4.21.1.2(walk)',\
        routerIfIP VARCHAR(100) COMMENT '路由出接口IP OID:1.3.6.1.2.1.4.20.1.2(walk)',\
        routerNextHop VARCHAR(100) COMMENT '路由下一跳IP OID:1.3.6.1.2.1.4.21.1.7(walk)',\
        routerMask VARCHAR(100) COMMENT '路由目的网络掩码 OID:1.3.6.1.2.1.4.21.1.11(walk)',\
        PRIMARY KEY (routerUniqueID)\
        )DEFAULT CHARSET=utf8;" % (time.strftime('%Y%m%d'))
        res = Operation.create_one(sql)
        if not res:
            print('Create table equipmentRouterInformation%s sucessfully.' % (time.strftime('%Y%m%d')))
            return 0
        else:
            print(res)
            return 1

    @log.classFuncDetail2Log('DEBUG')
    def createTableEquipment2equipment(self):
        Operation = mysql_model.OperationMysql()
        sql = "CREATE TABLE IF NOT EXISTS equipment2equipment%s(\
        localSysName VARCHAR(255) NOT NULL COMMENT '本地设备名称 OID:1.3.6.1.2.1.1.5.0(get)',\
        relativeUniqueID VARCHAR(255) NOT NULL COMMENT '路由唯一标识符 由本地设备SN码和对端设备接口IP组成',\
        localInterfaceID INT NOT NULL COMMENT '本地设备相连接口ID OID:1.3.6.1.2.1.4.22.1.1(walk)',\
        localInterfaceIP VARCHAR(100) NOT NULL COMMENT '本地设备相连接口IP OID:1.3.6.1.2.1.4.20.1.1(walk)',\
        peerSysName VARCHAR(100) COMMENT '对端设备名称 OID:1.3.6.1.2.1.1.5.0(get)',\
        peerInterfaceIP VARCHAR(100) NOT NULL COMMENT '对端设备相连接口IP OID:1.3.6.1.2.1.4.22.1.3(walk)',\
        peerInterfacePhysAddress VARCHAR(100) NOT NULL COMMENT '对端设备相连接口MAC/终端设备MAC OID:1.3.6.1.2.1.4.22.1.2(walk)',\
        peerSysForwarding INT COMMENT '对端设备类型。exp：转发设备(1)、终端(2) OID:1.3.6.1.2.1.4.1.0(get)',\
        PRIMARY KEY (relativeUniqueID)\
        )DEFAULT CHARSET=utf8;" % (time.strftime('%Y%m%d'))
        res = Operation.create_one(sql)
        if not res:
            print('Create table equipment2equipment%s sucessfully.' % (time.strftime('%Y%m%d')))
            return 0
        else:
            print(res)
            return 1

    @log.classFuncDetail2Log('DEBUG')
    def createTableTerminalSnmpUnenabled(self):
        Operation = mysql_model.OperationMysql()
        sql = "CREATE TABLE IF NOT EXISTS terminalSnmpUnenabled(\
        id INT NOT NULL AUTO_INCREMENT COMMENT '本表的主键',\
        terminalIP  VARCHAR(100) NOT NULL COMMENT '未开启snmp协议的终端设备IP',\
        PRIMARY KEY (id )\
        )DEFAULT CHARSET=utf8;"
        res = Operation.create_one(sql)
        if not res:
            print('Create table terminalSnmpUnenabled sucessfully.')
            return 0
        else:
            print(res)
            return 1

    @log.classFuncDetail2Log('DEBUG')
    def createTableAll(self):
        if (
                self.createTableEquipmentInterfaceInformation() or self.createTableEquipmentSysInformation() or self.createTableEquipmentRouterInformation() or self.createTableEquipment2equipment() or self.createTableTerminalSnmpUnenabled()):
            return 'Create all table failed!'

    @log.classFuncDetail2Log('DEBUG')
    def insertDictionary2Database(self, Dict):
        sysName = Dict['equipmentSysInformation']['sysName']
        for tableName in Dict:
            if (tableName == 'neighborDict'):
                continue
            if (tableName == 'equipmentSysInformation'):
                """
                    "equipmentSysInformation": {
                        "sysSNID": "2102350RHQ10L1000004",
                        "sysDescr": "Huawei Versatile Routing Platform Software \r\nVRP (R) software, Version 8.180 (NE40E V800R010C10SPC500) \r\nCopyright (C) 2012-2018 Huawei Technologies Co., Ltd. \r\nHUAWEI NE40E-X2-M8A \r\n",
                        "sysObjectID": "SNMPv2-SMI::enterprises.2011.2.62.24",
                        "sysUpTime": "184363026",
                        "sysContact": "R&D Beijing, Huawei Technologies co.,Ltd.",
                        "sysName": "FZFJ-WS-1F-C12-OA-CORE-NE40E-1",
                        "sysLocation": "Beijing China",
                        "sysSevices": "78",
                        "sysIfNumber": "71",
                        "sysForwarding": "1"
                        },
                """
                sql = "insert into equipmentSysInformation%s" % (
                    time.strftime('%Y%m%d')) +" (sysSnID,sysDescr,sysObjectID,sysUpTime,sysContact,sysName,sysLocation,sysSevices,sysIfNumber,sysForwarding)" +" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " + \
                      "ON DUPLICATE KEY UPDATE sysSnID = VALUES(sysSnID),sysDescr=VALUES(sysDescr),sysObjectID=VALUES(sysObjectID), sysUpTime=VALUES(sysUpTime),sysContact=VALUES(sysContact),sysName=VALUES(sysName),sysLocation=VALUES(sysLocation),sysSevices=VALUES(sysSevices),sysIfNumber=VALUES(sysIfNumber),sysForwarding=VALUES(sysForwarding)"
                data = []
                data.append(tuple(Dict[tableName][i] for i in Dict[tableName]))
                Operation = mysql_model.OperationMysql()
                res = Operation.insert_all(sql, tuple(data))
                if (res):
                    print(res)
                else:
                    print('insert data to %s%s successfully' % (tableName, time.strftime('%Y%m%d')))
            elif (tableName == 'equipmentRouterInformation'):
                """
                "109": {
                    "routerUniqueID": "2102350RHQ10L100000410.46.83.41",
                    "routerDest": "10.46.83.41",
                    "routerIfIndex": "93",
                    "routerIfIP": "10.46.83.124",
                    "routerNextHop": "0.0.0.0",
                    "routerMask": "255.255.255.255"
                },
                """
                sql = "insert into equipmentRouterInformation%s" % (
                    time.strftime('%Y%m%d')) +" (sysName,routerUniqueID,routerDest,routerIfIndex,routerIfIP,routerNextHop,routerMask)" +" values(%s,%s,%s,%s,%s,%s,%s) " + \
                      "ON DUPLICATE KEY UPDATE sysName=VALUES(sysName),routerUniqueID = VALUES(routerUniqueID),routerDest=VALUES(routerDest),routerIfIndex=VALUES(routerIfIndex),routerIfIP=VALUES(routerIfIP) ,routerNextHop=VALUES(routerNextHop) , routerMask=VALUES(routerMask)"
                data = tuple(tuple([sysName] +
                             list([Dict[tableName][m][i] for i in Dict[tableName][m]])) for m in Dict[tableName])
                Operation = mysql_model.OperationMysql()
                res = Operation.insert_all(sql, tuple(data))
                if (res):
                    print(res)
                else:
                    print('insert data to %s%s successfully' % (tableName, time.strftime('%Y%m%d')))

            elif (tableName == 'equipment2equipment'):
                """
                "10.46.83.214": {
                    "relativeUniqueID": "2102350RHQ10L100000410.46.83.214",
                    "localInterfaceID": "94",
                    "localInterfaceIP": "10.46.83.252",
                    "peerInterfaceIP": "10.46.83.214",
                    "peerInterfacePhysAddress": "0x00e070c5dd96",
                    "peerSysName": "",
                    "peerSysForwarding": ""
                    },
                """
                sql = "insert into equipment2equipment%s" % (
                    time.strftime('%Y%m%d')) +" (localSysName,relativeUniqueID,localInterfaceID,localInterfaceIP,peerInterfaceIP,peerInterfacePhysAddress,peerSysName,peerSysForwarding)"+" values(%s,%s,%s,%s,%s,%s,%s,%s) " + \
                      "ON DUPLICATE KEY UPDATE localSysName=VALUES(localSysName),relativeUniqueID =VALUES(relativeUniqueID),localInterfaceID=VALUES(localInterfaceID), localInterfaceIP=VALUES(localInterfaceIP),peerInterfaceIP=VALUES(peerInterfaceIP), peerInterfacePhysAddress=VALUES(peerInterfacePhysAddress) ,peerSysName=VALUES(peerSysName),peerSysForwarding = VALUES(peerSysForwarding)"
                data = tuple(tuple([sysName] +
                             list([Dict[tableName][m][i] for i in Dict[tableName][m]])) for m in Dict[tableName])
                Operation = mysql_model.OperationMysql()
                res = Operation.insert_all(sql, data)
                if (res):
                    print(res)
                else:
                    print('insert data to %s%s successfully' % (tableName, time.strftime('%Y%m%d')))

            else:
                """
                "1": {
                    "interfaceUniqueID": "2102350RHQ10L10000041",
                    "interfaceID": "1",
                    "interfaceName": "Virtual-Template0",
                    "interfacePhysAddress": "0x000000000000",
                    "interfaceAdminStatus": "1",
                    "interfaceOperStatus": "1",
                    "interfaceLastChange": "0",
                    "interfaceDesc": "",
                    "interfaceIP": "",
                    "interfaceNetmask": ""
                    },
                """
                sql = "insert into equipmentInterfaceInformation%s" % (
                    time.strftime('%Y%m%d')) +" (sysName,interfaceUniqueID,interfaceID,interfaceName,interfacePhysAddress,interfaceAdminStatus,interfaceOperStatus,interfaceLastChange,interfaceDesc,interfaceIP,interfaceNetmask)" +" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " + \
                      "ON DUPLICATE KEY UPDATE sysName=VALUES(sysName),interfaceUniqueID = VALUES(interfaceUniqueID),interfaceID=VALUES(interfaceID), interfaceName=VALUES(interfaceName),interfacePhysAddress=VALUES(interfacePhysAddress), interfaceAdminStatus=VALUES(interfaceAdminStatus),interfaceOperStatus=VALUES(interfaceOperStatus),interfaceLastChange=VALUES(interfaceLastChange),interfaceDesc=VALUES(interfaceDesc),interfaceIP=VALUES(interfaceIP),interfaceNetmask=VALUES(interfaceNetmask)"
                data = tuple(tuple([sysName] +
                             list([Dict[tableName][m][i] for i in Dict[tableName][m]])) for m in Dict[tableName])
                print(data)
                Operation = mysql_model.OperationMysql()
                res = Operation.insert_all(sql, data)
                if (res):
                    print(res)
                else:
                    print('insert data to %s%s successfully' % (tableName, time.strftime('%Y%m%d')))

    @log.classFuncDetail2Log('DEBUG')
    def insertSysName2Database(self, Sysname):
        sql = "insert into equipmentSysInformation%s(sysSnID,sysName) values ('%s','%s') ON DUPLICATE KEY UPDATE sysSnID = VALUES(sysSnID),sysName=VALUES(sysName) " % (
            time.strftime('%Y%m%d'), 'Unknown' + Sysname, Sysname)
        print(sql)
        Operation = mysql_model.OperationMysql()
        res = Operation.insert_one(sql)
        if (res):
            print(res)

    @log.classFuncDetail2Log('DEBUG')
    def selectFromDatabaseGroupByParam(self, table, param):
        sql = 'SELECT %s FROM %s group by %s;' % (param, table, param)
        Operation = mysql_model.OperationMysql()
        res = Operation.search_all(sql)
        return res

    @log.classFuncDetail2Log('DEBUG')
    def selectFromDatabase(self, table):
        sql = 'SELECT * FROM %s;' % (table)
        Operation = mysql_model.OperationMysql()
        res = Operation.search_all(sql)
        return res
        # print(res[0]['id'])
        # print(res[2]['id'])

    @log.classFuncDetail2Log('DEBUG')
    def insertTreeDict2Database(self):
        """
        "name": "0.0.0.0/0"
        "used": 2773,
        "netip": "0.0.0.0",
        "startip": "0.0.0.1",
        "broip": "255.255.255.255",
        "endip": "255.255.255.254",
        "total": 4294967294,
        "netmask": "0.0.0.0",
        "free": 4294964521
        :return:
        """


        def networkInfoDictPOST(data):
            sql = "insert into network_info_dict (UNIQUEID,PARENTNETWORK,NETWORK,NETMASK,STARTIP,ENDIP,BROAIP,NETIP,IPNUM,USED,FREE,HEARTBEATTIME,STATUS) \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
            UNIQUEID=VALUES(UNIQUEID),PARENTNETWORK=VALUES(PARENTNETWORK),NETWORK=VALUES(NETWORK),NETMASK=VALUES(NETMASK),STARTIP=VALUES(STARTIP),ENDIP=VALUES(ENDIP),BROAIP=VALUES(BROAIP),NETIP=VALUES(NETIP),IPNUM=VALUES(IPNUM),USED=VALUES(USED),FREE=VALUES(FREE),HEARTBEATTIME=VALUES(HEARTBEATTIME),STATUS=VALUES(STATUS)"
            #print(sql)
            Operation = mysql_model.OperationMysql()
            res = Operation.insert_all(sql, data)
            #print(res)

        def networkInfoPOST(data):
            sql = "insert into network_info (UNIQUEID,NETWORK,IP,SYSNAME,MAC,PRODUCER,IPTYPE,HEARTBEATTIME,USAGE_STATUS) \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
            UNIQUEID=VALUES(UNIQUEID),NETWORK=VALUES(NETWORK),IP=VALUES(IP),SYSNAME=VALUES(SYSNAME),MAC=VALUES(MAC),PRODUCER=VALUES(PRODUCER),IPTYPE=VALUES(IPTYPE),HEARTBEATTIME=VALUES(HEARTBEATTIME),USAGE_STATUS=VALUES(USAGE_STATUS)"
            #print(sql)
            Operation = mysql_model.OperationMysql()
            res = Operation.insert_all(sql, data)
            #print(res)

        def dfs(dataDict: dict,parentNetwork:str):
            data.append([parentNetwork+dataDict['name'],parentNetwork,dataDict['name'], dataDict['netmask'], dataDict['startip'], dataDict['endip'], dataDict['broip'],
            dataDict['netip'], dataDict['total'], dataDict['used'], dataDict['free']])
            try:
                for child in dataDict['children']:
                    dfs(child,dataDict['name'])
            except:
                return

        def getDiffDataList(databaseInfoDict,data):
            updateList = []
            insertList = []
            for info in data:
                info = [str(i) for i in info]
                try:
                    if databaseInfoDict[info[0]] != '&'.join(info):
                        updateList.append(info)
                except:
                    insertList.append(info)
            return updateList,insertList

        def changeNetDeviceInfo2data(dataDict):
            for network,networkDiCT in dataDict.items():
                for IP,IPInfo in networkDiCT['networkDevice'].items():
                    for i in IPInfo.split('&'):
                        iList = i.split('/ ')
                        data.append([network+IP+iList[1],network,IP]+iList+['1'])
                for IP,IPInfo in networkDiCT['host'].items():
                    for i in IPInfo.split('&'):
                        iList = i.split('/ ')
                        data.append([network+IP+iList[0],network,IP,'']+iList+['0'])

        def statusUPDATE(table,column):
            sql = "update %s set %s = 0"%(table,column)
            Operation = mysql_model.OperationMysql()
            res = Operation.updata_one(sql)
            return res
        statusUPDATE('network_info','usage_status')
        statusUPDATE('network_info_dict','status')
        net = network_model.OperationNetwork('../logs/networkInformation.txt')
        netDeviceInformationDict,superNetworkInformationDict = net.getNetDeviceInformationTreeDict()
        data = []
        dfs(superNetworkInformationDict,'startPoint')
        databaseInfoDict = self.networkInfoDictGET()
        dictUpdateList,dictInsertList = getDiffDataList(databaseInfoDict,data)
        heartBeatTime = getTime()
        for i in data:
            i.append(heartBeatTime)
            i.append(1)
        networkInfoDictPOST(data)
        data = []
        changeNetDeviceInfo2data(netDeviceInformationDict)
        databaseInfoDict = self.networkDeviceDictGET()
        infoUpdateList, infoInsertList = getDiffDataList(databaseInfoDict, data)
        for i in data:
            i.append(heartBeatTime)
            i.append(1)
        networkInfoPOST(data)
        return dictUpdateList,dictInsertList,infoUpdateList, infoInsertList

    @log.classFuncDetail2Log('DEBUG')
    def networkDeviceDictGET(self):
        sql = "select * from network_info"
        #print(sql)
        Operation = mysql_model.OperationMysql()
        resList = Operation.search_all(sql)
        resDict = {}
        for res in resList:
            valueList = []
            for key,value in res.items():
                valueList.append(str(value))
            resDict[res['UniqueID']] = '&'.join(valueList)
        return resDict

    @log.classFuncDetail2Log('DEBUG')
    def networkInfoDictGET(self):
        sql = "select * from network_info_dict"
        #print(sql)
        Operation = mysql_model.OperationMysql()
        resList = Operation.search_all(sql)
        resDict = {}
        for res in resList:
            valueList = []
            for key,value in res.items():
                valueList.append(str(value))
            resDict[res['UNIQUEID']] = '&'.join(valueList)
        return resDict

    @log.classFuncDetail2Log('DEBUG')
    def monitoringItemTypeGET(self):
        sql = 'SELECT itemid FROM history GROUP BY itemid;'
        Operation = mysql_model.OperationMysql()
        res = Operation.search_all(sql)
        return res

def main():
    to = OperationTable()
    to.insertTreeDict2Database()
    #to.createTableTerminalSnmpUnenabled()
    #print(to.networkInfoDictGET())

if __name__ == '__main__':
    main()
