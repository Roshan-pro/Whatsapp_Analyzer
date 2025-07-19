import logging
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from abc import ABC,abstractmethod
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class WeeklyMessage(ABC):
    @abstractmethod
    def analysis(self,df:pd.DataFrame,sender_name:str):
        pass
class MembersWeeklyMessage(WeeklyMessage):
    def analysis(self, df:pd.DataFrame, sender_name:str):
        logging.info(f"Analysing {sender_name} weakly message. ")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.error("Data should be in pandas dataframe.")
                elif not isinstance(sender_name,str):
                    return logging.error(f"Sender name :{sender_name} should be in string.")
                member_data = df[df["Sender"] == sender_name].copy()

                member_data["DayOfWeek"] = member_data["Date"].dt.day_name()

                weekday_counts = member_data["DayOfWeek"].value_counts().reindex(
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0
                )

                plt.figure(figsize=(10, 5))
                sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette="coolwarm")

                plt.title(f"Message Activity by Day of Week\n{sender_name}", fontsize=14)
                plt.xlabel("Day of Week")
                plt.ylabel("Number of Messages")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
        except ValueError as e:
            return logging.error(f"Something went wrong in MembersWeaklyMessage {e} ")
class WeekMeassage:
    def __init__(self,strategy:WeeklyMessage):
        self._strategy=strategy
    def analysis(self,df:pd.DataFrame,sender_name:str):
        return self._strategy.analysis(df,sender_name)