import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models

from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts" , "model.pkl")
    
class ModelTrainer:
    
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                'Random Forest': RandomForestRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'LinearRegression': LinearRegression(),
                'KN Classifer': KNeighborsRegressor(),
                'xgboost': XGBRegressor(),
                'CatBossting Classifer': CatBoostRegressor(verbose=False),
                'AdaBoost Classifer': AdaBoostRegressor()
            }

            model_report = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)

            # Sort the dict with maximum r2 value.
            best_model_name = None
            best_r_squared = -1  # Initialize with a negative value

            for model_name, model_scores in model_report.items():
                if model_scores > best_r_squared:
                    best_model_name = model_name
                    best_r_squared = model_scores

            if best_model_name is None:
                raise CustomException("No best model found")

            best_model_score = models[best_model_name]

            logging.info("Best model is selected and all the algorithms are used")

            try:
                save_object(file_path=self.model_trainer_config.trained_model_file_path,
                            obj=best_model_score)
            except Exception as e:
                logging.error(f"Error saving the best model: {str(e)}")

            predicted = best_model_score.predict(X_test)
            r2_squared = r2_score(y_test, predicted)

            return best_model_name, r2_squared

        except Exception as e:
            raise CustomException(e, sys)

        