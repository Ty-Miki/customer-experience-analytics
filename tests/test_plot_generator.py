import pandas as pd
import pytest
from unittest.mock import patch
from scripts.plot_generator import PlotGenerator

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "category": ["A", "B", "A", "B"],
        "value": [10, 20, 15, 25],
        "hue_col": ["X", "X", "Y", "Y"]
    })

def test_plot_barchart_calls_seaborn_and_matplotlib(sample_df):
    plotter = PlotGenerator(sample_df)
    with patch("scripts.plot_generator.sns.barplot") as mock_barplot, \
         patch("scripts.plot_generator.plt.savefig") as mock_savefig, \
         patch("scripts.plot_generator.plt.show"), \
         patch("scripts.plot_generator.plt.close"):
        plotter.plot_barchart(
            x_value="category",
            y_value="value",
            hue="hue_col",
            title="Test Chart",
            x_label="Category",
            y_label="Value",
            legend=True,
            file_path="test_chart.png"
        )
        mock_barplot.assert_called_once_with(data=sample_df, x="category", y="value", hue="hue_col")
        mock_savefig.assert_called_once_with("test_chart.png")

def test_plot_barchart_no_legend(sample_df):
    plotter = PlotGenerator(sample_df)
    with patch("scripts.plot_generator.plt.legend") as mock_legend, \
         patch("scripts.plot_generator.sns.barplot"), \
         patch("scripts.plot_generator.plt.savefig"), \
         patch("scripts.plot_generator.plt.show"), \
         patch("scripts.plot_generator.plt.close"):
        plotter.plot_barchart(
            x_value="category",
            y_value="value",
            legend=False
        )
        mock_legend.assert_called_once_with([], [], frameon=False)