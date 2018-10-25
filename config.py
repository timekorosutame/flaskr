
import os

class BaseConfig(object):
	"""docstring for BaseConfig"""
	DEBUG = False
	SECRET_KEY = 'DEV_KEY'
	SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']


class TestConfig(BaseConfig):
	"""docstring for TestConfig"""
	DEBUG = True
	#TESTING = True
	#WTF_CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
		
		