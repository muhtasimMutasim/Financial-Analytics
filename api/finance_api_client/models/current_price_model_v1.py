# generated by datamodel-codegen:
#   filename:  tsla_resp.json
#   timestamp: 2022-10-18T04:31:10+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Pre(BaseModel):
    timezone: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    gmtoffset: Optional[int] = None


class Regular(BaseModel):
    timezone: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    gmtoffset: Optional[int] = None


class Post(BaseModel):
    timezone: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    gmtoffset: Optional[int] = None


class CurrentTradingPeriod(BaseModel):
    pre: Optional[Pre] = None
    regular: Optional[Regular] = None
    post: Optional[Post] = None


class TradingPeriod(BaseModel):
    timezone: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    gmtoffset: Optional[int] = None


class Meta(BaseModel):
    currency: Optional[str] = None
    symbol: Optional[str] = None
    exchangeName: Optional[str] = None
    instrumentType: Optional[str] = None
    firstTradeDate: Optional[int] = None
    regularMarketTime: Optional[int] = None
    gmtoffset: Optional[int] = None
    timezone: Optional[str] = None
    exchangeTimezoneName: Optional[str] = None
    regularMarketPrice: Optional[float] = None
    chartPreviousClose: Optional[float] = None
    previousClose: Optional[float] = None
    scale: Optional[int] = None
    priceHint: Optional[int] = None
    currentTradingPeriod: Optional[CurrentTradingPeriod] = None
    tradingPeriods: Optional[List[List[TradingPeriod]]] = None
    dataGranularity: Optional[str] = None
    range: Optional[str] = None
    validRanges: Optional[List[str]] = None


class QuoteItem(BaseModel):
    open: Optional[List[Optional[float]]] = None
    low: Optional[List[Optional[float]]] = None
    close: Optional[List[Optional[float]]] = None
    volume: Optional[List[Optional[int]]] = None
    high: Optional[List[Optional[float]]] = None


class Indicators(BaseModel):
    quote: Optional[List[QuoteItem]] = None


class ResultItem(BaseModel):
    meta: Optional[Meta] = None
    timestamp: Optional[List[int]] = None
    indicators: Optional[Indicators] = None


class Chart(BaseModel):
    result: Optional[List[ResultItem]] = None
    error: Optional[Any] = None


class Model(BaseModel):
    chart: Optional[Chart] = None
