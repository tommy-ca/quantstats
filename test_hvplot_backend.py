import os
import sys
import importlib

import numpy as np
import pandas as pd


def _load_quantstats(backend):
    os.environ["QS_PLOT_BACKEND"] = backend
    for mod in list(sys.modules):
        if mod.startswith("quantstats"):
            del sys.modules[mod]
    return importlib.import_module("quantstats")


def _sample_returns():
    rng = np.random.default_rng(7)
    dates = pd.date_range("2024-01-01", periods=120, freq="D")
    return pd.Series(rng.normal(0, 0.01, size=len(dates)), index=dates, name="Strategy")


def test_hvplot_returns_object():
    qs = _load_quantstats("hvplot")
    returns = _sample_returns()
    plot = qs.plots.returns(returns, show=False)
    assert hasattr(plot, "opts")
    assert plot.__class__.__module__.startswith("holoviews")


def test_hvplot_does_not_import_matplotlib_or_seaborn():
    for mod in list(sys.modules):
        if mod.startswith("matplotlib") or mod.startswith("seaborn"):
            del sys.modules[mod]

    qs = _load_quantstats("hvplot")
    returns = _sample_returns()
    _ = qs.plots.returns(returns, show=False)

    assert "matplotlib" not in sys.modules
    assert "seaborn" not in sys.modules


def test_hvplot_report_contains_bokeh_markers(tmp_path):
    qs = _load_quantstats("hvplot")
    returns = _sample_returns()
    benchmark = returns * 0.8
    out = tmp_path / "report.html"

    qs.reports.html(returns, benchmark, output=str(out), title="Test Report")
    html = out.read_text(encoding="utf-8")

    assert "data-root-id" in html
    assert "Bokeh" in html
    assert "<script" in html
