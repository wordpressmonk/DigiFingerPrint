# ~/app/models/users.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash





# id
# smartpixl_recordId = record['smartpixl_recordId']
# company_Id = record['company_Id']
# first_name = record['first_name']
# last_name = record['last_name']
# email = record['email']
# email_status = record['email_status']
# email_source = record['email_source']
# # smartpixl_data = record['smartpixl_data']
# sql = "INSERT INTO customers (smartpixl_recordId, companyId, first_name, last_name, email, email_status, email_source, smartpixl_data)

class Users:
    pass

# failed_process = []
# invalid_emails = []
# unknown_emails = []
# valid_email_list = []
# for records in email_hygiene_list:
#     count += 1
#     print(count)
#     record_id = list(records.keys())[0]
#     email = list(records.values())[0]['email']
#     print(email)
#     response = requests.request("GET", url=Config.BASE_URL_BULK_VERIFIER,params={"key": Config.BULK_EMAIL_VERIFIER_API_KEY, "email": email})
#     try:
#         response_data = response.json()
#         if response_data['status'] == "passed":
#             records['email'] = response_data['email']
#             records['email_status'] = 'valid'
#             records['email_source'] = 'smartpixl'
#             valid_email_list.append(records)
#         elif response_data['status'] == "failed":
#             invalid_emails.append(record_id)
#         elif response_data['status'] == "unknown":
#             unknown_emails.append(record_id)
#     except:
#         failed_process.append(record_id)

count = 0
exception = []
valid_email_list = []
not_valid_email_list = []
not_a_list_of_data = []

# for message in input_datas:
#     count += 1
#     if count>230:
#         print(count)
#         record_id = list(message.keys())[0]
#         values_present = list(message.values())[0]
#         company_id = values_present['companyId']
#         params = values_present['params']
#         params['service'] = 'email'
#         params['k2'] = Config.DATAFINDER_APPEND_API_KEY
#         params['dcfg_emailinvalid'] = 1
#         try:
#             start_time = time.time()
#             response = requests.request("GET", url=Config.BASE_URL_DATAFINDER_APPEND, headers={}, params=params)
#             end_time = time.time()
#             print(end_time-start_time)
#             json_response = response.json().get('datafinder', {})
#             email_append_api_data = json_response.get('results', [])
#             email_append_api_message = True
#         except Exception as e:
#             email_append_api_message = False
#         if not email_append_api_message:
#             exception.append(message)
#         elif type(email_append_api_data) == list and len(email_append_api_data)>0:
#             if email_append_api_data[0].get('EmailAddr') and email_append_api_data[0].get('EmailAddrUsable') == "YES":
#                 values_present['email'] = email_append_api_data[0]['EmailAddr']
#                 values_present['email_status'] = 'valid'
#                 values_present['email_source'] = 'datafinder'
#                 valid_email_list.append({record_id: values_present})
#             else:
#                 not_valid_email_list.append(message)
#         else:
#             not_a_list_of_data.append(message)



#email verifier

# valid_info = []
# email_append_list = []
# exception = []
#
# retrieve_hygiene_sqs_messages, retrieve_hygiene_sqs_status = aws_object.retrieveBunchOfMessages(Config.DATA_HYGIENE_QUEUE_NAME)
# for message in retrieve_hygiene_sqs_messages:
#     entry = {}
#     message_body = json.loads(message.body)
#     record_id = list(message_body.keys())[0]
#     values_present = list(message_body.values())[0]
#     company_id = values_present['companyId']
#     email = values_present['email']
#     try:
#         response = requests.request("GET", url=Config.BASE_URL_BULK_VERIFIER, params={"key": Config.BULK_EMAIL_VERIFIER_API_KEY, "email": email})
#         verifier_response = response.json()
#         verifier_status = True
#     except Exception as e:
#         exception.append(message.body)
#         print(str(e))
#         verifier_status = False
#     if verifier_status and verifier_response.get('emailSuggested'):
#         email = verifier_response['emailSuggested']
#         verifier_response, verifier_status = bulkVerifier(email)
#     if verifier_status and verifier_response['status'] == "passed":
#         values_present['email'] = verifier_response['email']
#         values_present['email_status'] = 'valid'
#         values_present['email_source'] = 'smartpixl'
#         valid_info.append({record_id: values_present})
#         message.delete()
#     elif verifier_status and verifier_response['status'] == "failed":
#         email_append_list.append({record_id: message_body})
#         message.delete()
#     elif verifier_status and verifier_response['status'] == "unknown":
#         email_append_list.append({record_id: message_body})
#         message.delete()
#         print("unknown")
#         # unknown need to be deleted or not
# if valid_info:
#     send_to_sqs_valid_message, send_to_sqs_valid_status = aws_object.sendBunchOfMessages(Config.VALID_EMAIL_QUEUE_NAME, valid_info)
# if email_append_list:
#     send_to_sqs_email_append_message, send_to_sqs_email_append_status = aws_object.sendBunchOfMessages(Config.DATA_APPEND_QUEUE_NAME, email_append_list)