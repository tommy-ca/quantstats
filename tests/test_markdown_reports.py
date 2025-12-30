#!/usr/bin/env python3
import unittest
import os
import pandas as pd
import numpy as np
import quantstats as qs


class TestMarkdownReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate sample data
        np.random.seed(42)
        dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq="D")
        cls.returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)
        cls.benchmark = pd.Series(
            np.random.normal(0.0008, 0.015, len(dates)), index=dates
        )

        cls.multi_returns = pd.DataFrame(
            {
                "Strategy1": np.random.normal(0.001, 0.02, len(dates)),
                "Strategy2": np.random.normal(0.001, 0.015, len(dates)),
            },
            index=dates,
        )

        cls.output_file = "test_report_output.md"

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_basic_markdown_generation(self):
        """Test basic markdown report generation for a Series"""
        qs.reports.markdown(
            self.returns,
            benchmark=self.benchmark,
            title="Test Report",
            output=self.output_file,
        )

        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            content = f.read()
            self.assertIn("# Test Report", content)
            self.assertIn("## Performance Summary", content)
            self.assertIn("data:image/png;base64", content)  # Verify embedded images

    def test_multi_strategy_markdown(self):
        """Test markdown report generation for multiple strategies"""
        qs.reports.markdown(
            self.multi_returns, title="Multi-Strategy Test", output=self.output_file
        )

        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            content = f.read()
            self.assertIn("# Multi-Strategy Test", content)
            self.assertIn("Strategy1", content)
            self.assertIn("Strategy2", content)

    def test_pandas_integration(self):
        """Test the plot_markdown method via extend_pandas"""
        qs.extend_pandas()
        self.returns.plot_markdown(
            benchmark=self.benchmark, title="Pandas Test", output=self.output_file
        )

        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            content = f.read()
            self.assertIn("# Pandas Test", content)

    def test_hvplot_fallback(self):
        """Test that markdown correctly handles hvplot backend by falling back to matplotlib"""
        original_backend = qs._plotting_backend.get_backend()
        try:
            # Attempt to set hvplot if available
            try:
                import hvplot.pandas

                qs._plotting_backend.set_backend("hvplot")
            except ImportError:
                self.skipTest("hvplot not installed")

            qs.reports.markdown(
                self.returns, title="HVPlot Fallback Test", output=self.output_file
            )

            self.assertTrue(os.path.exists(self.output_file))
            with open(self.output_file, "r") as f:
                content = f.read()
                self.assertIn("# HVPlot Fallback Test", content)
                self.assertIn("data:image/png;base64", content)
        finally:
            qs._plotting_backend.set_backend(original_backend)

    def test_no_output_returns_string(self):
        """Test that markdown returns a string if no output file is specified"""
        result = qs.reports.markdown(self.returns, title="String Return Test")
        self.assertIsInstance(result, str)
        self.assertIn("# String Return Test", result)
        self.assertIn("data:image/png;base64", result)


if __name__ == "__main__":
    unittest.main()
