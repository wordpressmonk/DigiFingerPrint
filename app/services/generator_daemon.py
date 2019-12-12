import sys

sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.config import Config
from app.constants import SleepingTime, SQSConstants, DataSourceCode, EmailStatus
from app.services import AmazonSQS
from app.services.datazapp import emailAppendApi
import json
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('generator_log.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

aws_object = AmazonSQS()



def emailGenerator():
    to_hit_local_db = []
    to_valid_queue = []
    for_dump_list = []
    retrieve_append_sqs_messages, retrieve_append_sqs_status = aws_object.retrieveBunchOfMessages(
        Config.DATA_APPEND_QUEUE_NAME)
    if len(retrieve_append_sqs_messages) == 0:
        return SQSConstants.EMPTYQUEUEMESSAGE, True
    logger.info("started email append process")
    for message in retrieve_append_sqs_messages:
        message_body = json.loads(message.body)
        logger.debug({"message": message_body})
        record_id = list(message_body.keys())[0]
        values_present = list(message_body.values())[0]
        params = values_present['params']
        old_email = values_present.get('email', '')
        email_append_api_data, email_append_api_status = emailAppendApi(params)
        logger.debug({"datazapp": email_append_api_data})
        new_email = ''
        try:
            new_email = email_append_api_data['ResponseDetail']['Data'][0]['Email']
        except Exception as e:
            logger.error('Datazapp Failed', exc_info=True)
        if old_email and new_email and old_email.lower() == new_email.lower():
            values_present['email_source_code'] = DataSourceCode.DATAZAPP
            for_dump_list.append({record_id: values_present})
            to_valid_queue.append({record_id: values_present})
            logger.info("Pushed to for_dump_list & to_valid_queue")
        elif new_email:
            values_present['email'] = new_email
            values_present['email_source_code'] = DataSourceCode.DATAZAPP
            to_hit_local_db.append({record_id: values_present})
            logger.info("Pushed to to_hit_local_db")
        elif old_email:
            for_dump_list.append({record_id: values_present})
            to_valid_queue.append({record_id: values_present})
            logger.info("Pushed to for_dump_list & to_valid_queue")
        else:
            logger.info("No data from APPEND API")
    logger.info("Finished processing the queue")
    send_to_sqs_dump, send_to_sqs_dump_status = aws_object.sendBunchOfMessages(
        Config.DUMP_LIST_UPDATION_QUEUE_NAME, for_dump_list)
    logger.info(f"Length of for dump_list {len(for_dump_list)}")
    send_to_sqs_valid_message, send_to_sqs_valid_status = aws_object.sendBunchOfMessages(
        Config.VALID_EMAIL_QUEUE_NAME, to_valid_queue)
    logger.info(f"Length of to_valid_queue {len(to_valid_queue)}")
    send_to_sqs_previous_message, send_to_sqs_previous_status = aws_object.sendBunchOfMessages(
        Config.PREVIOUS_DATA_QUEUE_NAME, to_hit_local_db)
    logger.info(f"Length of to_hit_local_db {len(to_hit_local_db)}")
    if send_to_sqs_dump_status and send_to_sqs_valid_status and send_to_sqs_previous_status:
        deleted_message, deleted_status = aws_object.deleteMessages(retrieve_append_sqs_messages)
        logger.info("successfully deleted")
        return deleted_message, deleted_status
    else:
        logger.info("deletion failed")
        return "failed", False


if __name__ == "__main__":
    while True:
        generator_message, generator_status = emailGenerator()
        if generator_message == SQSConstants.EMPTYQUEUEMESSAGE:
            logger.info("sleeping")
            sleep(SleepingTime.QUEUECHECKERTIME)
        elif not generator_status:
            break
