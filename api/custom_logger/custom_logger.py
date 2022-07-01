import logging
import os

from dotenv import load_dotenv; 
load_dotenv()

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

# __default_logger, __default_logger_name = _init_logger()
# _logger = logging.getLogger(__default_logger_name)
# _logger.info('App started in %s', os.getcwd())


def _module_logger_init(logger_name:str):
    # logger_name = 'utils'
    logger_name = os.environ['PARENT_LOGGER'] + '.' + logger_name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    return logger_name


