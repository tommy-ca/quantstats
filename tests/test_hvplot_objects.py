import quantstats as qs
import pandas as pd
import numpy as np
import holoviews as hv

def test_returns_returns_hvplot():
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(np.random.randn(len(dates)) * 0.01, index=dates)
    
    # Call with show=False to get the object
    res = qs.plots.returns(returns, show=False)
    
    # We expect res to be a HoloViews object (or hvPlot object)
    assert isinstance(res, (hv.core.Dimensioned, hv.Layout, hv.Overlay)), \
        f"Expected hvPlot/HoloViews object, got {type(res)}"

def test_drawdown_returns_hvplot():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(np.random.randn(len(dates)) * 0.01, index=dates)
    
    res = qs.plots.drawdown(returns, show=False)
    
    assert isinstance(res, (hv.core.Dimensioned, hv.Layout, hv.Overlay)), \
        f"Expected hvPlot/HoloViews object, got {type(res)}"