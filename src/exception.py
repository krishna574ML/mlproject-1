import sys
sys.path.append('D:/mlprojects')  # Adjust the path to match the location of your src directory
from src.logger import logging
from src.logger import logging
class CustomException(Exception):
    


    """
    A custom exception class for handling errors within your application.

    This class inherits from the standard `Exception` class in Python,
    allowing you to create more specific exceptions tailored to your needs.

    Attributes:
        error_message (str): A detailed error message explaining the issue.
    """

    def __init__(self, error_message: str, error_details=sys.exc_info()):
        
        """
        Initializes a new `CustomException` object.

        Args:
            error_message (str): The primary error message to be displayed.
            error_details (sys.exc_info, optional): Internal system details
                about the error. Defaults to `sys.exc_info()`. This can
                provide more context for debugging purposes.
        """

        super().__init__(error_message)  # Call the superclass's __init__ method to initialize the exception with the given error message
        self.error_message = error_message  # Store the error message for later reference
        self.error_details = error_details  # Store additional error details for debugging purposes, defaults to sys.exc_info()

    
        

    def __str__(self) -> str:
        """
        Returns the error message associated with this exception.

        This method is automatically called when you try to print or directly
        convert the `CustomException` object to a string.

        Returns:
            str: The error message.
        """

        return self.error_message
    
    def error_message_detail(error_message,error_details=sys.exc_info()):
        """
        This function creates a detailed error message for easier troubleshooting.

        Args:
            error (Exception): The error object that occurred.
            error_details (sys.exc_info, optional): Internal system details about the error.
                Defaults to sys.exc_info().

        Returns:
            str: A formatted error message containing the following information:
                - Error type (e.g., ValueError, TypeError)
                - Script name where the error occurred
                - Line number where the error occurred
                - The actual error message
        """
        # Unpack the error details (ignore the first two return values from exc_info())
        _, _, exc_tb = error_details

        # Extract the filename and line number from the traceback
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        # Construct the error message with clear formatting
        return f"Error: {type(error_message).__name__} occurred in '{file_name}' on line {line_number}.\n" \
               f"Error message: {str(error_message)}"

        

