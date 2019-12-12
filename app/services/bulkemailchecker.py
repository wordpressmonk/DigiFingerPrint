import requests
from app.config import Config


def bulkVerifier(email):
    try:
        response = requests.request("GET", url=Config.BASE_URL_BULK_VERIFIER,
                                    params={"key": Config.BULK_EMAIL_VERIFIER_API_KEY, "email": email})
        response_data = response.json()
        # print(response_data)
        return response_data, True
    except Exception as e:
        return str(e), False
