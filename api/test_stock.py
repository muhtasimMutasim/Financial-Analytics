
######  Standard Libraries ######
import logging
import json
import os
import sys
import asyncio


######  3rd party libraries  ######
from dotenv import load_dotenv;


######  Local Libraries.  ######
from finance_api_client import StockAPIClientBase


load_dotenv(dotenv_path="../.env")


########## Logging Information  ##########
_logger_name_ = 'stock-client-api-test'
_logger_level_ = logging.INFO
try:
    _logger_file_path = f'logs/{_logger_name_}_logs.log'
    _logger = logging.getLogger(_logger_name_)
    # handler = logging.FileHandler(_logger_file_path)
    handler = logging.FileHandler(_logger_file_path, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    _logger.setLevel(_logger_level_)
    _logger.addHandler(handler)

except:
    __logger_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=_logger_level_, format=__logger_format)
    _logger = logging.getLogger(__name__)
    _logger.setLevel(_logger_level_)



def test():

    ticker = "TSLA"
    # api = StockAPIClientBase()

    # stock = api._search_ticker(ticker="TSLA")
    # stock = api._get_statistics(ticker=ticker)
    # print(f"\n\n\n{json.dumps(stock, indent=4)}\n\n\n")
    # current_price = await api._get_current_price(ticker=ticker)
    # print(f"\n\n\n{json.dumps(current_price, indent=4)}\n\n\n")
    # print(  f"\n\n{ json.dumps(current_price.dict(), indent=4, default=str)   }\n\n"  )
    
    price = StockAPIClientBase(ticker=ticker).current_price
    print(f"\n\nCurrent Price:   {price} \n\n")



def main():
    """ Main function. """
    test()


if __name__ == "__main__":
    main()