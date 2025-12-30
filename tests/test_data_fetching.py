import quantstats as qs
import pandas as pd

def test_yfinance_data_fetching():
    # Fetch data for AAPL
    data = qs.utils.download_returns("AAPL", period="1mo")
    
    assert isinstance(data, pd.Series), "Expected pandas Series"
    assert not data.empty, "Expected non-empty data"
    # In newer pandas is_all_dates might be removed or replaced.
    # We can check if the index type is DatetimeIndex.
    assert isinstance(data.index, pd.DatetimeIndex), "Expected DatetimeIndex"
