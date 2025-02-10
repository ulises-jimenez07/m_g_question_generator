"""M&G Q-Gen Logger"""

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