from typing import Optional
from pydantic import BaseModel, Field, PositiveFloat


class StockMetaData(BaseModel):
    """
    StockMetaData is a Pydantic model designed for validating and mapping stock-related data
    from a JSON response. It ensures the data adheres to specific types and constraints,
    making it easier to process and display on a dashboard or other applications.

    Attributes:
        uuid (str): Unique identifier for the stock.
        currentPrice (PositiveFloat): The current trading price of the stock, must be positive.
        fiftyTwoWeekLow (PositiveFloat): The lowest price of the stock in the last 52 weeks, must be positive.
        fiftyTwoWeekHigh (PositiveFloat): The highest price of the stock in the last 52 weeks, must be positive.
        trailingPE (Optional[float]): The trailing price-to-earnings ratio of the stock, must be non-negative.
        longName (str): The full name of the company, default is an empty string.
        symbol (str): The ticker symbol of the stock, default is an empty string.
        longBusinessSummary (str): A detailed business summary of the company, default is an empty string.
        industry (str): The industry category of the stock, default is an empty string.
        industryKey (str): An identifier or key for the industry, default is an empty string.
        sector (str): The sector category of the stock, default is an empty string.
        sectorKey (str): An identifier or key for the sector, default is an empty string.
        website (str): The company's website URL, default is an empty string.

    Usage:
        - This model is intended for parsing and validating stock data received from an API in JSON format.
        - It ensures that only the valid fields are used in your application while handling default values
          for optional fields.
    """

    uuid: str
    currentPrice: PositiveFloat
    fiftyTwoWeekLow: PositiveFloat
    fiftyTwoWeekHigh: PositiveFloat
    trailingPE: Optional[float] = Field(
        0.0, ge=0
    )  # Optional and must be >= 0 if provided
    longName: str = Field(default="")
    symbol: str = Field(default="")
    longBusinessSummary: str = Field(default="")
    industry: str = Field(default="")
    industryKey: str = Field(default="")
    sector: str = Field(default="")
    sectorKey: str = Field(default="")
    website: str = Field(default="")

    class Config:
        populate_by_name = (
            True  # Allows validation with field names even if aliases are used
        )
