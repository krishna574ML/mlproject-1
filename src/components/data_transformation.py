import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path: str = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformer_object(self):
        try:
            numerical_features = ['reading_score', 'writing_score']
            categorical_features = ['gender', 'race_ethnicity', 'parental_level_of_education',
                                     'lunch', 'test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical columns scaling completed.")

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder())
                ]
            )
            logging.info("Categorical columns encoding completed.")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", categorical_pipeline, categorical_features)
                ]
            )
            return preprocessor

        except Exception as e:
            error_msg = CustomException.error_message_detail(str(e))
            logging.error(error_msg)  # Log error messages with a higher severity level
            raise CustomException(error_msg)  # Re-raise the custom exception for clearer error handling

    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info("Read train and test data completed.")
            logging.info("Obtaining preprocessing object.")

            preprocessor_obj = self.get_transformer_object()
            target_column = "math_score"

            train_features = train_df.drop(columns=[target_column], axis=1)
            test_features = test_df.drop(columns=[target_column], axis=1)

            train_target = train_df[target_column]
            test_target = test_df[target_column]

            logging.info("Applying preprocessing data to train and test.")

            train_features_processed = preprocessor_obj.fit_transform(train_features)
            test_features_processed = preprocessor_obj.transform(test_features)

            train_data = np.c_[train_features_processed, train_target.to_numpy()]
            test_data = np.c_[test_features_processed, test_target.to_numpy()]

            logging.info("Saving preprocessor object.")

            save_object(file_path=self.data_transformation_config.preprocessor_obj_path, obj=preprocessor_obj)

            return train_data, test_data, self.data_transformation_config.preprocessor_obj_path
        
        except Exception as e:
            error_msg = CustomException.error_message_detail(str(e))
            logging.error(error_msg)  # Log error messages with a higher severity level (error)
            raise CustomException(error_msg)  # Re-raise the custom exception for clearer error handling
