import os

class Config(object):
    DEBUG = False
    TESTING = False

    AWS_ACCESS_KEY =  os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    NG_ENDPOINT = ''

    VIDEO_UPLOADS = 'app/static/uploads'
    ALLOWED_FILE_EXTENSIONS = ['MP4']

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
 
class TestConfig(Config):
    TESTING = True

