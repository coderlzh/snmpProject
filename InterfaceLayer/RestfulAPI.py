from flask import Flask,request
import json
from utils import tool_model

# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
api = Flask(__name__)

# 'index'是接口路径，methods不写，默认get请求
@api.route('/DBNetworkInfoFlush', methods=['get'])
# get方式访问
def DBNetworkInfoFlush():
    from utils import kafka_model
    kf = kafka_model.OperationKafka()
    producer = kf.createKafkaProducer('10.46.97.234:9092')
    Time = tool_model.getTime()
    producer.send('network', value={'timestamp': Time,'targetFunc':'networkInfoAbility/networkInfoDetect','param':{}})
    ren = {'code': 200, 'msg': '正在完整更新网络设备信息表，更新完毕将以短信形式通知'}
    return json.dumps(ren, ensure_ascii=False)


@api.route('/pathTrace', methods=['POST'])
def pathTrace():
    data = request.get_json()
    print(data)
    ren = {'code': 200, 'msg': '路径计算完成'}
    return json.dumps(ren, ensure_ascii=False)

if __name__ == '__main__':
    api.run(port=8088, debug=True, host='127.0.0.1')  # 启动服务
