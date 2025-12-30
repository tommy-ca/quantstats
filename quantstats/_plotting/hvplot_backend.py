"""hvPlot backend implementations for QuantStats plots."""

from __future__ import annotations

import pandas as _pd
import numpy as _np

from .. import stats as _stats
from .. import utils as _utils
from .._compat import safe_resample

_HV = None


def _ensure_hvplot():
    global _HV
    if _HV is not None:
        return _HV
    try:
        import holoviews as hv
        import hvplot.pandas  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "hvplot and holoviews are required for the hvplot backend. "
            "Install quantstats[hvplot] or set QS_PLOT_BACKEND=matplotlib."
        ) from exc
    hv.extension("bokeh", logo=False)
    _HV = hv
    return _HV


def bokeh_resources() -> str:
    from bokeh.resources import CDN

    return CDN.render()


def render_bokeh(obj):
    hv = _ensure_hvplot()
    from bokeh.embed import components

    bokeh_obj = hv.render(obj, backend="bokeh")
    return components(bokeh_obj)


def _as_dataframe(data, name):
    if isinstance(data, _pd.Series):
        if data.name is None:
            data = data.rename(name)
        return data.to_frame()
    return data.copy()


def _join_benchmark(df, benchmark, name="Benchmark"):
    if isinstance(benchmark, _pd.Series):
        if benchmark.name is None:
            benchmark = benchmark.rename(name)
        elif benchmark.name in df.columns:
            benchmark = benchmark.rename(name)
        df = df.join(benchmark, how="inner")
    return df


def _prepare_timeseries(
    returns,
    benchmark=None,
    compound=False,
    resample=None,
    match_volatility=False,
    raw_data=False,
):
    returns = returns.fillna(0)
    if isinstance(benchmark, _pd.Series):
        benchmark = benchmark.fillna(0)

    if match_volatility and benchmark is None:
        raise ValueError("match_volatility requires passing of benchmark.")
    if match_volatility and benchmark is not None:
        bmark_vol = benchmark.std()
        returns = (returns / returns.std()) * bmark_vol

    if not raw_data:
        if compound:
            returns = _stats.compsum(returns)
            if isinstance(benchmark, _pd.Series):
                benchmark = _stats.compsum(benchmark)
        else:
            returns = returns.cumsum()
            if isinstance(benchmark, _pd.Series):
                benchmark = benchmark.cumsum()

    if resample:
        returns = safe_resample(returns, resample, "last" if compound else "sum")
        if isinstance(benchmark, _pd.Series):
            benchmark = safe_resample(benchmark, resample, "last" if compound else "sum")

    return returns, benchmark


def snapshot(
    returns,
    grayscale=False,
    figsize=(10, 8),
    title="Portfolio Summary",
    fontname="Arial",
    lw=1.5,
    mode="comp",
    subtitle=True,
    savefig=None,
    show=True,
    log_scale=False,
    **kwargs,
):
    hv = _ensure_hvplot()
    returns_plot = _utils.make_portfolio(returns.dropna(), 1, mode).pct_change(
        fill_method=None
    ).fillna(0)
    cum = _stats.compsum(returns_plot) * 100 if mode.lower() not in ["cumsum", "sum"] else returns_plot.cumsum() * 100
    dd = _stats.to_drawdown_series(returns_plot) * 100

    cum_plot = _as_dataframe(cum, "Cumulative").hvplot.line(
        title=title, ylabel="Cumulative Return", width=int(figsize[0] * 100)
    )
    dd_plot = _as_dataframe(dd, "Drawdown").hvplot.area(
        ylabel="Drawdown", width=int(figsize[0] * 100)
    )
    daily_plot = _as_dataframe(returns_plot * 100, "Daily").hvplot.line(
        ylabel="Daily Return", width=int(figsize[0] * 100)
    )

    layout = hv.Layout([cum_plot, dd_plot, daily_plot]).cols(1)
    if log_scale:
        layout = layout.opts(logy=True)
    return layout


def earnings(
    returns,
    start_balance=1e5,
    mode="comp",
    grayscale=False,
    figsize=(10, 6),
    title="Portfolio Earnings",
    fontname="Arial",
    lw=1.5,
    subtitle=True,
    savefig=None,
    show=True,
):
    _ensure_hvplot()
    series = _utils.make_portfolio(returns, start_balance, mode)
    data = _as_dataframe(series, "Value")
    return data.hvplot.line(title=title, ylabel="Value")


