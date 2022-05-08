from datetime import timedelta
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret"
    DB_URI = "mongodb+srv://root:root@cluster0.n6gtz.mongodb.net/flasktemplate?retryWrites=true&w=majority"
    JWT_SECRET_KEY = 'secret'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = timedelta(days=1)
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True