import logging


# Configure the main logger (if not configured already)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

# Create a separate logger for elapsed time
time_logger = logging.getLogger('elapsed_time_logger')
time_logger.setLevel(logging.INFO)

# Add a file handler to the time_logger
time_handler = logging.FileHandler('elapsed_time.log')
time_handler.setLevel(logging.INFO)

# Set the format for the time_logger
time_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
time_handler.setFormatter(time_formatter)

# Add the handler to the time_logger
time_logger.addHandler(time_handler)

# Create a separate logger for authentication
auth_logger = logging.getLogger('authentication_logger')
auth_logger.setLevel(logging.INFO)

# Add a file handler to the auth_logger
auth_handler = logging.FileHandler('authentication.log')
auth_handler.setLevel(logging.INFO)

# Set the format for the auth_logger
auth_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
auth_handler.setFormatter(auth_formatter)

# Add the handler to the auth_logger
auth_logger.addHandler(auth_handler)
