import logging
import pandas as pd 
from abc import ABC,abstractmethod
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FeatureEnginneeringStrategy(ABC):
    @abstractmethod
    def apply(self):
        pass

class SetDatesMonths(FeatureEnginneeringStrategy):
    def __init__(self,df:pd.DataFrame,DateCol:str=None):
        self.date=DateCol
        self.df=df
    def apply(self):
        logging.info("Making Date and Month new columns")
        try:
            if self.df is not None and not self.df.empty:
                if not isinstance(self.df,pd.DataFrame):
                    return logging.info("Data should be pandas data frame.")
                elif not isinstance(self.date,str):
                    return logging.info("columns should be given in string format.")
                self.df[self.date]=pd.to_datetime(self.df[self.date],errors='coerce')
                self.df["Day"]=self.df[self.date].dt.strftime('%A')
                self.df["Month"]=self.df[self.date].dt.strftime('%B')
                return self.df
        except ValueError as e:
            return logging.error(f"Data is avaialbe :{e}")
class Repalacestrategy(FeatureEnginneeringStrategy):
    def __init__(self, df: pd.DataFrame, replacements: dict):
        self.df = df
        self.replacements = replacements  

    def apply(self):
        
            logging.info(f"Replacing values using mapping: {self.replacements}")
            try:
                if self.df is not None and not self.df.empty:
                    if not isinstance(self.df, pd.DataFrame):
                        return logging.info("Data should be pandas data frame.")
                    if not isinstance(self.replacements, dict):
                        return logging.info("Replacements should be a dictionary.")

                    for col, mapping in self.replacements.items():
                        if col in self.df.columns:
                            self.df[col] = self.df[col].replace(mapping)
                    return self.df
                else:
                    return logging.info("DataFrame is empty or None.")
            except Exception as e:
                return logging.error(f"Error in replacement strategy: {e}")

class FeautreEng:
    def __init__(self,strategy:FeatureEnginneeringStrategy):
        self._strategy=strategy
    def set_strategy(self,strategy:FeatureEnginneeringStrategy):
        self._strategy=strategy
    def apply(self):
        return self._strategy.apply()