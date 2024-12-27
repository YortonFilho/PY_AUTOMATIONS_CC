import os
import oracledb
import pandas as pd
from modules.logger import get_logger
from modules.config import DB_NAME, DB_PASSWORD, DB_USER

# Logging configuration
logger = get_logger()

# Function to initialize the Oracle client
def init_oracle_client() -> None:
    """Initializes the Oracle client using Instant client path"""
    client_path = r"C:\instantclient_19_21"

    try:
        os.environ["PATH"] = client_path + ";" + os.environ.get("PATH", "")
        oracledb.init_oracle_client(lib_dir=client_path)
        logger.info(f"Cliente Oracle inicializado com sucesso usando o caminho: {client_path}")
    except Exception as e:
        logger.error(f"Erro ao inicializar o cliente Oracle: {e}")
        raise e

# Function to connect to the database
def database_connection() -> oracledb.Connection:
    init_oracle_client() # Initializes Oracle Client

    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_NAME)
        logger.info("Banco de dados conectado com sucesso!")
        return connection
    except oracledb.Error as e:
        logger.error(f"Falha ao tentar conexão com banco de dados! {e}")
        raise e

def database_update(df, table) -> None:
    """Function to delete all data from the table and 
    insert all data from the dataFrame into a table in the database
    
    :param df: Dataframe containing all the data
    :param table: Table to insert the data into
    """
    try:
        # Connecting to the database and opening a cursor
        with database_connection() as connection:
            with connection.cursor() as cursor:
                
                # Get columns of the table
                cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table}'")
                columns = [row[0] for row in cursor.fetchall()]
                num_columns = len(columns)

                # Order the columns of the dataFrame to match the table's columns
                df_filtered = df[columns] 

                # Check if the number of columns in the dataframe and table are equal
                if len(df_filtered.columns) != num_columns:
                    raise logger.error(
                        f"Número de colunas no DataFrame ({len(df_filtered.columns)})" 
                        f"não corresponde ao número de colunas na tabela Oracle ({num_columns})."
                    )

                # Prepare the query for inserting data
                placeholders = ', '.join([f':{col}' for col in columns])  # Using :column_name as placeholder
                insert_command = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

                try:
                    # Delete data in table
                    cursor.execute(f"DELETE FROM {table}")
                    logger.info(f"Dados da tabela deletados com sucesso!")

                    # Insert new data
                    for index, row in df_filtered.iterrows():
                        values = row.to_dict()  # Convert row to dictionary

                        try:
                            cursor.execute(insert_command, values)  # Pass dictionary for binding variables
                        except oracledb.Error as e:
                            logger.error(f"Erro ao inserir os seguintes dados: {values} ERRO: {e})")
                            connection.rollback() 
                            raise e

                    connection.commit()
                    logger.info(f"Todos os dados foram inseridos na tabela '{table}'!")

                except oracledb.Error as e:   
                    logger.error(f"Erro ao deletar dados da tabela {table}: {e}")
                    connection.rollback()
                    raise e

    except oracledb.Error as e:
        logger.error(f'Erro ao se conectar com banco de dados! {e}')
        raise e
