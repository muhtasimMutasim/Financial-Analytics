import traceback
import json
import os
import sys
import logging
import asyncio

from custom_logger import _module_logger_init as _init_logger

from requests import Response
import aiohttp
# from aiohttp import
from typing import Dict, List, Optional
from pydantic import ValidationError




__logger_name = _init_logger(logger_name="stock-api-client")
_logger = logging.getLogger(__logger_name)




class StockAPIClientBase:

    def __init__(self):
        self._base_url_ = 'https://query2.finance.yahoo.com'
        self._scrape_url_ = 'https://finance.yahoo.com/quote'
        # self._root_url_ = 'https://finance.yahoo.com'
        
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


    async def _post_req(self, endpoint:str, data:str, 
        headers: Optional[Dict] = None):
        # No use for post requests as of now.
        """  Function for POST call. """
        pass


    async def _get_req(self, endpoint: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        url:str=None,
        only_text:bool=False):
        """  Function for GET call. """
        try:
            headers = self.user_agent_headers if headers is None else headers
            url = self.url_from_endpoint(_base_url=url, endpoint=endpoint)
            
            async with self._client_session.get(url=url, headers=headers, params=params) as resp:
                await self._process_response(response=resp)
                if only_text:
                    return await resp.text()
                return await resp.json()


        except Exception as exc:
            _type, value, _traceback = sys.exc_info()
            logging.error(traceback.format_exc())
            _error_mess = f"\nError: {_type}  Value:{value}\n{_traceback}\n"
            print(_error_mess)
            print(traceback.print_exc())
    
    

    def _get_single_ticker_json_data( self,
        endpoint:str=None,
        params: Optional[Dict] = None,
    ):
        """ Make request to get Stock ticker. """
        return self.loop.run_until_complete(
                self._get_req(endpoint=endpoint, params=params)
        )



    def _search_ticker( self, ticker:str=None):
        """ Search Stock ticker and get response with 
            relevant info response. """
        endpoint = "/v1/finance/search"
        params = { "q": ticker.strip() }
        return self._get_single_ticker_json_data(
               endpoint=endpoint, params=params )

    

    def _get_multiple_tickers_json_data(
        self,
        tickers:List[str]=[]
    ):
        """ Function for getting multiple tickers. """


    def _get_ticker_quote(self, ticker:str):
        """ Gets ticker quote. """







