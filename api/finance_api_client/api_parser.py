import logging
import json
import re

from custom_logger import _module_logger_init as _init_logger

__logger_name = _init_logger(logger_name="stock-api-client")
_logger = logging.getLogger(__logger_name)



class TickerResponseParser:
    _if_data_is_string = True

    @classmethod
    def _check_if_json(cls, data=None):
        """ Checks if data is a dictionary. """
        if data:
            data_type = type(data)
            if data_type == str:
                cls._if_data_is_string = False
                return data
            
            return json.loads(data)
    
    @classmethod
    def get_json(cls, html:str = None):
        

        json_str = html.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
        # add data about Shares Outstanding for companies' tickers if they are available
        try:
            data['annualBasicAverageShares'] = json.loads(
                json_str)['context']['dispatcher']['stores'][
                    'QuoteTimeSeriesStore']['timeSeries']['annualBasicAverageShares']
        except Exception:
            pass

        # return data
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(
            r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

        return json.loads(new_data)
