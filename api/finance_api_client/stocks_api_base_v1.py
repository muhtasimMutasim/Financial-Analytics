import traceback
import json
import os
import time
import datetime
import sys
import logging
import asyncio

from requests import Response
import aiohttp
from typing import Dict, List, Optional
from pydantic import ValidationError, validator

from .api_parser import TickerResponseParser

######## Import Models  ########
from models.current_price_model import *



########## Logging Information  ##########
_logger_name_ = 'stock-client-api'
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



class StockAPIClientBase:

    def __init__(self):
        self._base_url_ = 'https://query2.finance.yahoo.com'
        # self._scrape_url_ = 'https://finance.yahoo.com/quote'
        self._root_url_ = 'https://finance.yahoo.com'
        
        self.user_agent_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.headers = {"Accept": "application/json", "Content-Type": "application/json" }
        
        self._client_session = aiohttp.ClientSession(raise_for_status=True)
        self.loop = asyncio.get_event_loop()

    async def _close_client(self):
        return await self._client_session.close()


    def __del__(self):
        """
        A destructor is provided to ensure that the client and the event loop are closed at exit.
        """
        # Use the loop to call async close, then stop/close loop.
        self.loop.run_until_complete(self._close_client())
        self.loop.close()


    def url_from_endpoint(self, endpoint: str=None, _base_url:str=None) -> str:
        if _base_url == None: _base_url = self._base_url_
        url = _base_url if _base_url.endswith("/") else _base_url + "/"
        return f"{url}{endpoint.strip()}"
    

    async def _process_response( self,
        response: Response=None,
        raise_error:bool=True
    ):
        """
        Return the response if it has a correct status code
        otherwise it raise an Exception.
        """
        if response.status > 299:
            error = await aiohttp.ClientError(response)
            _logger.error(error)
            if raise_error:
                raise error
        return response


    async def _post_req(self, 
            endpoint:str,
            data:str, 
            headers: Optional[Dict] = None
    ):
        # No use for post requests as of now.
        """  Function for POST call. """
        pass


    async def _get_request_v1(self, endpoint: str,
            base_url:str=None,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
    ):
        """  Function for GET call. """
        
        headers = self.user_agent_headers if headers is None else headers
        url = self.url_from_endpoint(_base_url=base_url, endpoint=endpoint)
        
        async with self._client_session.get(url=url, headers=headers, params=params) as resp:
            # await self._process_response(response=resp)
            return await resp

    
    async def _parse_model(self,
            response: Response,
            model
    ):
        """ Parse Responses with Models. """
        try:
            return model(**response.json())
        except ValidationError as vr:
            _mess = f"\nData was not parsed correctly with model, check data:\n{vr}\n"


    async def _get_ticker_statistics_html(self, ticker:str):
        """ Gets ticker quote. """
        base_url = self._root_url_
        endpoint = "/quote/"+ticker
        html_data = await self._get_request(
            base_url=base_url, endpoint=endpoint)
        html_data = html_data.text()
        return html_data
    

    async def _get_ticker_statistics_json_data(self, ticker:str):
        """ Gets ticker quote. """
        
        html_data = await self._get_ticker_statistics_html(ticker=ticker)

        if "QuoteSummaryStore" not in html_data:
            html_data = await self._get_ticker_statistics_html(ticker=ticker)
            if "QuoteSummaryStore" not in html_data:
                return {}
        data = TickerResponseParser.get_json(html=html_data)
        return data
        

    async def _get_history(self, 
            ticker:str=None, period="1mo", interval="1d",
            start=None, end=None, prepost=False, actions=True,
            auto_adjust=True, back_adjust=False,
            proxy=None, rounding=False, 
            tz=None, timeout=None, **kwargs
    ):
        """ Function to get stock history """
        if start or period is None or period.lower() == "max":
            if end is None:
                end = int(time.time())
            elif isinstance(end, datetime.datetime):
                end = int(time.mktime(end.timetuple()))
            else:
                end = int(time.mktime(time.strptime(str(end), '%Y-%m-%d'))) 
            if start is None:
                if interval=="1m":
                    start = end - 604800 # Subtract 7 days 
                else:
                    start = -631159200
            elif isinstance(start, datetime.datetime):
                start = int(time.mktime(start.timetuple()))
            else:
                start = int(time.mktime(
                    time.strptime(str(start), '%Y-%m-%d')))
            params = {"period1": start, "period2": end}
        else:
            period = period.lower()
            params = {"range": period}

        params["interval"] = interval.lower()
        params["includePrePost"] = str(prepost).lower()
        params["events"] = "div,splits"

        # 1) fix weired bug with Yahoo! - returning 60m for 30m bars
        if params["interval"] == "30m":
            params["interval"] = "15m"

        try:
            endpoint = "/v8/finance/chart/"+ticker
            data = await self._get_request(endpoint=endpoint, params=params)
            data_str = json.dumps(data)

            if "Will be right back" in data_str or data_str is None:
                raise RuntimeError("*** YAHOO! FINANCE IS CURRENTLY DOWN! ***\n"
                                   "Our engineers are working quickly to resolve "
                                   "the issue. Thank you for your patience.")
            return data

        except Exception as exc:
            _type, value, _traceback = sys.exc_info()
            logging.error(traceback.format_exc())
            _error_mess = f"\nError: {_type}  Value:{value}\n{_traceback}\n"
            print(_error_mess)
            print(traceback.print_exc())
            pass


    def _get_single_ticker_json_data( self,
        endpoint:str=None,
        params: Optional[Dict] = None,
    ):
        """ Make request to get Stock ticker. """
        return self.loop.run_until_complete(
                self._get_request(endpoint=endpoint, params=params)
        )


    def _get_statistics( self,
             ticker:str=None
    ):
        """ Search Stock ticker and get response with 
            relevant info response. """
        try:
            return self.loop.run_until_complete(
                self._get_ticker_statistics_html(ticker=ticker)
            )

        except Exception as exc:
            _type, value, _traceback = sys.exc_info()
            logging.error(traceback.format_exc())
            _error_mess = f"\nError: {_type}  Value:{value}\n{_traceback}\n"
            print(_error_mess)
            print(traceback.print_exc())


    async def _get_current_price( self,
            ticker:str=None, 
            period:str='2d', 
            interval:str='1m'
    ):
        """ Get current price of Stock ticker. """
        try:
            # return self.loop.run_until_complete()
            _current = await self._get_history(ticker=ticker, period=period, interval=interval)
            
        
        except Exception as exc:
            _type, value, _traceback = sys.exc_info()
            logging.error(traceback.format_exc())
            _error_mess = f"\nError: {_type}  Value:{value}\n{_traceback}\n"
            print(_error_mess)
            print(traceback.print_exc())


    def _search_ticker( self, ticker:str=None):
        """ Search Stock ticker and get response with 
            relevant info response. """
        endpoint = "/v1/finance/search"
        params = { "q": ticker.strip() }
        return self._get_single_ticker_json_data(
                    endpoint=endpoint, params=params 
            )


    def _get_multiple_tickers_json_data(
        self,
        tickers:List[str]=[]
    ):
        """ Function for getting multiple tickers. """








