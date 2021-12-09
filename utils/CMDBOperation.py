import requests
import json
from utils import LogOperation

log = LogOperation.OperationLog()

class OprationCMDB:

    def __init__(self):
        pass


    # def RouterSysInformationGET(self):
    #     try:
    #         log = LogOperation.OperationLog()
    #         data = {
    #             "objectClass":1043,
    #             "keyword":"1043",
    #             "mode":0,
    #             "columnNames":["SYSNAME1","STATUS"],
    #             "conditions":[{"fieldName":"OBJECT_CLASS","fieldValue":"1050","mode":2}]
    #         }
    #         data = json.dumps(data, ensure_ascii=False,indent=4)
    #         url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/search'
    #         response = requests.post(url, data=data)
    #         log.logPrint(str(response))
    #     except Exception as e:
    #         log = LogOperation.OperationLog()
    #         log.logPrint(e)
    #         return e
    #
    # def SwitchSysInformationGET(self):
    #     try:
    #         log = LogOperation.OperationLog()
    #         data = {
    #             "objectClass":1043,
    #             "keyword":"1043",
    #             "mode":0,
    #             "columnNames":["SYSNAME1","STATUS"],
    #             "conditions":[{"fieldName":"OBJECT_CLASS","fieldValue":"1053","mode":2}]
    #         }
    #         data = json.dumps(data, ensure_ascii=False,indent=4)
    #         url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/search'
    #         response = requests.post(url, data=data)
    #         log.logPrint(str(response))
    #     except Exception as e:
    #         log = LogOperation.OperationLog()
    #         log.logPrint(e)
    #         return e
    #
    # def RouterInformationGET(self):
    #     try:
    #         log = LogOperation.OperationLog()
    #         data = {
    #             "objectClass": 1054,
    #             "keyword": "1054",
    #             "mode": 0,
    #             "columnNames": ["SYSNAME1", "STATUS"],
    #             "conditions": [{"fieldName": "OBJECT_CLASS", "fieldValue": "1054", "mode": 2}]
    #         }
    #         data = json.dumps(data, ensure_ascii=False, indent=4)
    #         url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/search'
    #         response = requests.post(url, data=data)
    #         log.logPrint(str(response))
    #     except Exception as e:
    #         log = LogOperation.OperationLog()
    #         log.logPrint(e)
    #         return e
    #
    # def InterfaceInformationGET(self):
    #     try:
    #         log = LogOperation.OperationLog()
    #         data = {
    #             "objectClass": 1045,
    #             "keyword": "1045",
    #             "mode": 0,
    #             "columnNames": ["SYSNAME1", "STATUS"],
    #             "conditions": [{"fieldName": "OBJECT_CLASS", "fieldValue": "1045", "mode": 2}]
    #         }
    #         data = json.dumps(data, ensure_ascii=False, indent=4)
    #         url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/search'
    #         response = requests.post(url, data=data)
    #         log.logPrint(str(response))
    #     except Exception as e:
    #         log = LogOperation.OperationLog()
    #         log.logPrint(e)
    #         return e
    #
    # def RelatinonshipInformationGET(self):
    #     try:
    #         log = LogOperation.OperationLog()
    #         data = {
    #             "objectClass": 1046,
    #             "keyword": "1046",
    #             "mode": 0,
    #             "columnNames": ["SYSNAME1", "STATUS"],
    #             "conditions": [{"fieldName": "OBJECT_CLASS", "fieldValue": "1046", "mode": 2}]
    #         }
    #         data = json.dumps(data, ensure_ascii=False, indent=4)
    #         url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/search'
    #         response = requests.post(url, data=data)
    #         log.logPrint(str(response))
    #     except Exception as e:
    #         log = LogOperation.OperationLog()
    #         log.logPrint(e)
    #         return e
    @log.classFuncDetail2Log('DEBUG')
    def RouterSysInformationPOST(self,dataDict,dataList):
        temp = {}
        temp['OBJECT_CLASS']= '1054'
        temp['SEARCHCODE']=''
        temp['NAME']=dataDict['sysName']
        temp['STATUS']='使用中'
        temp['SYSNAME']='网络管理SNMP'
        temp['OPERATOR']='李至恒'
        temp['NAME'] = dataDict['sysSNID']
        temp['SYSDESCR'] = dataDict['sysDescr']
        temp['SYSOBJECTID'] = dataDict['sysObjectID']
        temp['SYSUPTIME'] = dataDict['sysUpTime']
        temp['SYSCONTACT'] = dataDict['sysContact']
        temp['SYSNAME1'] = dataDict['sysName']
        temp['SYSLOCATION'] = dataDict['sysLocation']
        temp['SYSIFNUMBER'] = dataDict['sysIfNumber']
        temp['SYSFORWADING'] = dataDict['sysForwarding']
        temp['SYSSERVICES'] = dataDict['sysSevices']
        dataList.append(temp)
        return dataList

    @log.classFuncDetail2Log('DEBUG')
    def SwtichSysInformationPOST(self,dataDict,dataList):
        temp ={}
        temp['OBJECT_CLASS']= '1043'
        temp['SEARCHCODE']=''
        temp['NAME']=dataDict['sysName']
        temp['STATUS']='使用中'
        temp['SYSNAME']='网络管理SNMP'
        temp['OPERATOR']='李至恒'
        temp['NAME'] = dataDict['sysSNID']
        temp['SYSSNID'] = dataDict['sysSNID']
        temp['SYSDESCR'] = dataDict['sysDescr']
        temp['SYSOBJECTID'] = dataDict['sysObjectID']
        temp['SYSUPTIME'] = dataDict['sysUpTime']
        temp['SYSCONTACT'] = dataDict['sysContact']
        temp['SYSNAME1'] = dataDict['sysName']
        temp['SYSLOCATION'] = dataDict['sysLocation']
        temp['SYSIFNUMBER'] = dataDict['sysIfNumber']
        temp['SYSFORWADING'] = dataDict['sysForwarding']
        temp['SYSSERVICES'] = dataDict['sysSevices']
        dataList.append(temp)
        return dataList

    @log.classFuncDetail2Log('DEBUG')
    def RouterInformationPOST(self,dataDict,dataList,sysName):
        for row in dataDict:
            temp = {}
            temp['OBJECT_CLASS']= '1045'
            temp['SEARCHCODE']=''
            temp['STATUS']='使用中'
            temp['SYSNAME']='网络管理SNMP'
            temp['OPERATOR']='李至恒'
            temp['NAME'] = dataDict[row]['routerUniqueID']
            temp['ROUTERUNIQUEID'] = dataDict[row]['routerUniqueID']
            temp['SYSNAME1'] = sysName
            temp['ROUTERDEST'] = dataDict[row]['routerDest']
            temp['ROUTERIFINDEX'] = dataDict[row]['routerIfIndex']
            temp['ROUTERIFIP'] = dataDict[row]['routerIfIP']
            temp['ROUTERNEXTHOP'] = dataDict[row]['routerNextHop']
            temp['ROUTERMASK'] = dataDict[row]['routerMask']
            dataList.append(temp)
        return dataList

    @log.classFuncDetail2Log('DEBUG')
    def InterfaceInformationPOST(self,dataDict,dataList,sysName):
        for row in dataDict:
            temp = {}
            temp['OBJECT_CLASS']= '1050'
            temp['SEARCHCODE']=''
            temp['STATUS']='使用中'
            temp['SYSNAME']='网络管理SNMP'
            temp['OPERATOR']='李至恒'
            temp['NAME'] = dataDict[row]['interfaceUniqueID']
            temp['INTERFACEUNIQUEID'] = dataDict[row]['interfaceUniqueID']
            temp['SYSNAME1'] = sysName
            temp['INTERFACEID'] = dataDict[row]['interfaceID']
            temp['INTERFACENAME'] = dataDict[row]['interfaceName']
            temp['INTERFACEIP'] = dataDict[row]['interfaceIP']
            temp['INTERFACENETMASK'] = dataDict[row]['interfaceNetmask']
            temp['INTERFACEADMINSTATUS'] = dataDict[row]['interfaceAdminStatus']
            temp['INTERFACEOPERSTATUS'] = dataDict[row]['interfaceOperStatus']
            temp['INTLASTCHANGE'] = dataDict[row]['interfaceLastChange']
            temp['INTERFACEPHYSADDRESS'] = dataDict[row]['interfacePhysAddress']
            temp['INTERFACESDESC'] = dataDict[row]['interfaceDesc']
            dataList.append(temp)
        return dataList

    @log.classFuncDetail2Log('DEBUG')
    def RelationshipInformationPOST(self,dataDict,dataList,sysName):
        for row in dataDict:
            temp = {}
            temp['OBJECT_CLASS']= '1046'
            temp['SEARCHCODE']=''
            temp['STATUS']='使用中'
            temp['SYSNAME']='网络管理SNMP'
            temp['OPERATOR']='李至恒'
            temp['NAME'] = dataDict[row]['relativeUniqueID']
            temp['RELATIVEUNIQUEID'] = dataDict[row]['relativeUniqueID']
            temp['LOCALSYSNAME'] = sysName
            temp['LOCALINTERFACEID'] = dataDict[row]['localInterfaceID']
            temp['LOCALINTERFACEIP'] = dataDict[row]['localInterfaceIP']
            temp['PEERSYSNAME'] = dataDict[row]['peerSysName']
            temp['PEERINTERFACEIP'] = dataDict[row]['peerInterfaceIP']
            temp['PEERINTPHYSADDRESS'] = dataDict[row]['peerInterfacePhysAddress']
            temp['PEERSYSFORWADING'] = dataDict[row]['peerSysForwarding']
            dataList.append(temp)
        return dataList

    @log.classFuncDetail2Log('DEBUG')
    def AllInformationPOST(self,dataDict):
        sysName =dataDict['equipmentSysInformation']['sysName']
        dataList = []
        dataList = self.RouterSysInformationPOST(dataDict['equipmentSysInformation'],dataList)
        dataList = self.InterfaceInformationPOST(dataDict['equipmentInterfaceInformation'],dataList,sysName)
        dataList = self.RelationshipInformationPOST(dataDict['equipment2equipment'],dataList,sysName)
        dataList = self.RouterSysInformationPOST(dataDict['equipmentSysInformation'],dataList)
        dataList = self.RouterInformationPOST(dataDict['equipmentRouterInformation'],dataList,sysName)
        log = LogOperation.OperationLog()
        data = json.dumps(dataList, ensure_ascii=False, indent=4)
        url = 'http://10.47.174.136:9018/bomc-resource-api/cmdb/data/batchSaveOrUpdate'
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=data.encode("utf-8"), headers=headers)
        return 0

def main():
    pass

if __name__ == '__main__':
    main()
