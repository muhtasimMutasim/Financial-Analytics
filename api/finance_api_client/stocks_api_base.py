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

from .api_parser import TickerResponseParser


__logger_name = _init_logger(logger_name="stock-api-client")
_logger = logging.getLogger(__logger_name)




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


    async def _post_req(self, endpoint:str, data:str, 
        headers: Optional[Dict] = None):
        # No use for post requests as of now.
        """  Function for POST call. """
        pass


    async def _get_req(self, endpoint: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        base_url:str=None,
        only_text:bool=False):
        """  Function for GET call. """
        try:
            headers = self.user_agent_headers if headers is None else headers
            url = self.url_from_endpoint(_base_url=base_url, endpoint=endpoint)
            
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
    

    async def _get_ticker_statistics_html(self, ticker:str):
        """ Gets ticker quote. """
        base_url = self._root_url_
        endpoint = "/quote/"+ticker
        html_data = await self._get_req(
            base_url=base_url, endpoint=endpoint, only_text=True)
        return html_data
    

    async def _get_ticker_statistics_json_data(self, ticker:str):
        """ Gets ticker quote. """
        
        html_data = await self._get_ticker_quote_html(ticker=ticker)

        if "QuoteSummaryStore" not in html_data:
            html_data = await self._get_ticker_quote_html(ticker=ticker)
            if "QuoteSummaryStore" not in html_data:
                return {}

        data = TickerResponseParser.get_json(html=html_data)
        return data
        
    

    def _get_history(self, period="1mo", interval="1d",
                start=None, end=None, prepost=False, actions=True,
                auto_adjust=True, back_adjust=False,
                proxy=None, rounding=False, tz=None, timeout=None, **kwargs):

        if start or period is None or period.lower() == "max":
            if end is None:
                end = int(_time.time())
            elif isinstance(end, _datetime.datetime):
                end = int(_time.mktime(end.timetuple()))
            else:
                end = int(_time.mktime(_time.strptime(str(end), '%Y-%m-%d'))) 
            if start is None:
                if interval=="1m":
                    start = end - 604800 # Subtract 7 days 
                else:
                    start = -631159200
            elif isinstance(start, _datetime.datetime):
                start = int(_time.mktime(start.timetuple()))
            else:
                start = int(_time.mktime(
                    _time.strptime(str(start), '%Y-%m-%d')))
            params = {"period1": start, "period2": end}
        else:
            period = period.lower()
            params = {"range": period}

        params["interval"] = interval.lower()
        params["includePrePost"] = prepost
        params["events"] = "div,splits"

        # 1) fix weired bug with Yahoo! - returning 60m for 30m bars
        if params["interval"] == "30m":
            params["interval"] = "15m"

        # setup proxy in requests format
        if proxy is not None:
            if isinstance(proxy, dict) and "https" in proxy:
                proxy = proxy["https"]
            proxy = {"https": proxy}

        # Getting data from json
        url = "{}/v8/finance/chart/{}".format(self._base_url, self.ticker)

        data = None

        try:
            data = session.get(
                url=url,
                params=params,
                proxies=proxy,
                headers=utils.user_agent_headers,
                timeout=timeout
            )
            if "Will be right back" in data.text or data is None:
                raise RuntimeError("*** YAHOO! FINANCE IS CURRENTLY DOWN! ***\n"
                                   "Our engineers are working quickly to resolve "
                                   "the issue. Thank you for your patience.")

            data = data.json()
        except Exception:
            pass

        # Work with errors
        debug_mode = True
        if "debug" in kwargs and isinstance(kwargs["debug"], bool):
            debug_mode = kwargs["debug"]


    def _get_single_ticker_json_data( self,
        endpoint:str=None,
        params: Optional[Dict] = None,
    ):
        """ Make request to get Stock ticker. """
        return self.loop.run_until_complete(
                self._get_req(endpoint=endpoint, params=params)
        )


    def _get_statistics( self, ticker:str=None):
        """ Search Stock ticker and get response with 
            relevant info response. """
        return self.loop.run_until_complete(
               self._get_ticker_quote_json_data(ticker=ticker))
        

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








