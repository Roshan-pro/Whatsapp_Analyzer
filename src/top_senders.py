import logging
import pandas as pd 
from abc import ABC,abstractmethod
import matplotlib.pyplot as plt 
import seaborn as sns 
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TopSendersStrategy(ABC):
    @abstractmethod
    def check_senders(self,df:pd.DataFrame,senders:int=None):
        pass
class Barplot(TopSendersStrategy):
    def check_senders(self, df:pd.DataFrame,senders:int=None):
        logging.info(f"Preparing to plot bar graph of top {senders} senders.")
        try:
            if df is not None and not df.empty:
                    if not isinstance(df, pd.DataFrame):
                        return logging.info("Data should be pandas data frame.")
                    if not isinstance(senders, int):
                        return logging.info("Senders value  should be a int.")
                    top_5_senders=df["Sender"].value_counts().head(senders)
                    plt.Figure(figsize=(10,6))
                    sns.barplot(x=top_5_senders.values,y=top_5_senders.index,palette="coolwarm",legend=False)
                    plt.title(f"Top {senders} Most active members")
                    plt.xlabel("Message send")
                    plt.ylabel("senders")
                    plt.tight_layout()
                    plt.show()
        except Exception as e:
            return logging.error(f"Error in barplot strategy: {e}")
class TopSenedr:
    def __init__(self,strategy:TopSendersStrategy):
        self._strategy=strategy
    def plot(self,df:pd.DataFrame,senders:int):
        return self._strategy.check_senders(df,senders)