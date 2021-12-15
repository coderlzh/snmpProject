import json

from utils import kafka_model, message_model, log_model, table_model


kf = kafka_model.OperationKafka()
consumer = kf.createKafkaConsumer('10.46.97.234:9092', topic='network')

log = log_model.OperationLog()

@log.Detail2Log('DEBUG')
def manhattanTransfer(MessageDict):
    modules, func = MessageDict['targetFunc'].split('/')
    obj = __import__("AbilityLayer." + modules, fromlist=True)
    if hasattr(obj, func):
        func = getattr(obj, func)
        res = func(**MessageDict['param'])
        return res

@log.Detail2Log('DEBUG')
def main():
    for msg in consumer:
        if not msg.value:
            continue
        MessageDict = json.loads(msg.value.decode('utf-8'))
        print(MessageDict)
        res = manhattanTransfer(MessageDict)
        producer = kf.createKafkaProducer('10.46.97.234:9092')
        producer.send('SendMes', res)


if __name__ == '__main__':
    main()
