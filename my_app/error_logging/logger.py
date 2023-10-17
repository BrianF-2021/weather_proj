import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.ERROR)

# Create a file handler that writes log messages to a file
file_handler = logging.FileHandler('error.log', mode='w')
file_handler.setLevel(logging.ERROR)

# Create a console handler that prints log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# Define the log message format
formatter = logging.Formatter(
    '\n%(asctime)s [%(levelname)s]: \n\t%(message)s \n')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
