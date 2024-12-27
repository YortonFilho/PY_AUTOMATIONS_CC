import os
from dotenv import load_dotenv
from modules.logger import get_logger

# Logging function
logger = get_logger()

# Load the environment variables from the .env file
load_dotenv()

def check_env_var(var_name) -> str:
    """
    Function to check if an environment variable exists and is not empty

    :param var_name: Name of the environmet variable
    """
    value = os.getenv(var_name)
    
    if not value or not value.strip():
        erro = f"A variável de ambiente {var_name} não foi encontrada no arquivo .env!"
        logger.error(erro)
        raise ValueError(erro)
    return value

# Check environments variables for the database
DB_NAME = check_env_var("DB_NAME")
DB_USER = check_env_var("DB_USER")
DB_PASSWORD = check_env_var("DB_PASSWORD")

# Check environments for google sheets
URL_GOOGLE_SHEETS = check_env_var("URL_GOOGLE_SHEETS")
SCOPE_AUTH_DRIVE = check_env_var("SCOPE_AUTH_DRIVE")
SCOPE_AUTH_SPREADSHEETS = check_env_var("SCOPE_AUTH_SPREADSHEETS")
JSON_PATH = check_env_var("JSON_PATH")