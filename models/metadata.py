from typing import Optional
from pydantic import BaseModel, Field, PositiveFloat

class StockMetaData(BaseModel):
    uuid: str
    currentPrice: PositiveFloat
    fiftyTwoWeekLow: PositiveFloat
    fiftyTwoWeekHigh: PositiveFloat
    trailingPE: Optional[float] = Field(0.0, ge=0)  # Optional and must be >= 0 if provided
    longName: str = Field(default='')
    symbol: str = Field(default='')
    longBusinessSummary: str = Field(default='')
    industry: str = Field(default='')
    industryKey: str = Field(default='')
    sector: str = Field(default='')
    sectorKey: str = Field(default='')
    website: str = Field(default='')

    class Config:
        populate_by_name = True  # Allows validation with field names even if aliases are used
