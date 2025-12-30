import quantstats as qs
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup

def test_html_report_contains_hvplot_markers():
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(np.random.randn(len(dates)) * 0.01, index=dates)
    
    output_file = "test_report.html"
    if os.path.exists(output_file):
        os.remove(output_file)
        
    try:
        # Generate report
        # We need a small dataset for speed
        qs.reports.html(returns, output=output_file, show=False)
        
        # Verify file exists
        assert os.path.exists(output_file), "Report file was not created"
        
        # Read and parse
        with open(output_file, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Check for Bokeh/HoloViews markers
        # Current reports use static images. New reports should have Bokeh scripts.
        has_bokeh = any("bokeh" in str(s).lower() for s in soup.find_all("script"))
        
        assert has_bokeh, "Bokeh scripts not found in HTML report. The migration might not be active."
        
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
