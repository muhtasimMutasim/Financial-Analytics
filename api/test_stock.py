import logging
import json
import os
import sys
from dotenv import load_dotenv;
from custom_logger import _init_logger
from finance_api_client import StockAPIClientBase


load_dotenv(dotenv_path="../.env")
os.environ['PARENT_LOGGER'] = 'stock_async_api'

__default_logger, __default_logger_name = _init_logger()
_logger = logging.getLogger(__default_logger_name)
_logger.info('App started in %s', os.getcwd())



def test():

    ticker = "TSLA"
    api = StockAPIClientBase()
    # stock = api._search_ticker(ticker="TSLA")
    # stock = api._get_statistics(ticker=ticker)
    # print(f"\n\n\n{json.dumps(stock, indent=4)}\n\n\n")
    current_price = api._get_current_price(ticker=ticker)
    print(f"\n\n\n{json.dumps(current_price, indent=4)}\n\n\n")



def main():
    """ Main function. """
    test()


if __name__ == "__main__":
    main()