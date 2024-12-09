import logging
# tail -f server.log in bash to check logs
#if any error occurs any moment, it will be saved in server.log, in future we can find out what happened at what time

def setup_logger(name,log_file='server.log',level=logging.DEBUG):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Configure the custom logger
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger