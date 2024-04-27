import os
import sys
from src.exception import CustomException # importing the class and the methods from src/exception.py file
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

@dataclass
class DataIngestionConfig:
    train_data_path :str = os.path.join('artifacts' , 'train.cv')
    test_data_path :str = os.path.join('artifacts' , 'test.cv')
    raw_data_path:str = os.path.join('artifacts' , 'data.cv')

class DataIngection:
    def __init__(self):
        self.injection_config = DataIngestionConfig()

    def initiate_data_intiate(self):
        logging.info("Entered the data ingection method or component")
        try:
            df = pd.read_csv('data\stud.csv')
            logging.info("Exported the data set and stored as dataframe")
            os.makedirs(os.path.dirname(self.injection_config.train_data_path) , exist_ok= True)

            df.to_csv(self.injection_config.raw_data_path , index=True, header=True)

            logging.info("Train test split initiated")
            train_set, test_set  = train_test_split(df, test_size=0.33, random_state=42)
            
            train_set.to_csv(self.injection_config.train_data_path , index=True, header=True)
            test_set.to_csv(self.injection_config.test_data_path , index=True, header=True)

            logging.info('ingestion of data is completed')

            return(

                self.injection_config.train_data_path, 
                self.injection_config.test_data_path, 
             )
        except Exception as e:
            error_msg = CustomException.error_message_detail(str(e))
            logging.info(error_msg)

            

    


