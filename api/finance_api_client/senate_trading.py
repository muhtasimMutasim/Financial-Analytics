### Built in libraries
import logging
import asyncio
import json

### 3rd party libraries
from dotenv import load_dotenv; load_dotenv()
from typing import Optional, Dict
from pydantic import ValidationError
from requests import Request, Response, Session

### Local Libraries
# from ..

"""
Four committees:

    - Homeland Security Committee (Senate)
    - Energy and Commerce Committee (House)
    - Transportation and Infrastructure Committee (House)
    - Natural Resources Committee (House)

-------------Logic-----------------
1. get all government officials on each committe.

"""

_logger = get_logger(module_name="sec-api")


class SECUrls:

    # https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent
    # https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=&owner=include&count=100&action=getcurrent
    BASE_URL = "https://www.sec.gov/"
    CGI_BIN_URL = BASE_URL + "cgi-bin/"
    # edgar_url = cgi_bin_url + "browse-edgar"
    



class SECApi:

    user_agent_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    headers = {"Accept": "application/json", "Content-Type": "application/json" }
    
    ### Initialize Session  ######
    _session = Session()
    
    ######  Asyncio Event Loop  ######
    # _loop = asyncio.get_event_loop()

    # def __del__(cls):
    #     """
    #     A destructor is provided to ensure that the client and the event loop are closed at exit.
    #     """
    #     cls.loop.close()

    @classmethod
    def url_from_endpoint(cls, endpoint: str=None, _base_url:str=None) -> str:
        if _base_url == None: _base_url = cls._base_url_
        url = _base_url if _base_url.endswith("/") else _base_url + "/"
        return f"{url}{endpoint.strip()}"
    
    @classmethod
    async def _process_response( cls,
        response: Response=None,
        raise_error:bool=True
    ) -> Response:
        """
        Return the response if it has a correct status code
        otherwise it raise an Exception.
        """
        if response.status_code > 299:
            error = Request.HTTPError(response)
            _logger.error(error)
            if raise_error:
                raise error

        return response

    @classmethod
    async def _get_request(cls, 
            base_url:str=None,
            endpoint: str = None,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
    ) -> Response:
        """  Function for GET call. """
        
        headers = cls.user_agent_headers if headers is None else headers
        url = cls.url_from_endpoint(_base_url=base_url, endpoint=endpoint)
        
        ### Currently implementing sessions instead of requests.
        response = cls._session.get(
            url=url,
            headers=headers,
            params=params        
        )
        return response

    @classmethod
    async def _parse_model(cls,
            response: Response,
            model
    ):
        """ Parse Responses with Models. """
        try:
            return model(**response.json())
        except ValidationError as vr:
            _mess = f"\nData was not parsed correctly with model, check data:\n{vr}\n"
            _logger.error(_mess)

    @classmethod
    async def _get_sec_filings(cls,
            company:str = '',
            cik:str = '',
            type:str = '',
            owner:str = '',
            include:str = '',
            count:str = 100,
            action:str = 'getcurrent',
                                           
    ) -> Response:
        """
            Function will return SEC fillings from the 
            SEC's EDGAR service. By Default it gets the latest.
        """
        # https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=&owner=include&count=100&action=getcurrent

        endpoint = "browse-edgar"
        params = {
            'company': company,
            'CIK': cik,
            'type': type,
            'owner': owner,
            'include': include,
            'count': count,
            'action': action,
        }
        headers = {"Accept": "application/json", "Content-Type": "text/html" }
        resp: (Response) = await cls._get_request(
            base_url = SECUrls.CGI_BIN_URL,
            endpoint = endpoint,
            params=params,
            headers=headers
        )
        resp = await cls._process_response(response=resp)
        return resp


    @classmethod
    async def _scrape_sec_filings_search_results(cls):
        """ Function will be scraping the SEC fillings page. """

        sec_search_results = await cls._get_sec_filings()
        results = sec_search_results.content
        print(json.dumps(results, indent=4))



def test():
    
    asyncio.run(
        SECApi._scrape_sec_filings_search_results()
    )




if __name__ == "__main__":
    test()