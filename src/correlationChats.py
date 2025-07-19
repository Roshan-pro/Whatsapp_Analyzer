import logging
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd 
import yaml
import os
from abc import ABC,abstractmethod
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config(path=None):
    if path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))  
        path = os.path.join(base_dir, "config.yaml")
    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

class CorrelationMatrix(ABC):
    @abstractmethod
    def correlate(self):
        pass

class WhatsappMatrix(CorrelationMatrix):
    def __init__(self,df:pd.DataFrame):
        self.df=df
    def correlate(self):
        try:
            if self.df is not None and not self.df.empty:
                if not isinstance(self.df,pd.DataFrame):
                    return logging.error("Data should be pandas data frame.")
                logging.info("Finding correlation between chats")
                corr_mat=self.df.corr()
                fig,ax =plt.subplots(figsize=(10,6))
                sns.heatmap(corr_mat,annot=True,cmap=config["visuals"]["color_palette"],ax=ax)
                return fig
        except ValueError as e:
            return logging.error(f"Data is not Loaded {e}")
class WhatsappCorrelation:
    def __init__(self,strategy:CorrelationMatrix):
        self._strategy=strategy
    def plot(self):
        return self._strategy.correlate()