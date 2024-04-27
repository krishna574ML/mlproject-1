import os
import sys
import dill

import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        error_msg = CustomException.error_message_detail(str(e))
        logging.info(error_msg)  # Log error messages with a higher severity level (error)
        raise CustomException(error_msg)  # Re-raise the custom exception for clearer error handling
