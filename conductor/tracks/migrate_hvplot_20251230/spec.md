# Spec: Migrate visualizations from Matplotlib/Seaborn to hvPlot

## Overview
The goal of this track is to modernize the visualization layer of QuantStats by replacing the static Matplotlib/Seaborn plots with interactive hvPlot charts. This will provide users with a more dynamic and engaging experience when analyzing portfolio performance, both in notebooks and in generated HTML reports.

## Requirements
- Identify all existing plot functions in `quantstats/plots.py` and `quantstats/_plotting/`.
- Implement hvPlot equivalents for all core visualizations (Equity Curve, Drawdowns, Monthly Returns, etc.).
- Update the report generation logic in `quantstats/reports.py` and `quantstats/report.html` to support embedding interactive Bokeh/HoloViews objects produced by hvPlot.
- Maintain consistency in the visual style defined in `product-guidelines.md`.
- Ensure that the new interactive charts are responsive and work well within the existing HTML report structure.

## Technical Details
- **Backend:** hvPlot (built on HoloViews and Bokeh).
- **Integration:** hvPlot objects can be exported to HTML/JS snippets for inclusion in reports.
- **Compatibility:** Where possible, provide a way for users to still generate static plots if needed, or ensure the new plots cover all previous use cases.

## Success Criteria
- All standard QuantStats plots are successfully migrated to hvPlot.
- HTML reports feature interactive charts with hover tools, zooming, and panning.
- The new plotting system maintains or improves upon the existing statistical accuracy and visual clarity.
