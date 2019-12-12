import sys
sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.config import Config
from app.constants import EmailStatus, DataSourceCode, SleepingTime, SQSConstants
from app.services import AmazonSQS
from app.services.bulkemailchecker import bulkVerifier
import json
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('verifier_log.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

aws_object = AmazonSQS()


def emailVerifier():
    retrieve_hygiene_sqs_messages, retrieve_hygiene_sqs_status = aws_object.retrieveBunchOfMessages(
        Config.DATA_HYGIENE_QUEUE_NAME)
    for_dump_list = []
    valid_info = []
    email_append_list = []
    unknown_email_list = []
    if len(retrieve_hygiene_sqs_messages) == 0:
        return SQSConstants.EMPTYQUEUEMESSAGE, True
    logger.info("started processing queue")
    for count, message in enumerate(retrieve_hygiene_sqs_messages):
        message_body = json.loads(message.body)
        logger.debug({"message": message_body})
        record_id = list(message_body.keys())[0]
        values_present = list(message_body.values())[0]
        email = values_present['email']
        verifier_response, verifier_status = bulkVerifier(email)
        logger.debug({"bulk_email_checker": verifier_response})
        if not verifier_status or verifier_response.get('error'):
            deleted_message, deleted_status = aws_object.deleteMessages(retrieve_hygiene_sqs_messages[:count])
            sleep(SleepingTime.BULKEMAILCHECKERERRORSLEEP)
            return deleted_message, deleted_status
        elif verifier_response.get('emailSuggested'):
            logger.info("In email suggestion")
            email = verifier_response['emailSuggested']
            verifier_response, verifier_status = bulkVerifier(email)
            logger.debug({"bulk_email_checker": verifier_response})
        if verifier_status:
            logger.info("Verifier status is true")
            values_present['email'] = verifier_response['email']
        if verifier_response['status'] == "failed":
            logger.debug({"email_status": verifier_response['status']})
            values_present['email_status'] = EmailStatus.INVALIDEMAILSTATUS
            if values_present.get('email_source_code') == DataSourceCode.DATAZAPP:
                logger.info("Push to valid_info and for_dump_list")
                valid_info.append({record_id: values_present})
                for_dump_list.append({record_id: values_present})
                continue
            else:
                email_append_list.append({record_id: values_present})
                logger.info("Push to email_append_list")
                continue
        elif verifier_response.get('status') == "passed":
            values_present['email_status'] = EmailStatus.VALIDEMAILSTATUS
        elif verifier_response.get('event') == "is_catchall":
            values_present['email_status'] = EmailStatus.CATCHALL
        elif verifier_response.get('status') == "unknown":
            values_present['email_status'] = EmailStatus.UNKNOWNEMAILSTATUS
            values_present['unknown_count'] = values_present.get('unknown_count') + 1 \
                if values_present.get('unknown_count') else 1
            logger.debug({"email_status": values_present['email_status']})
            if values_present.get('unknown_count', 0) <= 3:
                unknown_email_list.append({record_id: values_present})
                logger.info("Push to unknown_email_list")
                continue
        valid_info.append({record_id: values_present})
        for_dump_list.append({record_id: values_present})
        logger.debug("Push to for_dump_list and valid_info queue")
    logger.info("processed from queue completely")
    logger.info(f"Length of valid_info {len(valid_info)}")
    send_to_sqs_valid_message, send_to_sqs_valid_status = aws_object.sendBunchOfMessages(
        Config.VALID_EMAIL_QUEUE_NAME, valid_info)
    send_to_sqs_email_append_message, send_to_sqs_email_append_status = aws_object.sendBunchOfMessages(
        Config.DATA_APPEND_QUEUE_NAME, email_append_list)
    logger.info(f"Length of email_append_list {len(email_append_list)}")
    send_to_sqs_dump_message, send_to_sqs_dump_status = aws_object.sendBunchOfMessages(
        Config.DUMP_LIST_UPDATION_QUEUE_NAME, for_dump_list)
    send_to_sqs_hygiene_message, send_to_sqs_hygiene_status = aws_object.sendBunchOfMessages(
        Config.DATA_HYGIENE_QUEUE_NAME, unknown_email_list)
    logger.info(f"Push to unknown_email_list {len(unknown_email_list)}")
    logger.info(f"Push to for_dump_list {len(for_dump_list)}")
    if send_to_sqs_valid_status and send_to_sqs_dump_status and send_to_sqs_email_append_status and \
            send_to_sqs_hygiene_status:
        deleted_message, deleted_status = aws_object.deleteMessages(retrieve_hygiene_sqs_messages)
        return deleted_message, deleted_status
    else:
        return "failed", False


if __name__ == "__main__":
    while True:
        email_verifier_message, email_verifier_status = emailVerifier()
        if email_verifier_message == SQSConstants.EMPTYQUEUEMESSAGE:
            logger.info("Sleeping")
            sleep(SleepingTime.QUEUECHECKERTIME)
        elif not email_verifier_status:
            logger.info(email_verifier_message)
            break


