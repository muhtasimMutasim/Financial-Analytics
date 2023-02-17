import logging
import os
import sys

from dotenv import load_dotenv; 
load_dotenv()


########## Logging Information  ##########
_MAIN_LOGGER_NAME = 'stock-client-api'
_MAIN_LOGGER_LEVEL = logging.INFO

def init_app_logger(
      logger_name:str = _MAIN_LOGGER_NAME,
      file_name:str = None,
      debug:str = False    
    ):
    """ Main logging function. """

    _logger = logging.getLogger(logger_name)
    _logger.setLevel(_MAIN_LOGGER_LEVEL if not debug else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if not file_name:
      _logger_file_path = f'logs/{logger_name}_logs.log'
    else:
       _logger_file_path = f'logs/{file_name}_logs.log'

    _stream = logging.StreamHandler(sys.stdout)
    _stream.formatter(formatter)

    handler = logging.FileHandler(_logger_file_path)
    handler.setFormatter(formatter)
    
    _logger.addHandler(handler)


def get_logger(module_name):
    return logging.getLogger(_MAIN_LOGGER_NAME).getChild(module_name)




def _init_logger(log:str=None, file_name:str=None, level=logging.INFO):
    # Exit code if parent logger name for identifying project doesn't exist.
    if not os.environ['PARENT_LOGGER'] or len(os.environ['PARENT_LOGGER']) <= 0:
        print("\n\n\nNeed to set Parent logger name!\n\nExiting.\n")
        exit(1)

    # Default Logger information
    if log == None:
      log = os.environ['PARENT_LOGGER']
    if file_name == None:
      file_name = 'error_logs'

    log_dir = "logs"
    if not os.path.exists(log_dir):
        print("\n\n'logs' directory does not exist.\n\n")
        os.makedirs(log_dir)

    # if log == None: 
    #   logger = logging.getLogger(parent_logger_name)
    # else:
    logger = logging.getLogger(log)

    handler = logging.FileHandler(log_dir +'/'+file_name+'.log')

    logger.setLevel(level)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger, log


def _module_logger_init(logger_name:str):
    # logger_name = 'utils'
    logger_name = os.environ['PARENT_LOGGER'] + '.' + logger_name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    return logger_name


