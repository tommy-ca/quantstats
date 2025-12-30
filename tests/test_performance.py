#!/usr/bin/env python3
import time
import os
import sys
import importlib
import pandas as pd
import numpy as np
import quantstats as qs


def _load_quantstats(backend):
    os.environ["QS_PLOT_BACKEND"] = backend
    for mod in list(sys.modules):
        if mod.startswith("quantstats"):
            del sys.modules[mod]
    return importlib.import_module("quantstats")


def _generate_test_data(n_points=10_000):
    """Generate test data with specified number of points."""
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2020-01-01", periods=n_points, freq="D")
    return pd.Series(rng.normal(0.001, 0.02, n_points), index=dates, name="Strategy")


def test_hvplot_vs_matplotlib_performance():
    """Benchmark hvPlot vs matplotlib generation times."""
    returns = _generate_test_data(10_000)  # 10K points

    # Test matplotlib backend
    qs_mpl = _load_quantstats("matplotlib")
    start_time = time.time()
    for _ in range(10):
        _ = qs_mpl.plots.returns(returns, show=False)
    mpl_time = time.time() - start_time

    # Test hvPlot backend
    qs_hvplot = _load_quantstats("hvplot")
    start_time = time.time()
    for _ in range(10):
        _ = qs_hvplot.plots.returns(returns, show=False)
    hvplot_time = time.time() - start_time

    # Assert hvPlot is within 110% of matplotlib time
    ratio = hvplot_time / mpl_time
    assert ratio < 1.1, (
        f"hvPlot time ({hvplot_time:.3f}s) exceeds 110% of matplotlib time ({mpl_time:.3f}s) - ratio: {ratio:.2f}"
    )
    print(
        f"Performance: hvPlot ({hvplot_time:.3f}s) vs matplotlib ({mpl_time:.3f}s) = {ratio:.2f}x"
    )


def test_multi_column_performance():
    """Test performance with multiple strategy columns."""
    n_strategies = 10
    dates = pd.date_range(start="2020-01-01", periods=10_000, freq="D")
    rng = np.random.default_rng(42)

    returns = pd.DataFrame(
        {
            f"Strategy_{i + 1}": rng.normal(0.001, 0.02, len(dates))
            for i in range(n_strategies)
        },
        index=dates,
    )

    qs = _load_quantstats("hvplot")
    start_time = time.time()

    _ = qs.plots.returns(returns, show=False)

    elapsed = time.time() - start_time

    # Should complete in reasonable time for 10 columns
    assert elapsed < 30.0, (
        f"Multi-column generation ({elapsed:.1f}s) exceeds 30s for 10 columns"
    )
    print(f"Multi-column (10 cols) generation time: {elapsed:.1f}s")


def test_high_frequency_data():
    """Test with high-frequency (minute-level) data."""
    dates = pd.date_range(
        start="2024-01-01", periods=10_000, freq="min"
    )  # ~7 days of minute data
    rng = np.random.default_rng(42)
    returns = pd.Series(
        rng.normal(0.0001, 0.005, len(dates)), index=dates, name="HighFreq"
    )

    qs = _load_quantstats("hvplot")
    start_time = time.time()

    _ = qs.plots.returns(returns, show=False)

    elapsed = time.time() - start_time

    # Minute-level data may take longer but should still be reasonable
    assert elapsed < 10.0, (
        f"High-frequency generation ({elapsed:.1f}s) exceeds 10s for 10K minute points"
    )
    print(f"High-frequency (10K minute points) generation time: {elapsed:.1f}s")


def test_report_generation_benchmark():
    """Benchmark full HTML report generation time."""
    returns = _generate_test_data(50_000)
    benchmark = returns * 0.8

    qs = _load_quantstats("hvplot")

    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp:
        start_time = time.time()
        qs.reports.html(returns, benchmark, output=tmp.name, title="Benchmark Report")
        elapsed = time.time() - start_time

        # Full report should complete in reasonable time
        assert elapsed < 60.0, (
            f"Report generation ({elapsed:.1f}s) exceeds 60s for 50K points"
        )
        assert os.path.exists(tmp.name), "Report file not created"
        print(f"Full HTML report generation time: {elapsed:.1f}s")
        os.unlink(tmp.name)  # Cleanup
