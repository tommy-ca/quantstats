import os
import sys
import importlib

import numpy as np
import pandas as pd


def _load_quantstats(backend="hvplot"):
    os.environ["QS_PLOT_BACKEND"] = backend
    for mod in list(sys.modules):
        if mod.startswith("quantstats"):
            del sys.modules[mod]
    return importlib.import_module("quantstats")


def _sample_returns():
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2023-01-01", end="2024-01-01", freq="D")
    returns_series = pd.Series(rng.normal(0, 0.01, size=len(dates)), index=dates)
    returns_df = pd.DataFrame({"returns": returns_series})
    return returns_series, returns_df


def test_cvar_consistent_for_series_and_dataframe():
    qs = _load_quantstats()
    returns_series, returns_df = _sample_returns()

    cvar_series = qs.stats.cvar(returns_series)
    cvar_df = qs.stats.cvar(returns_df)

    assert np.isclose(cvar_series, cvar_df)


def test_cvar_appears_in_metrics_report():
    qs = _load_quantstats()
    returns_series, _ = _sample_returns()

    metrics = qs.reports.metrics(returns_series, mode="full", display=False)
    assert "Expected Shortfall (cVaR)" in metrics.index
