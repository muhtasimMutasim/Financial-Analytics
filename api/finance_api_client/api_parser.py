import logging
import json




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
    def get_json(html:str = None):
        
        if "QuoteSummaryStore" not in html:
            html = session.get(url=url, proxies=proxy).text
            if "QuoteSummaryStore" not in html:
                return {}

        json_str = html.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()
        data = _json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
        # add data about Shares Outstanding for companies' tickers if they are available
        try:
            data['annualBasicAverageShares'] = _json.loads(
                json_str)['context']['dispatcher']['stores'][
                    'QuoteTimeSeriesStore']['timeSeries']['annualBasicAverageShares']
        except Exception:
            pass

        # return data
        new_data = _json.dumps(data).replace('{}', 'null')
        new_data = _re.sub(
            r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

        return _json.loads(new_data)