def returns(
    returns,
    benchmark=None,
    grayscale=False,
    figsize=(10, 6),
    fontname="Arial",
    lw=1.5,
    match_volatility=False,
    compound=True,
    resample=None,
    ylabel="Cumulative Returns",
    subtitle=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    title = "Cumulative Returns" if compound else "Returns"
    if benchmark is not None:
        title += " vs Benchmark"
        if match_volatility:
            title += " (Volatility Matched)"
        benchmark = _utils._prepare_benchmark(benchmark, returns.index)

    if prepare_returns:
        returns = _utils._prepare_returns(returns)

    returns, benchmark = _prepare_timeseries(
        returns,
        benchmark=benchmark,
        compound=compound,
        resample=resample,
        match_volatility=match_volatility,
    )

    data = _as_dataframe(returns, "Strategy")
    data = _join_benchmark(data, benchmark)
    return data.hvplot.line(title=title, ylabel=ylabel)


def log_returns(
    returns,
    benchmark=None,
    grayscale=False,
    figsize=(10, 5),
    fontname="Arial",
    lw=1.5,
    match_volatility=False,
    compound=True,
    resample=None,
    ylabel="Cumulative Returns",
    subtitle=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    title = "Cumulative Returns" if compound else "Returns"
    if benchmark is not None:
        title += " vs Benchmark (Log Scaled)"
        if match_volatility:
            title += " (Volatility Matched)"
    else:
        title += " (Log Scaled)"

    if prepare_returns:
        returns = _utils._prepare_returns(returns)

    benchmark = _utils._prepare_benchmark(benchmark, returns.index)  # type: ignore

    returns, benchmark = _prepare_timeseries(
        returns,
        benchmark=benchmark,
        compound=compound,
        resample=resample,
        match_volatility=match_volatility,
    )
    data = _as_dataframe(returns, "Strategy")
    data = _join_benchmark(data, benchmark)
    return data.hvplot.line(title=title, ylabel=ylabel, logy=True)


def daily_returns(
    returns,
    benchmark,
    grayscale=False,
    figsize=(10, 4),
    fontname="Arial",
    lw=0.5,
    log_scale=False,
    ylabel="Returns",
    subtitle=True,
    savefig=None,
    show=True,
    prepare_returns=True,
    active=False,
):
    _ensure_hvplot()
    if prepare_returns:
        returns = _utils._prepare_returns(returns)
        if active and benchmark is not None:
            benchmark = _utils._prepare_returns(benchmark)
            returns = returns - benchmark

    plot_title = "Daily Active Returns" if active else "Daily Returns"
    plot_title += " (Cumulative Sum)"

    returns, _ = _prepare_timeseries(
        returns,
        benchmark=None,
        compound=False,
        resample="D",
        match_volatility=False,
    )
    data = _as_dataframe(returns, "Returns")
    return data.hvplot.line(title=plot_title, ylabel=ylabel, logy=log_scale)


def yearly_returns(
    returns,
    benchmark=None,
    fontname="Arial",
    grayscale=False,
    hlw=1.5,
    hlcolor="red",
    hllabel="",
    match_volatility=False,
    log_scale=False,
    figsize=(10, 5),
    ylabel=True,
    subtitle=True,
    compounded=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    title = "EOY Returns"
    if benchmark is not None:
        title += " vs Benchmark"
        benchmark = _utils._prepare_benchmark(benchmark, returns.index)
        benchmark = safe_resample(benchmark, "YE", _stats.comp)
        benchmark = safe_resample(benchmark, "YE", "last")

    if prepare_returns:
        returns = _utils._prepare_returns(returns)

    if compounded:
        returns = safe_resample(returns, "YE", _stats.comp)
    else:
        returns = safe_resample(returns, "YE", "sum")
    returns = safe_resample(returns, "YE", "last")

    data = _as_dataframe(returns, "Strategy")
    data = _join_benchmark(data, benchmark)
    if isinstance(data.index, (_pd.DatetimeIndex, _pd.PeriodIndex)):
        data = data.copy()
        data.index = data.index.astype(str)
    return data.hvplot.bar(title=title, ylabel="Returns")


def distribution(
    returns,
    fontname="Arial",
    grayscale=False,
    ylabel=True,
    figsize=(10, 6),
    subtitle=True,
    compounded=True,
    savefig=None,
    show=True,
    title=None,
    prepare_returns=True,
):
    _ensure_hvplot()
    if prepare_returns:
        returns = _utils._prepare_returns(returns)
    data = _as_dataframe(returns, title or "Returns")
    return data.hvplot.hist(title=title or "Returns Distribution", ylabel="Density")


def histogram(
    returns,
    benchmark=None,
    resample="ME",
    fontname="Arial",
    grayscale=False,
    figsize=(10, 5),
    ylabel=True,
    subtitle=True,
    compounded=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    if prepare_returns:
        returns = _utils._prepare_returns(returns)
        if benchmark is not None:
            benchmark = _utils._prepare_returns(benchmark)

    apply_fnc = _stats.comp if compounded else _np.sum
    if benchmark is not None:
        benchmark = safe_resample(benchmark, resample, apply_fnc)
        benchmark = safe_resample(benchmark, resample, "last")

    returns = safe_resample(returns, resample, apply_fnc)
    returns = safe_resample(returns, resample, "last")

    data = _as_dataframe(returns, "Strategy")
    data = _join_benchmark(data, benchmark)
    return data.hvplot.hist(title="Distribution of Returns", ylabel="Density")


def drawdown(
    returns,
    grayscale=False,
    figsize=(10, 5),
    fontname="Arial",
    lw=1,
    log_scale=False,
    match_volatility=False,
    compound=False,
    ylabel="Drawdown",
    resample=None,
    subtitle=True,
    savefig=None,
    show=True,
):
    _ensure_hvplot()
    dd = _stats.to_drawdown_series(returns)
    dd = _as_dataframe(dd, "Drawdown")
    return dd.hvplot.area(title="Underwater Plot", ylabel=ylabel, logy=log_scale)


def drawdowns_periods(
    returns,
    periods=5,
    lw=1.5,
    log_scale=False,
    fontname="Arial",
    grayscale=False,
    title=None,
    figsize=(10, 5),
    ylabel=True,
    subtitle=True,
    compounded=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    if prepare_returns:
        returns = _utils._prepare_returns(returns)

    dd = _stats.to_drawdown_series(returns.fillna(0))
    dddf = _stats.drawdown_details(dd)
    longest = dddf.sort_values(by="days", ascending=False, kind="mergesort")[:periods]

    series = _stats.compsum(returns) if compounded else returns.cumsum()
    data = _as_dataframe(series, "Backtest")
    for idx, (start, end) in enumerate(zip(longest["start"], longest["end"])):
        col = f"DD {idx + 1}"
        data[col] = series.where((series.index >= start) & (series.index <= end))

    return data.hvplot.line(title=title or "Worst Drawdown Periods", ylabel="Returns", logy=log_scale)


def rolling_beta(
    returns,
    benchmark,
    window1=126,
    window1_label="6-Months",
    window2=252,
    window2_label="12-Months",
    lw=1.5,
    fontname="Arial",
    grayscale=False,
    figsize=(10, 3),
    ylabel=True,
    subtitle=True,
    savefig=None,
    show=True,
    prepare_returns=True,
):
    _ensure_hvplot()
    if prepare_returns:
        returns = _utils._prepare_returns(returns)
    benchmark = _utils._prepare_benchmark(benchmark, returns.index)  # type: ignore

    data = _pd.DataFrame(index=returns.index)
    if isinstance(returns, _pd.Series):
        label = window1_label or f"{window1}"
        data[label] = _stats.rolling_greeks(returns, benchmark, window1)["beta"].fillna(0)
        if window2:
            label2 = window2_label or f"{window2}"
            data[label2] = _stats.rolling_greeks(returns, benchmark, window2)["beta"].fillna(0)
    else:
        for col in returns.columns:
            label = f"{col} ({window1_label or window1})"
            data[label] = _stats.rolling_greeks(returns[col], benchmark, window1)["beta"].fillna(0)
        if window2:
            for col in returns.columns:
                label = f"{col} ({window2_label or window2})"
                data[label] = _stats.rolling_greeks(returns[col], benchmark, window2)["beta"].fillna(0)

    return data.hvplot.line(title="Rolling Beta to Benchmark", ylabel="Beta")


def rolling_volatility(
    returns,
    benchmark=None,
    period=126,
    period_label="6-Months",
    periods_per_year=252,
    lw=1.5,
    fontname="Arial",
    grayscale=False,
    figsize=(10, 3),
    ylabel="Volatility",
    subtitle=True,
    savefig=None,
    show=True,
):
    _ensure_hvplot()
    returns = _stats.rolling_volatility(returns, period, periods_per_year)
    data = _as_dataframe(returns, "Volatility")
    if benchmark is not None:
        benchmark = _utils._prepare_benchmark(benchmark, returns.index)
        bench = _stats.rolling_volatility(benchmark, period, periods_per_year, prepare_returns=False)
        data = _join_benchmark(data, bench)
    return data.hvplot.line(title=f"Rolling Volatility ({period_label})", ylabel=ylabel)


def rolling_sharpe(
    returns,
    benchmark=None,
    rf=0.0,
    period=126,
    period_label="6-Months",
    periods_per_year=252,
    lw=1.25,
    fontname="Arial",
    grayscale=False,
    figsize=(10, 3),
    ylabel="Sharpe",
    subtitle=True,
    savefig=None,
    show=True,
):
    _ensure_hvplot()
    returns = _stats.rolling_sharpe(returns, rf, period, True, periods_per_year)
    data = _as_dataframe(returns, "Sharpe")
    if benchmark is not None:
        benchmark = _utils._prepare_benchmark(benchmark, returns.index, rf)
        bench = _stats.rolling_sharpe(benchmark, rf, period, True, periods_per_year, prepare_returns=False)
        data = _join_benchmark(data, bench)
    return data.hvplot.line(title=f"Rolling Sharpe ({period_label})", ylabel=ylabel)


def rolling_sortino(
    returns,
    benchmark=None,
    rf=0.0,
    period=126,
    period_label="6-Months",
    periods_per_year=252,
    lw=1.25,
    fontname="Arial",
    grayscale=False,
    figsize=(10, 3),
    ylabel="Sortino",
    subtitle=True,
    savefig=None,
    show=True,
):
    _ensure_hvplot()
    returns = _stats.rolling_sortino(returns, rf, period, True, periods_per_year)
    data = _as_dataframe(returns, "Sortino")
    if benchmark is not None:
        benchmark = _utils._prepare_benchmark(benchmark, returns.index, rf)
        bench = _stats.rolling_sortino(benchmark, rf, period, True, periods_per_year, prepare_returns=False)
        data = _join_benchmark(data, bench)
    return data.hvplot.line(title=f"Rolling Sortino ({period_label})", ylabel=ylabel)


def monthly_heatmap(
    returns,
    benchmark=None,
    annot_size=10,
    figsize=(8, 5),
    cbar=True,
    square=False,
    returns_label="Strategy",
    compounded=True,
    eoy=False,
    grayscale=False,
    fontname="Arial",
    ylabel=True,
    savefig=None,
    show=True,
    active=False,
):
    _ensure_hvplot()
    monthly = _stats.monthly_returns(returns, eoy=eoy, compounded=compounded) * 100
    if active and benchmark is not None:
        bench = _stats.monthly_returns(benchmark, eoy=eoy, compounded=compounded) * 100
        monthly = monthly - bench

    month_order = list(monthly.columns)
    year_col = monthly.index.name or "Year"
    monthly.index.name = year_col
    data = monthly.reset_index().melt(id_vars=year_col, var_name="Month", value_name="Return")
    data["Month"] = _pd.Categorical(data["Month"], categories=month_order, ordered=True)

    return data.hvplot.heatmap(
        x="Month",
        y=year_col,
        C="Return",
        title=f"{returns_label} - Monthly Returns (%)",
        colorbar=cbar,
    )


def monthly_returns(
    returns,
    annot_size=9,
    figsize=(10, 5),
    cbar=True,
    square=False,
    compounded=True,
    eoy=False,
    grayscale=False,
    fontname="Arial",
    ylabel=True,
    savefig=None,
    show=True,
):
    return monthly_heatmap(
        returns,
        annot_size=annot_size,
        figsize=figsize,
        cbar=cbar,
        square=square,
        compounded=compounded,
        eoy=eoy,
        grayscale=grayscale,
        fontname=fontname,
        ylabel=ylabel,
        savefig=savefig,
        show=show,
    )
