import json
import mysql.connector
from app.config import Config
from app.constants import DataSourceCode


def bulkInsertSmartPixlData(company_id, pixl_id, all_smartpixl_json):
    try:
        mydb = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN,
                                       passwd=Config.DB_PASSWORD_MAIN, database=Config.DB_NAME_CLIENT_DATA)
        table_name = f"{Config.SMARTPIXL_DATA_TABLE_NAME}_{pixl_id}"
        command = f"INSERT INTO {table_name}"
        mydb.autocommit = False
        mycursor = mydb.cursor(buffered=True)
        for count, record in enumerate(all_smartpixl_json):
            smartpixl_recordId = record['RecordID']
            first_name = record['FirstName']
            last_name = record['LastName']
            email = record['EMail'] if record.get('EMail') else ''
            email_source_code = DataSourceCode.SMARTPIXL if record.get('EMail') else ''
            smartpixl_data = json.dumps(record)
            sql = command + "(smartpixl_recordId, companyId, pixlId, first_name, last_name, email, email_source_code, " \
                            "smartpixl_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (smartpixl_recordId, company_id, pixl_id, first_name, last_name, email, email_source_code,
                      smartpixl_data)
            mycursor.execute(sql, values)
        mydb.commit()
        return "success", True
    except Exception as e:
        return f"bulkInsertFilteredDataERROR: {e}", False