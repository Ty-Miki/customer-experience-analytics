import seaborn as sns
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PlotGenerator:
    def __init__(self, df):
        """
        Initialize the PlotGenerator with a pandas DataFrame.
        """
        self.df = df
        logging.info("Plot generator initialized successfully.")

    def plot_barchart(
        self,
        x_value: str,
        y_value: str,
        hue: str = None,
        title: str = "Bar Chart",
        x_label: str = None,
        y_label: str = None,
        legend: bool = True,
        file_path: str = "bar_chart.png"
    ):
        """
        Generate and save a bar chart from the provided DataFrame.

        Parameters:
        - x_value (str): Column to be used on the x-axis.
        - y_value (str): Column to be used on the y-axis.
        - hue (str, optional): Column to group bars by color.
        - title (str): Title of the chart.
        - x_label (str, optional): Label for the x-axis.
        - y_label (str, optional): Label for the y-axis.
        - legend (bool): Whether to show legend.
        - file_path (str): Path to save the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(data=self.df, x=x_value, y=y_value, hue=hue)

        plt.title(title)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)

        if not legend:
            plt.legend([], [], frameon=False)
        elif hue:
            plt.legend(title=hue)

        plt.tight_layout()
        plt.savefig(file_path)
        plt.show()
        plt.close()  # prevent overlapping plots in Jupyter

        logging.info(f"[✓] Bar chart saved to: {file_path}")
