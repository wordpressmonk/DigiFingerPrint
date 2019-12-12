import sys
sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.config import Config
from app.constants import SleepingTime, SQSConstants
from app.services import AmazonSQS
import json
import mysql.connector
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('dump_data_insertion_log.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

aws_object = AmazonSQS()


def insertionDump():
    retrieve_dump_sqs_messages, retrieve_dump_sqs_status = aws_object.retrieveBunchOfMessages(
        Config.DUMP_LIST_UPDATION_QUEUE_NAME)
    if len(retrieve_dump_sqs_messages) == 0:
        return SQSConstants.EMPTYQUEUEMESSAGE, True
    try:
        logger.info("Connecting MYSQL")
        mydb = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN,
                                       passwd=Config.DB_PASSWORD_MAIN, database=Config.DB_NAME_MAIN)
        mydb.autocommit = True
        mycursor = mydb.cursor(buffered=True)
        for message in retrieve_dump_sqs_messages:
            message_body = json.loads(message.body)
            logger.debug({"message": message_body})
            record_id = list(message_body.keys())[0]
            values_obtained = list(json.loads(message.body).values())[0]
            email_status = values_obtained['email_status']
            email = values_obtained['email']
            # print(email)
            email_source_code = values_obtained.get('email_source_code')
            command = "INSERT INTO %s " % Config.EMAIL_LIST_TABLE_NAME
            sql = command + "(smartpixl_recordId, email, email_status, email_source_code) VALUES (%s, %s, %s, %s)"
            values = (record_id, email, email_status, email_source_code)
            mycursor.execute(sql, values)
        mydb.commit()
        logger.info("Inserted successfully")
        deleted_message, deleted_status = aws_object.deleteMessages(retrieve_dump_sqs_messages)
        return deleted_message, deleted_status
    except Exception as e:
        logger.error('Dump Insertion', exc_info=True)
        return str(e), False


if __name__ == "__main__":
    while True:
        insertion_message, insertion_status = insertionDump()
        if insertion_message == SQSConstants.EMPTYQUEUEMESSAGE:
            logger.info("sleeping")
            sleep(SleepingTime.QUEUECHECKERTIME)
        elif not insertion_status:
            break
