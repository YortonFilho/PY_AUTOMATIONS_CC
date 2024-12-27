import os
from dotenv import load_dotenv
from modules.logger import get_logger

# Função de logging
logger = get_logger()

def check_env_var(var_name):
    """
    Função para verificar se uma variável de ambiente existe e não está vazia.

    :param var_name: Nome da variável de ambiente
    """
    value = os.getenv(var_name)
    
    if not value or not value.strip():
        erro = f"A variável de ambiente {var_name} não foi encontrada no arquivo .env!"
        logger.error(erro)
        raise ValueError(erro)
    return value
         
# Loads the environment variables from the .env file
load_dotenv()

# Checks the environment variables for databse connection
DB_NAME = check_env_var("DB_NAME")
DB_USER = check_env_var("DB_USER")
DB_PASSWORD = check_env_var("DB_PASSWORD")