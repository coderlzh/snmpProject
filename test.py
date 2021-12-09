# # # import pandas as pd
# # # import SnmpOperation
# # # df = pd.read_excel('./10.46.97.252.MIB.xlsx', usecols='C,E')
# # # result = []
# # # sn =SnmpOperation.OperationSnmp('1q3e!Q#E','10.46.97.252','161')
# # # for oid in df.values:
# # #     if(oid[1] =='不可访问'):
# # #         result.append('')
# # #         continue
# # #     if(type(oid[0]) ==str):
# # #         if('.' in oid[0]):
# # #             result.append('\n'.join(sn.walk([oid[0][1::]])[0]))
# # #         else:
# # #             result.append('')
# # #     else:
# # #         result.append('')
# # # df.insert(2,'H',result)
# # # print(df)
# # # df.to_excel('./test.xlsx')
# # # # df_input = pd.DataFrame()
# # # # df.to_excel('./10.46.97.252.MIB.xlsx', index=False)
# # # # # for oid in df.iloc[:, 2]:
# # # # #     if('.' in oid):
# #
# # # print(str(tuple([2]+[i for i in range(2)])))
# # # sql = '123 %s %s'%tuple(i for i in range(2))+' %s'
# # # print(sql)
# # # dict1 = {'a':1,'b':2}
# # # print(list(i for i in tuple(i for i in dict1)))
# # # b ='a'
# # # a = eval(b)
# # # print(a)
# # # 装饰器就是一个'平常不过'的函数
# # # def my_decorator(func):
# # #     print( "I am an ordinary function")
# # #     def wrapper():
# # #         print( "I am function returned by the decorator")
# # #         func()
# # #     return wrapper
# # #
# # # # 因此你可以不用"@"也可以调用他
# # #
# # # def lazy_function():
# # #     print ("zzzzzzzz")
# # #
# # # decorated_function = my_decorator(lazy_function)
# # # #输出: I am an ordinary function
# # #
# # # # 之所以输出 "I am an ordinary function"是因为你调用了函数,
# # # # 并非什么魔法.
# # #
# # # @my_decorator
# # # def lazy_function():
# # #     print ("zzzzzzzz")
# # #
# # # #输出: I am an ordinary function
# # #
# # # lazy_function()
# # # class IOrderRepository:
# # #
# # #     def fetch_one_by(self, nid):
# # #         raise Exception('子类中必须实现该方法')
# # #
# # #
# # # class Something(IOrderRepository):
# # #     def fetch_one_by(self, nid):
# # #         pass
# # #
# # #
# # # st =Something()
# #
# # # class Father():
# # #     def __init__(self, name):
# # #         self.name = name
# # #         print("Im father")
# # #
# # #
# # # class Son_1(Father):
# # #     def __init__(self, age, name):
# # #         self.age = age
# # #         Father.__init__(self, name)
# # #         print("Im Son_1")
# # #
# # #
# # # class Son_2(Father):
# # #     def __init__(self, gender, name):
# # #         self.gender = gender
# # #         Father.__init__(self, name)
# # #         print("我是Son_2")
# # #
# # #
# # # class GrandSon(Son_1, Son_2):
# # #     def __init__(self, name, age, gender):
# # #         Son_1.__init__(self, age, name)
# # #         Son_2.__init__(self, gender, name)
# # #         pass
# # # grand_son = GrandSon("张三", 18, "男")
# # # print(grand_son.__class__.__mro__)
# # #
# # # print(["1","2","3"]+["2"])
# # #
# # #
# # # print(list(range(0,2)))
# # #
# # #
# # # import datetime
# # # yesterday = datetime.date.today() +datetime.timedelta(-1)
# # # print(yesterday)
# # # print(int(11/2))
# # #
# # # class Solution:
# # #     def checkNumberCanBeUsed(self,i,j,board):
# # #         numCanBeSelected = [str(num+1) for num in range(9)]
# # #         for num in board[i]:
# # #             if(num !='.'):
# # #                 if(num in numCanBeSelected):
# # #                     numCanBeSelected.remove(num)
# # #         for num in [board[row][j] for row in range(9)]:
# # #             if(num !='.'):
# # #                 if(num in numCanBeSelected):
# # #                     numCanBeSelected.remove(num)
# # #         for row in range(3*(i//3),3*(i//3)+3):
# # #             for col in range(3*(j//3),3*(j//3)+3):
# # #                 if(board[row][col]!='.'):
# # #                     if(board[row][col] in numCanBeSelected):
# # #                         numCanBeSelected.remove(board[row][col])
# # #         return numCanBeSelected
# # #
# # #     def dps(self,board) -> bool:
# # #         row, col = -1, -1
# # #         for i in range(9):
# # #             for j in range(9):
# # #                 if (board[i][j] == '.'):
# # #                     row = i
# # #                     col = j
# # #                     print("i:" + str(row) + ",j:" + str(col))
# # #                     numCanBeSelected = self.checkNumberCanBeUsed(row, col, board)
# # #                     print(numCanBeSelected)
# # #                     if not numCanBeSelected:
# # #                         return False
# # #                     for num in numCanBeSelected:
# # #                         print("i:" + str(row) + ",j:" + str(col))
# # #                         print(num)
# # #                         board[row][col] = num
# # #                         if not self.dps(board):
# # #                             board[row][col] = '.'
# # #                         else:
# # #                             return True
# # #                     return False
# # #         return True
# # #     def solveSudoku(self, board) -> None:
# # #         """
# # #         Do not return anything, modify board in-place instead.
# # #         """
# # #         self.dps(board)
# # #
# # #
# # #
# # # board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
# # #
# # # X=Solution()
# # # print(X.solveSudoku(board))
# # # print(board)
# #
# # # class Solution:
# # #     def combinationSum(self, candidates, target: int):
# # #         self.nums = sorted(candidates)
# # #         self.res = []
# # #         self.digui(0, target, [])
# # #         return self.res
# # #
# # #     def digui(self, idx, target, cur):
# # #         for i in range(idx, len(self.nums)):
# # #             print("target: " + str(target))
# # #             print("self.nums[i]: " + str(self.nums[i]))
# # #             if self.nums[i] < target:
# # #                 self.digui(i, target - self.nums[i], cur + [self.nums[i]])
# # #             elif self.nums[i] == target:
# # #                 self.res.append(cur + [self.nums[i]])
# # #                 print("bingo")
# # #                 break
# # #             else:
# # #                 print("roll back")
# # #                 break
# # # X=Solution()
# # # candidates = [2,3,6,7]
# # # target = 7
# # # print(X.combinationSum(candidates,target))
# #
# # # test = [1,2,3,4]
# # #
# # # for i in range(len(test)):
# # #     test[i] = 1
# # # test = test[1:]
# # # print(test)
# # #
# # # class Solution:
# # #     def ways(self, pizza, k: int) -> int:
# # #         self.methods = 0
# # #         self.pizza = pizza
# # #         Apple = self.getPizzaApples()
# # #         self.dps(Apple, k, pizza)
# # #         return self.methods
# # #
# # #     def dps(self, apple, k, pizza):
# # #         if (k > apple):
# # #             print('rollback')
# # #             return
# # #         if (k == 1):
# # #             print('bingo')
# # #             self.methods += 1
# # #             return
# # #         for line in range(1, len(pizza)):
# # #             print('pizza: ' + str(pizza))
# # #             #print('pizza ID:' + str(id(pizza)))
# # #             appleBeCutted, pizzaBeLeft = self.rowcut(line, pizza.copy())
# # #             #print('pizza: ' + str(pizza))
# # #             #print('pizza ID:' + str(id(pizza)))
# # #             print('pizzaBeLeftID:' + str(id(pizzaBeLeft)))
# # #             print('pizzaBeLeft:' + str(pizzaBeLeft))
# # #             if (appleBeCutted > 0):
# # #                 self.dps(apple - appleBeCutted, k - 1, pizzaBeLeft)
# # #         for line in range(1, len(pizza[0])):
# # #             print('pizza: ' + str(pizza))
# # #             #print('pizza ID:' + str(id(pizza)))
# # #             appleBeCutted, pizzaBeLeft = self.colcut(line, pizza.copy())
# # #             #print('pizza: ' + str(pizza))
# # #             #print('pizza ID:' + str(id(pizza)))
# # #             print('pizzaBeLeftID:' + str(id(pizzaBeLeft)))
# # #             print('pizzaBeLeft:' + str(pizzaBeLeft))
# # #             if (appleBeCutted > 0):
# # #                 self.dps(apple - appleBeCutted, k - 1, pizzaBeLeft)
# # #
# # #     def getPizzaApples(self):
# # #         apple = 0
# # #         for i in range(len(self.pizza)):
# # #             for j in self.pizza[i]:
# # #                 if j == 'A':
# # #                     apple += 1
# # #         return apple
# # #
# # #     def rowcut(self, line, pizza):
# # #         print('rowcut')
# # #         apple = 0
# # #         for i in range(line):
# # #             for j in range(len(pizza[i])):
# # #                 if (pizza[i][j]) == 'A':
# # #                     apple += 1
# # #         pizza = pizza[line:]
# # #         return apple, pizza
# # #
# # #     def colcut(self, line, pizza):
# # #         print('colcut')
# # #         apple = 0
# # #         for i in range(len(pizza)):
# # #             for j in range(line):
# # #                 if (pizza[i][j]) == 'A':
# # #                     apple += 1
# # #             pizza[i] = pizza[i][line:]
# # #         #print(id(pizza))
# # #         return apple, pizza
# # # X= Solution()
# # # pizza =["A..","AA.","..."]
# # # k = 3
# # # print(X.ways(pizza,k))
# # #
# # #
# # # strlist = '456798'
# # # print(strlist[:-2:])
# # # class Solution:
# # #     def minSteps(self, n: int) -> int:
# # #         stack = ''
# # #         stringOutPut = 'A'
# # #         self.counts = 99999
# # #         self.dps(0, n, stack, stringOutPut)
# # #         return self.counts
# # #
# # #
# # #     def copyAll(self,stack,stringOutPut):
# # #         return stringOutPut
# # #
# # #     def paste(self,stack,stringOutPut):
# # #         stringOutPut  += stack
# # #         return  stringOutPut
# # #
# # #     def dps(self,counts,n,stack,stringOutPut):
# # #         #print("stack: " + stack)
# # #         length = len(stringOutPut)
# # #         #print("stringOutPut: " + stringOutPut)
# # #         if(length > n):
# # #             #print("rollback")
# # #             return
# # #         if(length == n):
# # #             #print("bingo")
# # #             self.counts = min(self.counts,counts)
# # #             return
# # #         if(stringOutPut != stack):
# # #             stack_temp = self.copyAll(stack,stringOutPut)
# # #             counts += 1
# # #             #print("copy()")
# # #             self.dps(counts,n,stack_temp,stringOutPut)
# # #             counts -= 1
# # #         if(stack):
# # #             #print("paste()")
# # #             stringOutPut = self.paste(stack,stringOutPut)
# # #             counts += 1
# # #             self.dps(counts,n,stack,stringOutPut)
# # #             counts -= 1
# # #
# # # X= Solution()
# # # print(X.minSteps(3))
# #
# # # import json
# # #xu
# # # dict1 = {'1':1,'2':2}
# # # dict1['0'] = dict1.pop('2')
# # # print(json.dumps(dict1,ensure_ascii=False))
# #
# # # list1 = '1234567'
# # # print(len(list1))
# # # print(list1[0:6]+list1[7:])
# # # print('No such idot.'.startswith('No such'))
# # # num = 1
# # # while(num<=100):
# # #     print(num)
# # #     num +=1
# # # import re
# # # import pandas as pd
# # # with open('./test.txt', 'r+') as f:
# # #     str1 = f.read()
# # #     pattern = re.compile(
# # #         r'\[\'((([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5]))\', \'([^,]*)\', \'([^,]*)\'\]')
# # #     result = pattern.finditer(str1)
# # #     whiteList = []
# # #     for i in result:
# # #         whiteList.append(i.group(5))
# # # for white in whiteList:
# # #     print(white)
# # # df = pd.read_excel('./网络设备登记.xlsx', usecols='C,H')
# # # for i in df.values:
# # #     print(i)
# # import IPy
# # # for i in IPy.IP('192.168.1.0').make_net('255.255.255.0'):
# # #     print(i)
# # # print(IPy.IP('10.0.0.0/23') == IPy.IP('10.0.0.0').make_net('255.255.255.0'))
# # # dict = {IPy.IP('10.0.0.0').make_net('255.255.255.0'):123}
# # # for i in dict:
# # #     print(i)
# # #     print(IPy.IP('10.0.0.0/25') in i)
# # # #print('/'.join(['1']))
# # # # list1 = ['1','2','3']
# # # # list1.reverse()
# # # # print(list1)
# # # dict1 ={'1':{}}
# # # print(bool(dict1['1']))
# # # #print(IPy.IP('10.46.127.1') in IPy.IP('10.46.127.1/31'))
# # #
# # # test = [i for i in range(100)]
# # # print(test[200:200])
# # # print(test[50:100])
# # # print(test[50:])
# # # import time
# # # import datetime
# # # timeArray = time.localtime(1573780920)
# # # print(timeArray)
# # # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# # # #datetime1=datetime.datetime.strptime(, "%Y-%m-%d %H:%M:%S")
# # # #print(datetime1)
# # import IPy
# # # print(eval('192.168.0.0/30'.split('/')[1])<32)
# # print(IPy.IP('10.47.145.2').make_net('255.255.255.240').strNormal(1))
# # # # string = '123'
# # # dict1 = {'1':1,'2':2}
# # # dict2 = {'3':3,'4':4}
# # # for i in dict1:
# # #     for j in list(dict2.keys()):
# # #         dict2.pop(j)
# # #     print(dict2)
# # # -*- coding:utf8 -*-
# # # import winrm
# # # #
# # # # ip = '10.46.79.97'
# # # # username = '1051366162@qq.com'
# # # # password = '1999111wodegege'
# # # # shell = 'ipconfig /all'
# # # #
# # # # s = winrm.Session(ip, auth=(username, password), transport='ntlm')  # 远程连接windows
# # # # r = s.run_ps(shell)  # 执行脚本
# # # # print(r.status_code)
# # # # print(r.std_out)
# # # import time
# # # import sys
# # # for i in range(5):
# # # #     print(i, end='\r')
# # # #     #sys.stdout.flush()
# # # #     time.sleep(2)
# # # # # 注释打开和关闭效果不同
# # # import sys, time
# # #
# # # for i in range(20):
# # #     print('#', end='', flush=True)
# # #     time.sleep(0.4)
# # # def animation(num):
# # #     if(num%4 == 0):
# # #         return '-'
# # #     elif (num % 4 == 1):
# # #         return '/'
# # #     elif (num % 4 == 2):
# # #         return '|'
# # #     else:
# # #         return '\\'
# # # import time
# # # for i in range(10):
# # #     time.sleep(0.4)
# # #     print('\r',i,animation(i),end='')
# def longestCommonPrefix(strs):
#     """
#     :type strs: List[str]
#     :rtype: str
#     """
#     if not strs:
#         return ''
#     s1 = min(strs)
#     print(s1)
#     s2 = max(strs)
#     print(s2)
#     for i, c in enumerate(s1):
#         if c != s2[i]:
#             return s1[:i]
#     return s1
# print(longestCommonPrefix(['123','124','1234']))
# # # -*- coding:utf-8 -*-
# # """
# # Description:大变双向字典树
# # 迭代次数默认最大999，可以增加但是没必要。其实能深到999层，那这个序列还是选择另外的处理方式吧。
# #
# # @author: WangLeAi
# # @date: 2018/8/15
# # """
# #
# #
# # class TrieNode(object):
# #     def __init__(self, value=None, count=0, parent=None):
# #         # 值
# #         self.value = value
# #         # 频数统计
# #         self.count = count
# #         # 父结点
# #         self.parent = parent
# #         # 子节点，{value:TrieNode}
# #         self.children = {}
# #
# #
# # class Trie(object):
# #     def __init__(self):
# #         # 创建空的根节点
# #         self.root = TrieNode()
# #
# #     def insert(self, sequence):
# #         """
# #         基操，插入一个序列
# #         :param sequence: 列表
# #         :return:
# #         """
# #         cur_node = self.root
# #         for item in sequence:
# #             if item not in cur_node.children:
# #                 # 插入结点
# #                 child = TrieNode(value=item, count=1, parent=cur_node)
# #                 cur_node.children[item] = child
# #                 cur_node = child
# #             else:
# #                 # 更新结点
# #                 cur_node = cur_node.children[item]
# #                 cur_node.count += 1
# #
# #     def search(self, sequence):
# #         """
# #         基操，查询是否存在完整序列
# #         :param sequence: 列表
# #         :return:
# #         """
# #         cur_node = self.root
# #         mark = True
# #         for item in sequence:
# #             if item not in cur_node.children:
# #                 mark = False
# #                 break
# #             else:
# #                 cur_node = cur_node.children[item]
# #         # 如果还有子结点，说明序列并非完整
# #         if cur_node.children:
# #             mark = False
# #         return mark
# #
# #     def delete(self, sequence):
# #         """
# #         基操，删除序列，准确来说是减少计数
# #         :param sequence: 列表
# #         :return:
# #         """
# #         mark = False
# #         if self.search(sequence):
# #             mark = True
# #             cur_node = self.root
# #             for item in sequence:
# #                 cur_node.children[item].count -= 1
# #                 if cur_node.children[item].count == 0:
# #                     cur_node.children.pop(item)
# #                     break
# #                 else:
# #                     cur_node = cur_node.children[item]
# #         return mark
# #
# #     def search_part(self, sequence, prefix, suffix, start_node=None):
# #         """
# #         递归查找子序列，返回前缀和后缀结点
# #         此处简化操作，仅返回一位前后缀的内容与频数
# #         :param sequence: 列表
# #         :param prefix: 前缀字典，初始传入空字典
# #         :param suffix: 后缀字典，初始传入空字典
# #         :param start_node: 起始结点，用于子树的查询
# #         :return:
# #         """
# #         if start_node:
# #             cur_node = start_node
# #             prefix_node = start_node.parent
# #         else:
# #             cur_node = self.root
# #             prefix_node = self.root
# #         mark = True
# #         # 必须从第一个结点开始对比
# #         for i in range(len(sequence)):
# #             if i == 0:
# #                 if sequence[i] != cur_node.value:
# #                     for child_node in cur_node.children.values():
# #                         self.search_part(sequence, prefix, suffix, child_node)
# #                     mark = False
# #                     break
# #             else:
# #                 if sequence[i] not in cur_node.children:
# #                     for child_node in cur_node.children.values():
# #                         self.search_part(sequence, prefix, suffix, child_node)
# #                     mark = False
# #                     break
# #                 else:
# #                     cur_node = cur_node.children[sequence[i]]
# #         if mark:
# #             if prefix_node.value:
# #                 # 前缀数量取序列词中最后一词的频数
# #                 if prefix_node.value in prefix:
# #                     prefix[prefix_node.value] += cur_node.count
# #                 else:
# #                     prefix[prefix_node.value] = cur_node.count
# #             for suffix_node in cur_node.children.values():
# #                 if suffix_node.value in suffix:
# #                     suffix[suffix_node.value] += suffix_node.count
# #                 else:
# #                     suffix[suffix_node.value] = suffix_node.count
# #             # 即使找到一部分还需继续查找子结点
# #             for child_node in cur_node.children.values():
# #                 self.search_part(sequence, prefix, suffix, child_node)
# #
# #
# # if __name__ == "__main__":
# #     trie = Trie()
# #     texts = [["葬爱", "少年", "葬爱", "少年", "慕周力", "哈哈"], ["葬爱", "少年", "阿西吧"], ["烈", "烈", "风", "中"], ["忘记", "了", "爱"],
# #              ["埋葬", "了", "爱"]]
# #     for text in texts:
# #         trie.insert(text)
# #     markx = trie.search(["忘记", "了", "爱"])
# #     print(markx)
# #     markx = trie.search(["忘记", "了"])
# #     print(markx)
# #     markx = trie.search(["忘记", "爱"])
# #     print(markx)
# #     markx = trie.delete(["葬爱", "少年", "王周力"])
# #     print(markx)
# #     prefixx = {}
# #     suffixx = {}
# #     trie.search_part(["葬爱", "少年"], prefixx, suffixx)
# #     print(prefixx)
# #     print(suffixx)
# #
# # import IPy
# # print(IPy.IP('0x6000'))
# # !/usr/bin/python3
# # -*- coding=utf-8 -*-
# # 本模块由乾颐堂陈家栋编写，用于乾颐盾Python课程！
# # QQ: 594284672
# # 亁颐堂官网www.qytang.com
# # 乾颐盾课程包括传统网络安全（防火墙，IPS...）与Python语言和黑客渗透课程！
# from pysnmp.entity import engine, config
# from pysnmp.carrier.asynsock.dgram import udp
# from pysnmp.entity.rfc3413 import ntfrcv
# from pysnmp.proto.api import v2c
# import sys
#
# # Create SNMP engine with autogenernated engineID and pre-bound
# # snmpEngine = engine.SnmpEngine()
# #
# # config.addSocketTransport(
# #     snmpEngine,
# #     udp.domainName,
# #     udp.UdpTransport().openServerMode(('192.168.1.111', 162))
# # )
#
#
# # Callback function for receiving notifications
# # def cbFun(snmpEngine,
# #           stateReference,
# #           contextEngineId, contextName,
# #           varBinds,
# #           cbCtx):
# #     #    print('Notification received, ContextEngineId "%s", ContextName "%s"' % (
# #     #        contextEngineId.prettyPrint(), contextName.prettyPrint()
# #     #        )
# #     #    )
# #     for name, val in varBinds:
# #         #        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
# #         name = str(name)
# #         val = str(val)
# #         trapInfo = ''
# #         # cpu util in last 5s, rising threshold
# #         if '9.9.109.1.2.3.1.5.1.85' in name:
# #             trapInfo = '过去5秒的CPU利用率是 ' + val + '%'
# #             print('过去5秒的CPU利用率是 ' + val + '%')
# #         # falling threshold
# #         elif '9.9.109.1.2.4.1.4.1.1' in name:
# #             trapInfo = 'CPU利用率已经低于 ' + val + '%'
# #             print('CPU利用率已经低于 ' + val + '%')
# #         # ipsec tunnel start
# #         elif '1.3.6.1.4.1.9.9.171.2.0.7' in val:
# #             trapInfo = 'ipsec tunnel start'
# #             print('ipsec tunnel start')
# #         # ipsec tunnel stop
# #         elif '1.3.6.1.4.1.9.9.171.2.0.8' in val:
# #             trapInfo = 'ipsec tunnel stop'
# #             print('ipsec tunnel stop')
# #         # ipsla destination reachability inspection
# #         elif '9.9.42.1.2.19.1.9.1' in name:
# #             if '1' in val:
# #                 trapInfo = 'R2不可达!'
# #                 print('R2不可达!')
# #             else:
# #                 trapInfo = 'R2可达!'
# #                 print('R2可达!')
# #         if trapInfo != '':
# #             sendTrapInfo(trapInfo)
# #
#
# # def snmpv3_trap(user='', hash_meth=None, hash_key=None, cry_meth=None, cry_key=None, engineid=''):
# #     # usmHMACMD5AuthProtocol - MD5 hashing
# #     # usmHMACSHAAuthProtocol - SHA hashing
# #     # usmNoAuthProtocol - no authentication
# #     # usmDESPrivProtocol - DES encryption
# #     # usm3DESEDEPrivProtocol - triple-DES encryption
# #     # usmAesCfb128Protocol - AES encryption, 128-bit
# #     # usmAesCfb192Protocol - AES encryption, 192-bit
# #     # usmAesCfb256Protocol - AES encryption, 256-bit
# #     # usmNoPrivProtocol - no encryption
# #     hashval = None
# #     cryval = None
# #
# #     # NoAuthNoPriv
# #     if hash_meth == None and cry_meth == None:
# #         hashval = config.usmNoAuthProtocol
# #         cryval = config.usmNoPrivProtocol
# #     # AuthNoPriv
# #     elif hash_meth != None and cry_meth == None:
# #         if hash_meth == 'md5':
# #             hashval = config.usmHMACMD5AuthProtocol
# #         elif hash_meth == 'sha':
# #             hashval = config.usmHMACSHAAuthProtocol
# #         else:
# #             print('哈希算法必须是md5 or sha!')
# #             return
# #         cryval = config.usmNoPrivProtocol
# #     # AuthPriv
# #     elif hash_meth != None and cry_meth != None:
# #         if hash_meth == 'md5':
# #             hashval = config.usmHMACMD5AuthProtocol
# #         elif hash_meth == 'sha':
# #             hashval = config.usmHMACSHAAuthProtocol
# #         else:
# #             print('哈希算法必须是md5 or sha!')
# #             return
# #         if cry_meth == '3des':
# #             cryval = config.usm3DESEDEPrivProtocol
# #         elif cry_meth == 'des':
# #             cryval = config.usmDESPrivProtocol
# #         elif cry_meth == 'aes128':
# #             cryval = config.usmAesCfb128Protocol
# #         elif cry_meth == 'aes192':
# #             cryval = config.usmAesCfb192Protocol
# #         elif cry_meth == 'aes256':
# #             cryval = config.usmAesCfb256Protocol
# #         else:
# #             print('加密算法必须是3des, des, aes128, aes192 or aes256 !')
# #             return
# #     # 提供的参数不符合标准时给出提示
# #     else:
# #         print('三种USM: NoAuthNoPriv, AuthNoPriv, AuthPriv.。请选择其中一种。')
# #         return
# #
# #     # SNMPv3/USM setup
# #     # user: usr-md5-des, auth: MD5, priv DES, contextEngineId: 8000000001020304
# #     # this USM entry is used for TRAP receiving purposes
# #     config.addV3User(
# #         snmpEngine, user,
# #         hashval, hash_key,
# #         cryval, cry_key,
# #         contextEngineId=v2c.OctetString(hexValue=engineid)
# #     )
# #
# #     # Register SNMP Application at the SNMP engine
# #     ntfrcv.NotificationReceiver(snmpEngine, cbFun)
# #
# #     snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish
# #
# #     # Run I/O dispatcher which would receive queries and send confirmations
# #     try:
# #         snmpEngine.transportDispatcher.runDispatcher()
# #     except:
# #         snmpEngine.transportDispatcher.closeDispatcher()
# #         raise
# #
# #
# # if __name__ == '__main__':
# #     try:
# #         user = sys.argv[1]
# #         hm = sys.argv[2]
# #         hk = sys.argv[3]
# #         cm = sys.argv[4]
# #         ck = sys.argv[5]
# #         engineid = sys.argv[6]
# #         snmpv3_trap(user, hm, hk, cm, ck, engineid)
# #     except:
# #         print('参数设置应该如下:')
# #         print('python3 mytrap.py 用户名 认证算法 认证密钥 加密算法 加密密钥 engineID')
# #         print('认证算法支持md5和sha')
# #         print('加密算法支持3des, des, aes128, aes192, aes256')
# #         print('例如：')
# #         print('sudo python3 mytrap.py user1 sha Cisc0123 des Cisc0123 800000090300CA011B280000')
#
#
# # from pysnmp.hlapi import *
# #
# # g = sendNotification(SnmpEngine(),
# #                      CommunityData('public'),
# #                       UdpTransportTarget(('127.0.0.1', 162)),
# #                       ContextData(),
# #                       'trap',
# #                      NotificationType(ObjectIdentity('1.3.6.1.2.1.1.1.0','123')))
# #
# # print(next(g))
# # import IPy
# # print(IPy.IP('10.0.0.0/8').netmask().strNormal(1))
# # print('1'+'1')
# # Notification Originator Application (TRAP)
# # from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
# # from pysnmp.carrier.asynsock.dgram import udp
# # from pyasn1.codec.ber import encoder
# # from pysnmp.proto import api
# #
# # # Protocol version to use
# # verID = api.protoVersion2c
# # pMod = api.protoModules[verID]
# #
# # # Build PDU
# # trapPDU = pMod.TrapPDU()
# # pMod.apiTrapPDU.setDefaults(trapPDU)
# #
# # # Traps have quite different semantics among proto versions
# # if verID == api.protoVersion2c:
# #     var = []
# #     oid = (1, 3, 6, 1, 2, 1, 1, 5, 0)
# #     val = pMod.OctetString('12346')
# #     var.append((oid, val))
# #     pMod.apiTrapPDU.setVarBinds(trapPDU, var)
# #
# # # Build message
# # trapMsg = pMod.Message()
# # pMod.apiMessage.setDefaults(trapMsg)
# # pMod.apiMessage.setCommunity(trapMsg, 'public')
# # pMod.apiMessage.setPDU(trapMsg, trapPDU)
# #
# # transportDispatcher = AsynsockDispatcher()
# # transportDispatcher.registerTransport(
# #     udp.domainName, udp.UdpSocketTransport().openClientMode()
# # )
# # transportDispatcher.sendMessage(
# #     encoder.encode(trapMsg), udp.domainName, ('localhost', 162)
# # )
# # transportDispatcher.runDispatcher()
# # transportDispatcher.closeDispatcher()

# import time
#
# # 获得当前时间时间戳
# now = int(time.time())
# # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
# timeArray = time.localtime(now)
# otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
# print(otherStyleTime)
#from kafka import KafkaConsumer
#
# def get_partitions_number(server, topic):
#     consumer = KafkaConsumer(
#         topic,
#         bootstrap_servers=server
#     )
#     partitions = consumer.partitions_for_topic(topic)
#     return len(partitions)
# print(get_partitions_number('10.46.97.234:9092','network'))
# from utils import KafkaOperation
# import json


# kf = KafkaOperation.OperationKafka()
# consumer = kf.createKafkaConsumer('10.46.97.234:9092',topic='SendMes')
# for msg in consumer:
#     MessageDict = json.loads(msg.value.decode('utf-8'))
#     print(MessageDict)


from utils import LogOperation
log = LogOperation.OperationLog()
class A(object):
    def __init__(self):
        self.name = 'A'
        self.value = 1

    @log.classFuncDetail2Log('DEBUG')
    def foo(self,x,param=2):
        print(x)
        print(self.name + 'foo')
        return 1

a =A()
print(a.foo(1,param = 3))
