from modules.email_functions import send_emails_to_users
from modules.database import database_extract_nps
from modules.logger import get_logger

# Configuração de logs
logger = get_logger()

# Função principal
def main():
    try:
        # Extraindo dados do banco de dados Oracle
        users_data = database_extract_nps()

        # Enviando emails
        send_emails_to_users(users_data)

    except Exception as e:
        logger.error(f"Erro ao executar scrip principal! {e}")

if __name__ == "__main__":
    main()