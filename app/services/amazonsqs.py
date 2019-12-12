import boto3
from app.constants import SQSConstants
import json


class AmazonSQS(object):
    def __init__(self):
        self.sqs = boto3.resource('sqs')

    def sendBunchOfMessages(self, queue_name, data):
        maxBatchSize = 10
        if not data:
            return SQSConstants.EMPTYINPUTMESSAGE, True
        bunch_data_list = [data[x:x + maxBatchSize] for x in range(0, len(data), maxBatchSize)]
        for bunch_data in bunch_data_list:
            entries = []
            for record in bunch_data:
                entry = dict()
                values = list(record.values())[0]
                entry['Id'] = str(list(record.keys())[0])
                entry['MessageBody'] = json.dumps(record)
                entry['MessageGroupId'] = str(values['companyId'])
                entries.append(entry)
            try:
                queue = self.sqs.get_queue_by_name(QueueName=queue_name)
                response = queue.send_messages(Entries=entries)
            except Exception as e:
                return str(e), False
        return response, True

    def retrieveBunchOfMessages(self, queue_name):
        try:
            queue = self.sqs.get_queue_by_name(QueueName=queue_name)
            received_message_set = queue.receive_messages(MaxNumberOfMessages=SQSConstants.SQSRETRIEVALLIMIT,
                                                          VisibilityTimeout=SQSConstants.SQSRETRIEVALVISIBILITY)
            return received_message_set, True
        except Exception as e:
            return str(e), False

    def deleteMessages(self, messages):
        if type(messages) != list:
            messages = [messages]
        if len(messages) == 0:
            return "Empty message", True
        try:
            for message in messages:
                message.delete()
            return "success", True
        except:
            print("queue deletion failed")
            return "failed", False
