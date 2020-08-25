

class Config(object):
    DATABASE_URL='postgresql://postgres:password@postgres:5432/parsing_websites'
    CELERY_BROKER_URL='redis://redis:6379/0'
    CELERY_RESULT_BACKEND='redis://redis:6379/0'
    POSTGRES_USER='postgres'
    POSTGRES_PASSWORD='password'
    POSTGRES_DB='parsing_websites'
    SECRET_KEY = b'very_secret_key'

