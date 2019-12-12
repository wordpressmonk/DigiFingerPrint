# ~/app/services/smartpixl.py
import requests
import xmltodict
import json
from app.config import Config
from app.constants import SmartPixlCons
import mysql.connector


class SmartPixl(object):

    def getSmartPixlParams(self):
        try:
            mydb = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN,
                                           passwd=Config.DB_PASSWORD_MAIN,
                                           database=Config.DB_NAME_MAIN)
            mycursor = mydb.cursor(buffered=True)
            sql = f"SELECT * FROM {Config.SMARTPIXL_PARAMS_TABLE_NAME}"
            mycursor.execute(sql)
            smartpixl_params = [{'companyId': record[1], 'pixlId': record[2], 'domain': record[3], 'start': record[4]}
                                for record in mycursor.fetchall()]
            return smartpixl_params, True
        except Exception as e:
            return f"getSmartPixlParamERROR: {e}", False

    def updateSmartPixlParams(self, company_id, pixl_id, previous, start):
        try:
            mydb = mysql.connector.connect(host=Config.DB_HOST_MAIN, user=Config.DB_USER_MAIN,
                                           passwd=Config.DB_PASSWORD_MAIN,
                                           database=Config.DB_NAME_MAIN)
            mycursor = mydb.cursor(buffered=True)
            sql = f"UPDATE {Config.SMARTPIXL_PARAMS_TABLE_NAME} SET start = '{start}' , previous_run = '{previous}' " \
                  f"WHERE companyId = {company_id} AND pixlId = {pixl_id}"
            mycursor.execute(sql)
            mydb.commit()
            return "success", True
        except Exception as e:
            return f"getSmartPixlCronTimeUpdationERROR: {e}", False

    def smartPixlAPI(self, company_id, pixl_id, start, end, ckey=SmartPixlCons.CKEY):
        try:
            response = requests.request("GET", url=Config.SMARTPIXL_BASE_URL,
                                        params={'CompanyId': company_id, 'PiXLId': pixl_id, 'Startdate': start,
                                                'Enddate': end, 'UserTokenID': Config.SMARTPIXL_TOKEN, 'CKey': ckey})
            return response, True
        except Exception as e:
            return str(e), False

    def xmlToDict(self, response):
        try:
            json_response = json.dumps(xmltodict.parse(response.text))
            json_data = json.loads(json_response)['ArrayOfSmartPiXLAPIModel']['SmartPiXLAPIModel']
            return json_data, True
        except Exception as e:
            return "No data", False
