import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DB_HOST_MAIN = os.environ.get('DB_HOST_MAIN')
    DB_USER_MAIN = os.environ.get('DB_USER_MAIN')
    DB_PASSWORD_MAIN = os.environ.get('DB_PASSWORD_MAIN')
    DB_NAME_MAIN = os.environ.get('DB_NAME_MAIN')

    DB_NAME_CLIENT_DATA = os.environ.get('DB_NAME_CLIENT_DATA')

    DB_HOST_PIXL3 = os.environ.get('DB_HOST_PIXL3')
    DB_USER_PIXL3 = os.environ.get('DB_USER_PIXL3')
    DB_PASSWORD_PIXL3 = os.environ.get('DB_PASSWORD_PIXL3')
    DB_NAME_PIXL3 = os.environ.get('DB_NAME_PIXL3')

    DEBUG = os.environ.get('DEBUG')
    PORT = os.environ.get('PORT')

    SMARTPIXL_DATA_TABLE_NAME = os.environ.get('SMARTPIXL_DATA_TABLE_NAME')
    SMARTPIXL_PARAMS_TABLE_NAME = os.environ.get('SMARTPIXL_PARAMS_TABLE_NAME')
    EMAIL_LIST_TABLE_NAME = os.environ.get('EMAIL_LIST_TABLE_NAME')

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SMARTPIXL_BASE_URL = os.environ.get('SMARTPIXL_BASE_URL')
    SMARTPIXL_TOKEN = os.environ.get('SMARTPIXL_TOKEN')

    BASE_URL_BULK_VERIFIER = os.environ.get('BASE_URL_BULK_VERIFIER')
    BULK_EMAIL_VERIFIER_API_KEY = os.environ.get('BULK_EMAIL_VERIFIER_API_KEY')

    BASE_URL_DATAZAPP = os.environ.get('BASE_URL_DATAZAPP')
    DATAZAPP_API_KEY = os.environ.get('DATAZAPP_API_KEY')
    # MONGO_DATABASE_URI = os.environ.get('MONGO_DATABASE_URL') or "mongodb://localhost:27017"
    # MONGO_DATABASE_NAME = os.environ.get('MONGO_DATABASE_NAME') or "smartpixl_output"

    DATA_HYGIENE_QUEUE_NAME = os.environ.get('DATA_HYGIENE_QUEUE_NAME')
    DATA_APPEND_QUEUE_NAME = os.environ.get('DATA_APPEND_QUEUE_NAME')
    VALID_EMAIL_QUEUE_NAME = os.environ.get('VALID_EMAIL_QUEUE_NAME')
    PREVIOUS_DATA_QUEUE_NAME = os.environ.get('PREVIOUS_DATA_QUEUE_NAME')
    DUMP_LIST_UPDATION_QUEUE_NAME = os.environ.get('DUMP_LIST_UPDATION_QUEUE_NAME')
    UNKNOWN_EMAIL_QUEUE_NAME = os.environ.get('UNKNOWN_EMAIL_QUEUE_NAME')

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')

    # BASE_URL_DATAFINDER_APPEND = os.environ.get('BASE_URL_DATAFINDER_APPEND')
    # DATAFINDER_APPEND_API_KEY = os.environ.get('DATAFINDER_APPEND_API_KEY')