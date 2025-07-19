import logging
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd 
from abc import ABC,abstractmethod
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
class MostFrequentWordStrategy(ABC):
    @abstractmethod
    def frequentWords(self,df:pd.DataFrame):
        pass

class MostFrequentWordsinGroups(MostFrequentWordStrategy):
    def frequentWords(self, df:pd.DataFrame):
        logging.info("Creating Wordcloud of most frequent Messages send in group.")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.error("Data should be in pandas Dataframe")
                text = " ".join(message for message in df["Message"] if isinstance(message, str))

                custom_stopwords = set(STOPWORDS)
                custom_stopwords.update(["media", "omitted", "sticker", "gif", "image", "video", "file"])  

                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    stopwords=custom_stopwords,
                    colormap='viridis'
                ).generate(text)

                plt.figure(figsize=(12, 6))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.title("Most Frequent Words in WhatsApp Chat", fontsize=16)
                plt.show()
        except Exception as e:
            return logging.error(f"Error in MostFrequentWordsinGroups {e}")

class MostFrequentWordsfromMembers(MostFrequentWordStrategy):
    def __init__(self,sender_name:str):
        self.sender_name=sender_name
    def frequentWords(self, df:pd.DataFrame):
        logging.info("Creating Wordcloud of most frequent Messages send by  group members.")
        try:
            if df is not  None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.error("Data should be pandas dataframe")
                elif not isinstance(self.sender_name,str):
                    return logging.error("Write senders name in str (under----> '')")
                sender_messages = df[df["Sender"] == self.sender_name]
                total_messages = sender_messages.shape[0]
                logging.info(f"Total messages sent by '{self.sender_name}': {total_messages}")

                text = " ".join(msg for msg in sender_messages["Message"] if isinstance(msg, str))
                stopwords = set(STOPWORDS)
                stopwords.update(["media", "omitted", "sticker", "gif", "image", "video", "file"])

                # Generate word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)

                plt.figure(figsize=(12, 6))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.title(f"Most Word used  by {self.sender_name}", fontsize=14)
                plt.show()

                df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

                most_active_day = sender_messages["Date"].value_counts().idxmax()
                messages_that_day = sender_messages["Date"].value_counts().max()

                logging.info(f"Most active day by '{self.sender_name}': {most_active_day.date()} with {messages_that_day} messages")
                # return most_active_day,messages_that_day
        except ValueError as e:
            return logging.error("something is wrong in MostFrequentWordsfromMembers")

class MostFrequentWords:
    def __init__(self,strategy:MostFrequentWordStrategy):
        self._strategy=strategy
    def set_strategy(self,strategy:MostFrequentWordStrategy):
        self._strategy=strategy
    def checkFreqWords(self,df:pd.DataFrame):
        return self._strategy.frequentWords(df)