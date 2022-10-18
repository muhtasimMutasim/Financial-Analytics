import json
import datetime
import logging
import asyncio

from typing import Dict, List, Optional
from pydantic import ValidationError, validator

from models.current_price_model import TickerHistoryModel

######## Import Local Models  ########



########## Logging Information  ##########
_logger_name_ = 'stock-client-api-utils'
_logger_level_ = logging.INFO
try:
    _logger_file_path = f'logs/{_logger_name_}_logs.log'
    _logger = logging.getLogger(_logger_name_)
    handler = logging.FileHandler(_logger_file_path)
    # handler = logging.FileHandler(_logger_file_path, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    _logger.setLevel(_logger_level_)
    _logger.addHandler(handler)

except:
    __logger_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=_logger_level_, format=__logger_format)
    _logger = logging.getLogger(__name__)
    _logger.setLevel(_logger_level_)



# async def create_new 

# async def get_




