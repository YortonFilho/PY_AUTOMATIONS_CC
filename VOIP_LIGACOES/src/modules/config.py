import os
from dotenv import load_dotenv
from modules.logger import get_logger

# Function to generate logs
logger = get_logger()

def check_variables(variable_name: str) -> str:
    """
    Function to check environment variables from the .env file

    :param variable_name: Name of the environmente variable
    """
    value = os.getenv(variable_name)

    if not value or not value.strip():
        error = f"A variábel de ambiente {variable_name} não foi encontrada no arquivo '.env'!"
        logger.error(error)
        raise ValueError(error)
    
    return value

# Check environment variables
DB_NAME = check_variables("DB_NAME")
DB_USER = check_variables("DB_USER")
DB_PASSWORD = check_variables("DB_PASSWORD")

X5_TOKEN = check_variables("X5_TOKEN")
X5_BASE_URL = check_variables("X5_BASE_URL")