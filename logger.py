import logging
import settings


#config the logging: set the path and formatter
log_level = logging.INFO if settings.DEBUG else logging.WARNING
logging.basicConfig(level = log_level)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(settings.LOG_PATH)
handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def v(msg):
	'''log verbose message'''
	logger.info(msg)


def d(msg):
	'''log debug message'''
	logger.debug(msg)


def w(msg):
	'''log warning message'''
	logger.warning(msg) 


def e(msg):
	'''log error message'''
	logger.error(msg) 
