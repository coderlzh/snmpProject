from pysnmp.hlapi import *
from utils import LogOperation
import time


class OperationSnmp:
    """
    snmp相关操作
    """

    def __init__(self,community,target, port):
        self.community = community
        self.target = target
        self.port = port

    def walk(self,oidList):
        """
        :param oidList:OID列表
        :return:OID所在分支的snmp结果

        SNMPv2c
        ++++++
        Functionally similar to:
        | $ snmpwalk -v2c -c community target oid

        example: snmpwalk -v2c -c 1q3e!Q#E 10.46.97.252 1.3.6.1.2.1.4.21.1.7
        """
        log = LogOperation.OperationLog()
        result = []
        mib = []
        for oid in oidList:
            mib.append(ObjectType(ObjectIdentity(oid)))
            result.append([])
        g = nextCmd(SnmpEngine(),
                    CommunityData(self.community, mpModel=1),
                    UdpTransportTarget((self.target, self.port)),
                    ContextData(),
                    *mib,
                    lexicographicMode=False)
        for (errorIndication, errorStatus, errorIndex, varBinds) in g:
            if errorIndication:
                print(errorIndication)
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for i in range(len(varBinds)):
                    result[i].append(varBinds[i][1].prettyPrint())
                    #result[i].append(' = '.join([x.prettyPrint() for x in varBinds[i]]))
                    log.logPrint(' = '.join([x.prettyPrint() for x in varBinds[i]]))
                    #print(' = '.join([x.prettyPrint() for x in varBinds[i]]))
        return result

    def getbulk(self,oidList):
        """
        :param oidList: OID列表
        :return: OID所在分支的snmp结果
        """
        result = []
        mib = []
        for oid in oidList:
            mib.append(ObjectType(ObjectIdentity(oid)))
        g = getCmd(SnmpEngine(),
                    CommunityData(self.community, mpModel=1),
                    UdpTransportTarget((self.target, self.port)),
                    ContextData(),
                    *mib)
        errorIndication, errorStatus, errorIndex, varBinds = next(g)
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                result.append(varBind[1].prettyPrint())
                #print(' = '.join([x.prettyPrint() for x in varBind]))

        return result

def animation(num):
    if(num%4 == 0):
        return '-'
    elif (num % 4 == 1):
        return '\\'
    elif (num % 4 == 2):
        return '|'
    else:
        return '/'

def main():
    sn1 = OperationSnmp('1q3e!Q#E','10.46.79.126','161')
    id = 0
    while(id<50):
        res = sn1.walk(['1.3.6.1.4.1.2011.6.3.4.1.2'])
        print('\r','CPU主板1CPU占用率：'+str(res[0][0])+'%'+'    ' + 'CPU主板2CPU占用率：'+str(res[0][1])+'%'+'    ' + 'CPU主板3CPU占用率：'+str(res[0][2])+'%',animation(id),end='')
        id +=1
        time.sleep(1)
if __name__ == '__main__':
    main()