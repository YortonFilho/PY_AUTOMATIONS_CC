import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_logger():
    """
    Function to generate logs
    """
    return logging.getLogger()
