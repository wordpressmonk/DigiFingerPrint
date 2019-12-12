# import requests
# from app.config import Config
#
#
# def emailAppendApi(params):
#     try:
#         response = requests.request("GET", url=Config.BASE_URL_DATAZAPP, params=params)
#         json_response = response.json().get('datafinder', {})
#         results = json_response.get('results', [])
#         return results, True
#     except Exception as e:
#         print(str(e))
#         return [], False
#
#
#
