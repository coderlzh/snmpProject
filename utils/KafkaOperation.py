import json
from kafka import KafkaConsumer
from kafka import KafkaProducer

class OperationKafka:
    """
    Kafka相关操作
    """
    def __init__(self):
        pass

    def createKafkaConsumer(self,target,topic):
        consumer = KafkaConsumer(topic,
                                 bootstrap_servers=target,
                                 auto_offset_reset='latest',  # 消费kafka中最近的数据，如果设置为earliest则消费最早的数据，不管这些数据是否消费
                                 enable_auto_commit=True,  # 自动提交消费者的offset
                                 auto_commit_interval_ms=3000,  ## 自动提交消费者offset的时间间隔
                                 group_id='None',
                                 # consumer_timeout_ms=10000,  # 如果10秒内kafka中没有可供消费的数据，自动退出
                                 client_id='consumer-python3'
                                 )
        return consumer

    def createKafkaProducer(self,target):
        producer = KafkaProducer(bootstrap_servers=target,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return producer

def main():
    pass

if __name__ == '__main__':
    main()
