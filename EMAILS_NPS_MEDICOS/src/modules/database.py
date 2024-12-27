import os
import oracledb
import pandas as pd
from modules.logger import get_logger
from modules.config import DB_NAME, DB_PASSWORD, DB_USER

# Configuração de logs
logger = get_logger()

# Função para inicializar o cliente Oracle
def init_oracle_client() -> None:
    """Inicializa o cliente Oracle usando o caminho do cliente Instant Client."""
    client_path = r"C:\instantclient_19_21"

    try:
        os.environ["PATH"] = client_path + ";" + os.environ.get("PATH", "")
        oracledb.init_oracle_client(lib_dir=client_path)
        logger.info(f"Cliente Oracle inicializado com sucesso usando o caminho: {client_path}")
    except Exception as e:
        logger.error(f"Erro ao inicializar o cliente Oracle: {e}")
        raise e

# Função para conectar ao banco de dados
def database_connection() -> oracledb.Connection:
    init_oracle_client() # Inicializa o cliente Oracle

    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_NAME)
        logger.info("Banco de dados conectado com sucesso!")
        return connection
    except oracledb.Error as e:
        logger.error(f"Falha ao tentar conexão com banco de dados! {e}")
        raise e

# Função para extrair dados dos NPS dos médicos do banco e retornar como DataFrame
def database_extract_nps() -> pd.DataFrame:
    try:
        with database_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        *
                    FROM
                        VBI_DADOS_ENVIO_NPS_MEDICOS
                """

                # Executando query e armazenando todos os dados em 'data'
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Verificando se há dados
                if not data:
                    logger.warning("Nenhum dado encontrado na consulta.")
                    raise
                
                # Armazenando nomes das colunas
                columns = [column[0] for column in cursor.description]

                # Criando dataFrame
                df = pd.DataFrame(data, columns=columns)
                logger.info(f"Dados extraídos com sucesso! Total de {len(df)} registros.")
                
                return df
            
    except Exception as e:
        logger.error(f"Erro ao extrair dados: {e}")
        raise e
