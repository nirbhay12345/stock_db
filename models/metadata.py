from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt, PositiveFloat
from datetime import datetime

@dataclass
class StockMetaData:
    uuid: str
    currentPrice: PositiveFloat
    longName: str
    symbol: str
    fiftyTwoWeekLow: PositiveFloat
    fiftyTwoWeekHigh: PositiveFloat
    trailingPE: float
    longBusinessSummary: str
    industry: str
    industryKey: str
    sector: str
    sectorKey: str

