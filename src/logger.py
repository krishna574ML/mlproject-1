"""
This script configures a basic logging setup for the application.

It creates a log file with a timestamp and sets the logging level to INFO.

The log file includes details like timestamp, log level, module name, function name, line number, and the actual message.
"""

import logging
import os
from datetime import datetime

# Define the format string for the log messages
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s'

LOG_FILE = F"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=LOG_FORMAT,
    level=logging.INFO
)


