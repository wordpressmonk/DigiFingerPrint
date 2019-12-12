import requests
import json
from app.constants import DataZappConstants
from app.config import Config


def emailAppendApi(input_data):
    try:
        payloads = {"AppendModule": DataZappConstants.APPENDMODULE, "AppendType": DataZappConstants.APPENDTYPE,
                    "DncFlag": DataZappConstants.DNCFLAG, "Apikey": Config.DATAZAPP_API_KEY, "Data": [input_data]}
        response = requests.post(Config.BASE_URL_DATAZAPP, headers={'Content-Type': 'application/json'},
                                 data=json.dumps(payloads))
        return response.json(), True
    except Exception as e:
        return str(e), False
