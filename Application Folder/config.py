# config.py

#List of all Flask Config Variables -
#http://flask.pocoo.org/docs/0.11/config/

#List of all SQLAlchemy Configuration Variables -
#http://flask-sqlalchemy.pocoo.org/2.1/config/



#Set Environment Variable - Development, Testing, Production
ENVIRONMENT = "Development"


class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    FLASK_DEBUG = 1
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False
    
    #Set following two settings to True if you are using HTTPS
    SESSION_COOKIE_SECURE = False         
    REMEMBER_COOKIE_SECURE = False


    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True


# Return the config to the application based on the ENVIRONMENT variable
def get_app_config():

	if ENVIRONMENT == "Development":
		return DevelopmentConfig

	elif ENVIRONMENT == "Testing":
		return TestingConfig

	elif ENVIRONMENT == "Production":
		return ProductionConfig

	else:
		return Config


