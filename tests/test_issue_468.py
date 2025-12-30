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
    returns = pd.Series(rng.normal(0, 0.01, size=len(dates)), index=dates)
    benchmark = pd.Series(rng.normal(0, 0.008, size=len(dates)), index=dates)
    return returns, benchmark


def test_report_html_does_not_raise_mode_use_inf_as_null(tmp_path):
    qs = _load_quantstats()
    returns, benchmark = _sample_returns()
    output = tmp_path / "test_report.html"

    qs.reports.html(
        returns,
        benchmark,
        benchmark_title="SPY",
        output=str(output),
        title="Test Report",
    )

    html = output.read_text(encoding="utf-8")
    assert "mode.use_inf_as_null" not in html
