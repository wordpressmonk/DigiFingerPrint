import sys
sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.config import Config
from app.constants import SQSConstants, SleepingTime, EmailStatus
from app.services import AmazonSQS
import json
import mysql.connector
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('dbupdate_logs.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


aws_object = AmazonSQS()


def smartPixlDataUpdation():
    retrieve_valid_sqs_messages, retrieve_valid_sqs_status = aws_object.retrieveBunchOfMessages(
            Config.VALID_EMAIL_QUEUE_NAME)
    if len(retrieve_valid_sqs_messages) == 0:
        return SQSConstants.EMPTYQUEUEMESSAGE, True
    logger.info("connecting to main database")
    try:
        main_db = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN,
                                          passwd=Config.DB_PASSWORD_MAIN, database=Config.DB_NAME_CLIENT_DATA)
        main_db.autocommit = True
        main_db_cursor = main_db.cursor(buffered=True)
    except Exception as e:
        return str(e), False
    logger.info("connecting to main Cpanel DB")
    try:
        cpanel_db = mysql.connector.connect(host=Config.DB_HOST_PIXL3, user=Config.DB_USER_PIXL3,
                                            passwd=Config.DB_PASSWORD_PIXL3, database=Config.DB_NAME_PIXL3)
        cpanel_db.autocommit = True
        cpanel_db_cursor = cpanel_db.cursor(buffered=True)
    except Exception as e:
        return str(e), False
    logger.info("Started processing the queue")
    try:
        for message in retrieve_valid_sqs_messages:
            message_body = json.loads(message.body)
            record_id = list(message_body.keys())[0]
            values_obtained = list(json.loads(message.body).values())[0]    
            pixl_id = values_obtained['pixlId']
            email_status = values_obtained['email_status']
            email_source_code = values_obtained['email_source_code']
            email = values_obtained['email']
            # print(f"{email}, {email_status}, {email_source_code}")
            if email_status == EmailStatus.VALIDEMAILSTATUS and pixl_id == 3:
                table_name = f"{Config.SMARTPIXL_DATA_TABLE_NAME}"
                command = f"INSERT INTO {table_name}"
                cpanel_sql = command + "(smartpixl_recordId, companyId, pixlId, first_name, last_name, email, email_status, email_source_code, smartpixl_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (record_id, values_obtained['companyId'], values_obtained['pixlId'], values_obtained['params']['FirstName'], values_obtained['params']['LastName'], email, email_status, email_source_code, json.dumps(values_obtained['smartpixl_data']))
                cpanel_db_cursor.execute(cpanel_sql, values)
            table_name = f"{Config.SMARTPIXL_DATA_TABLE_NAME}_{pixl_id}"
            # print(table_name)
            sql = "UPDATE %s SET email = '%s', email_status = '%s', email_source_code = %s WHERE " \
                  "smartpixl_recordId = '%s'" % (table_name, email, email_status, email_source_code, record_id)
            # print(sql)
            main_db_cursor.execute(sql)
            # print("executed")
        main_db.commit()
        deleted_message, deleted_status = aws_object.deleteMessages(retrieve_valid_sqs_messages)
        return deleted_message, deleted_status
    except Exception as e:
        return str(e), False


if __name__ == "__main__":
    while True:
        db_updation_message, db_updation_status = smartPixlDataUpdation()
        if db_updation_message == SQSConstants.EMPTYQUEUEMESSAGE:
            logger.info("sleeping")
            sleep(SleepingTime.QUEUECHECKERTIME)
        elif not db_updation_status:
            logger.error(db_updation_message)
            break

