import mysql.connector
import sys

sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.services import SmartPixl
from app.config import Config
from app.constants import SleepingTime, SQSConstants, DataSourceCode
from app.services import AmazonSQS
import time
from datetime import datetime, timedelta
import json
from pytz import timezone

tz = timezone('EST')
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('previous_datafinder_log.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

smartpixl_object = SmartPixl()
aws_object = AmazonSQS()


def hitEmailDB():
    retrieve_sqs_input_data, retrieve_sqs_input_data_status = aws_object.retrieveBunchOfMessages(
        Config.PREVIOUS_DATA_QUEUE_NAME)
    if len(retrieve_sqs_input_data) == 0:
        return SQSConstants.EMPTYQUEUEMESSAGE, True
    mydb = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN, passwd=Config.DB_PASSWORD_MAIN,
                                   database=Config.DB_NAME_MAIN)
    mycursor = mydb.cursor(buffered=True)
    valid_list = []
    email_append_list = []
    email_hygiene_list = []
    for_dump_list = []
    logger.info("started local Db data finder")
    for message in retrieve_sqs_input_data:
        message_body = json.loads(message.body)
        logger.debug({"message": message_body})
        record_id = list(message_body.keys())[0]
        values_present = list(message_body.values())[0]
        email = values_present.get('email', '')
        # print(email)
        datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        current_timestamp = (datetime.utcnow() - timedelta(
            days=SleepingTime.EMAIlDUMPEXPIRATION)).strftime('%Y-%m-%d %H:%M:%S')
        record_id_query = f"SELECT smartpixl_recordId, email, email_status FROM {Config.EMAIL_LIST_TABLE_NAME} WHERE " \
                          f"created >= '{current_timestamp}' and smartpixl_recordId = '{record_id}'"
        mycursor.execute(record_id_query)
        db_record_id_data = mycursor.fetchone()
        if db_record_id_data:
            values_present['email'] = db_record_id_data[1]
            values_present['email_status'] = db_record_id_data[2]
            values_present['email_source_code'] = DataSourceCode.EMAILDUMP
            valid_list.append({record_id: values_present})
        elif email:
            email_query = f"SELECT smartpixl_recordId, email, email_status FROM {Config.EMAIL_LIST_TABLE_NAME} WHERE " \
                          f"created >= '{current_timestamp}' and LOWER(email) = LOWER('{email}')"
            mycursor.execute(email_query)
            db_email_data = mycursor.fetchone()
            if db_email_data:
                values_present['email'] = db_email_data[1]
                values_present['email_status'] = db_email_data[2]
                values_present['email_source_code'] = DataSourceCode.EMAILAPPENDHYGIENEDUMP if \
                    values_present.get('email_source_code') == DataSourceCode.DATAZAPP else \
                    DataSourceCode.EMAILHYGIENEDUMP
                valid_list.append({record_id: values_present})
                for_dump_list.append({record_id: values_present})
            else:
                email_hygiene_list.append({record_id: values_present})
        else:
            email_append_list.append({record_id: values_present})
    try:
        send_to_sqs_email_hygiene_message, send_to_sqs_email_hygiene_status = aws_object.sendBunchOfMessages(
            Config.DATA_HYGIENE_QUEUE_NAME, email_hygiene_list)
        logger.info(f"Length of email_hygiene_list {len(email_hygiene_list)}")
        send_to_sqs_email_append_message, send_to_sqs_email_append_status = aws_object.sendBunchOfMessages(
            Config.DATA_APPEND_QUEUE_NAME, email_append_list)
        logger.info(f"Length of email_append_list {len(email_append_list)}")
        send_to_sqs_valid_message, send_to_sqs_valid_status = aws_object.sendBunchOfMessages(
            Config.VALID_EMAIL_QUEUE_NAME, valid_list)
        logger.info(f"Length of valid_list {len(valid_list)}")
        send_to_sqs_dump_message, send_to_sqs_dump_status = aws_object.sendBunchOfMessages(
            Config.DUMP_LIST_UPDATION_QUEUE_NAME, for_dump_list)
    except:
        logger.error('Previous Data finder', exc_info=True)
        return "SQS Error", False
    if send_to_sqs_email_hygiene_status and send_to_sqs_email_append_status and send_to_sqs_valid_status and \
            send_to_sqs_dump_status:
        deleted_message, deleted_status = aws_object.deleteMessages(retrieve_sqs_input_data)
        return deleted_message, deleted_status
    else:
        logger.info("Error in queue insertion")
        return "Error in deletion", False


if __name__ == "__main__":
    while True:
        hit_message, hit_status = hitEmailDB()
        if hit_message == SQSConstants.EMPTYQUEUEMESSAGE:
            logger.info("Sleeping")
            time.sleep(SleepingTime.QUEUECHECKERTIME)
        elif not hit_status:
            logger.info(hit_message)
            break
