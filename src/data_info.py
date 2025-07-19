import logging
import pandas as pd 
from abc import ABC,abstractmethod
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
class DataInformationStrategy(ABC):
    @abstractmethod
    def check(self,df:pd.DataFrame):
        pass
class DataInfo(DataInformationStrategy):
    def check(self, df:pd.DataFrame):
        logging.info("Checking Information of Data.")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.info("Data should be in pandas DataFrame")
                return logging.info(f"\nData's Information:\n{df.info()}")
        except ValueError as e:
            return logging.error(f"Data is not present {e}")
            
class ISNULL(DataInformationStrategy):
    def check(self, df:pd.DataFrame):
        logging.info("Checking whether Data has null value.")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.info("Data should be in pandas DataFrame")
                return logging.info(f"\nNumber of Null values:\n{df.isna().sum()}")
        except ValueError as e:
            return logging.error(f"Data is not present{e}")
class DuplicatePresent(DataInformationStrategy):
    def check(self, df:pd.DataFrame):
        logging.info("Checking duplicate value present in Data.")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.info("Data should be in pandas DataFrame")
                return logging.info(f"\nData's duplicate Values:\n{df.duplicated().sum()}")
        except ValueError as e:
            return logging.error(f"Data is not present {e}")
class ValueCounts(DataInformationStrategy):
    def __init__(self,sender_columns:str="Sender"):
        self.sender=sender_columns
    def check(self, df:pd.DataFrame):
        logging.info("Most active members in group")
        try:
            if df is not None and not df.empty:
                if not isinstance(df,pd.DataFrame):
                    return logging.info("Data should be in pandas DataFrame")
                return logging.error(f"\nMost active memebers in group {df[self.sender].value_counts()}")
        except ValueError as e:
            return logging.info(f"Data is not present {e}")
class DataInformation:
    def __init__(self,strategy:DataInformationStrategy):
        self._strategy=strategy
    def set_strategy(self,strategy:DataInformationStrategy):
        self._strategy=strategy
    def info(self,df:pd.DataFrame):
        return self._strategy.check(df)