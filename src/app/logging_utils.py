"""Provides a pre-configured logger instance.

This module sets up a basic logger named "logger" with an INFO logging level.
It can be directly imported and used in other modules.  Commented-out code
shows an example of how to add a file handler and custom formatter if needed.
"""

import logging
import logging.config

# Create the Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("logger")
# logger.setLevel(logging.INFO)

# # Create the Handler for logging data to a file
# logger_handler = logging.FileHandler(filename='C:\Python\Log\stest.txt')
# logger_handler.setLevel(logging.DEBUG)

# # Create a Formatter for formatting the log messages
# logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# # Add the Formatter to the Handler
# logger_handler.setFormatter(logger_formatter)

# # Add the Handler to the Logger
# logger.addHandler(logger_handler)
# logger.info('Completed configuring logger()!')
