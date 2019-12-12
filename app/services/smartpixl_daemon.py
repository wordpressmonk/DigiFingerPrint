import sys

sys.path.append('/home/ubuntu/code/invocabo-backend/')
from app.services.smartpixl import SmartPixl
from app.config import Config
from app.constants import SleepingTime, DataSourceCode, EmailStatus
from app.services import AmazonSQS
from app.services.deduping import firstDeduping
from app.services.cpanelsql import bulkInsertSmartPixlData
import logging
import time
from datetime import datetime
from pytz import timezone
tz = timezone('EST')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('smartpixl_logs.log')
formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
smartpixl_object = SmartPixl()
aws_object = AmazonSQS()


def smartPixlProcess(end, smartpixl_client):
    data_list_to_queue = []
    smartpixl_api_response, smartpixl_api_status = smartpixl_object.smartPixlAPI(smartpixl_client['companyId'],
                                                                                 smartpixl_client['pixlId'],
                                                                                 smartpixl_client['start'], end)
    xml_to_json_message, xml_to_json_status = smartpixl_object.xmlToDict(smartpixl_api_response)
    if not xml_to_json_status:
        logger.info("XML to JSON Failed")
        return "XML to JSON Failed", False
    logger.info("Inserting data to cpanel")
    bulk_insertion_message, bulk_insertion_status = bulkInsertSmartPixlData(
        smartpixl_client['companyId'], smartpixl_client['pixlId'], xml_to_json_message)
    if not bulk_insertion_status:
        logger.info("Failed bulk data insertion")
        return "failed bulk data insertion", False
    logger.info(f"Successfully inserted {len(xml_to_json_message)}")
    deduped_data = firstDeduping(xml_to_json_message)
    logger.info(f"Deduped count {len(deduped_data[0])}")
    for key, value in deduped_data[0].items():
        to_queue = dict()
        to_queue['params'] = {'FirstName': value.get('FirstName', ''), 'LastName': value.get('LastName', ''),
                              'Address': value.get('Address'), 'Zip': value.get('ZipCode', ''),
                              'City': value.get('City', '')}
        to_queue['companyId'] = smartpixl_client['companyId']
        to_queue['pixlId'] = smartpixl_client['pixlId']
        to_queue['email'] = value.get('EMail', '')
        to_queue['email_source_code'] = DataSourceCode.SMARTPIXL if to_queue.get('email') else ''
        to_queue['smartpixl_data'] = value
        data_list_to_queue.append({key: to_queue})
    logger.info(f"Length of new data to queue {len(data_list_to_queue)}")
    sqs_data, sqs_status = aws_object.sendBunchOfMessages(Config.PREVIOUS_DATA_QUEUE_NAME, data_list_to_queue)
    return sqs_data, sqs_status


if __name__ == "__main__":
    while True:
        logger.info("started")
        end = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        get_smartpixl_params_message, get_smartpixl_params_status = smartpixl_object.getSmartPixlParams()
        for smartpixl_client in get_smartpixl_params_message:
            logger.debug({"smartpixl_client": smartpixl_client, "end": end})
            smart_message, smart_status = smartPixlProcess(end, smartpixl_client)
            logger.info(f"get_smartpixl_message {smart_message}")
            if smart_status:
                params_update_message, params_update_status = smartpixl_object.updateSmartPixlParams(
                    smartpixl_client['companyId'], smartpixl_client['pixlId'], smartpixl_client['start'], end)
                if not params_update_status:
                    logger.info("cannot update the start time")
        logger.info("sleeping")
        time.sleep(SleepingTime.SMARTPIXLTRIGGERTIME)


