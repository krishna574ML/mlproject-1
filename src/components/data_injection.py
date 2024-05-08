import os
import sys
from src.exception import CustomException  # Importing the class and methods from src/exception.py
from src.logger import logging  # Assuming a logging module for structured logging
import pandas as pd

from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from dataclasses import dataclass
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig  


# Data Ingestion Configuration (Optional)
@dataclass
class DataIngestionConfig:
    train_data_path :str = os.path.join('artifacts' , 'train.cv')
    test_data_path :str = os.path.join('artifacts' , 'test.cv')
    raw_data_path:str = os.path.join('artifacts' , 'data.cv')

class DataIngestion:
    """
    Class responsible for data ingestion tasks, including:
     - Reading data from CSV
     - Creating directories for output data (if needed)
     - Splitting data into training and testing sets
     - Saving split data to CSV files
    """

    def __init__(self, config: DataIngestionConfig = None):
        """
        Initializes the DataIngestion object.

        Args:
            config (DataIngestionConfig, optional): Configuration object for data paths.
                Defaults to None, using default paths defined in the class.
        """
        self.config = DataIngestionConfig()  # Use provided config or defaults

    def initiate_data_ingestion(self):
        """
        Performs the data ingestion process.

        Raises:
            CustomException: If any error occurs during data ingestion.
        """
        logging.info("Entered the data ingestion method")

        try:
            # Read data from CSV
            df = pd.read_csv('data/stud.csv')
            logging.info("Data set successfully loaded as a DataFrame.")

            # Create directories for output data (if needed)
            os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)

            df.to_csv(self.config.raw_data_path , index=True, header=True)

            # Split data into training and testing sets
            train_set, test_set = train_test_split(df, test_size=0.33, random_state=42)
            logging.info("Train/test split completed.")

            # Save split data to CSV files
            train_set.to_csv(self.config.train_data_path, index=True, header=True)
            test_set.to_csv(self.config.test_data_path, index=True, header=True)
            logging.info("Data saved to training and testing CSV files.")

            logging.info("Data ingestion completed successfully.")

            return self.config.train_data_path, self.config.test_data_path

        except Exception as e:
            error_msg = CustomException.error_message_detail(str(e))
            logging.info(error_msg)  # Log error messages with a higher severity level (error)
            raise CustomException(error_msg)  # Re-raise the custom exception for clearer error handling

if __name__ == '__main__':
    data_ingester = DataIngestion()
    train_data, test_data = data_ingester.initiate_data_ingestion()

    data_transformation = DataTransformation()
    
    transformed_train_data, transformed_test_data , pkl_1 = data_transformation.initiate_data_transformation(train_data , test_data)

    ModelTrainer = ModelTrainer()
    print(ModelTrainer.initiate_model_trainer(transformed_train_data, transformed_test_data))