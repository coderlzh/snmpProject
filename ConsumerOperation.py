import json
import KafkaOperation
import TableOperation
import MessageOperation
import LogOperation
import core

kf = KafkaOperation.OperationKafka()
consumer = kf.createKafkaConsumer('10.46.97.234:9092',topic='network')

def main():
    for msg in consumer:
        MessageDict = json.loads(msg.value.decode('utf-8'))
        print(MessageDict)
        if MessageDict['targetFunc'] == 'networkFlush':
            core.main()
            to = TableOperation.OperationTable()
            to.insertTreeDict2Database()
            ms = MessageOperation.OperationMessage()
            ReceiverList = []
            MessageSendFinal = ms.sendMessage2Kafka(ReceiverList)
            MessageJson = ms.message2json(MessageSendFinal)
            log = LogOperation.OperationLog()
            log.logPrint(MessageDict['timestamp'] + '      Message %s will be sent to kafka \n' % (MessageJson))
            producer = kf.createKafkaProducer('10.46.97.234:9092')
            producer.send('SendMes', MessageSendFinal)
if __name__ == '__main__':
    main()