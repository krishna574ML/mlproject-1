import os
import sys
from src.exception import CustomException  # Importing the class and methods from src/exception.py
from src.logger import logging  # Assuming a logging module for structured logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Data Ingestion Configuration (Optional)
@dataclass
class DataIngestionConfig:
    """
    Data paths configuration for the data ingestion process.
    """
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


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
        self.config = config or DataIngestionConfig()  # Use provided config or defaults

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
            logging.error(error_msg)  # Log error messages with a higher severity level (error)
            raise CustomException(error_msg)  # Re-raise the custom exception for clearer error handling

if __name__ == '__main__':
    data_ingester = DataIngestion()
    train_path, test_path = data_ingester.initiate_data_ingestion()
    print(f"Training data path: {train_path}")
    print(f"Testing data path: {test_path}")
