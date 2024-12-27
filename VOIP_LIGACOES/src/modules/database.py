import os
import oracledb
import pandas as pd
from modules.logger import get_logger
from modules.config import DB_NAME, DB_PASSWORD, DB_USER
from queries_sql.sql_voips import SQL_DELETE_VOIP, SQL_INSERT_VOIP

# Function to generate logs
logger = get_logger()

class Oracle:
    def __init__(self) -> None:
        """ 
        Function Initializes the Oracle client 
        and connect to the database
        """
        client_path = r"C:\instantclient_19_21"

        try:
            os.environ["PATH"] = client_path + ";" + os.environ.get("PATH", "")
            oracledb.init_oracle_client(lib_dir=client_path)
            logger.info(f"Cliente Oracle inicializado com sucesso usando o caminho: {client_path}")

        except Exception as e:
            logger.error(f"Erro ao inicializar o cliente Oracle: {e}")
            raise e

        try:
            self.connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_NAME)
            self.cursor = self.connection.cursor()
            logger.info("Banco de dados conectado com sucesso!")
                    
        except oracledb.Error as e:
            error = f"Erro ao se conectar ao bando de dados: {e}"
            logger.error(error)
            raise ValueError(error)
        
    def extract_data(self, sql: str, params: dict = None) -> list:
        """
        Function to execute sql queries

        :param sql: SQL command to be executed
        :param params: Parameters to be used with the SQL command
        """
        try:
            self.cursor.execute(sql, params)
            data =  self.cursor.fetchall()

            return data
        
        except oracledb.Error as e:
            error = f"Erro ao executar consulta SQL! {e}"
            logger.error(error)
            raise ValueError(error)

    def close(self) -> None:
        """
        Function to close the database connection
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Conexão fechada!")
        
    def database_insert(self, df: pd.DataFrame, table: str) -> None:
        """
        Function to insert data from a dataFrame into the database

        :param df: DataFrame containing the data
        :param table: The name of the table
        """
        # Get columns names
        self.cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table}'")
        columns_table = [row[0] for row in self.cursor.fetchall()]

        # Get the numbers of columns from table and the dataframe
        num_columns_table = len(columns_table)
        num_columns_df = len(df.columns)

        # Check if the number of columns in the table and the datafram are the same
        if num_columns_table != num_columns_df:
            error = (
                f"O número de colunas da tabela {num_columns_table}"
                f"é diferente do dataFrame {num_columns_df}"
                )
            logger.error(error)
            raise ValueError(error)
        
        # Reorder the dataframe columns to match the table columns 
        df_filtered = df[columns_table]

        # Prepare query to insert data into database
        placeholder = ', '.join([f":{col}" for col in range(num_columns_table)])
        insert_command = f"INSERT INTO {table} ({', '.join(columns_table)}) VALUES ({placeholder})"

        # Insert new data
        for index, row in df_filtered.iterrows():
            # Convert dataFrame to a list
            values = row.tolist()
            # Replace empty values with None
            values = [None if v == '' or pd.isna(v) else v for v in values]

            try:
                self.cursor.execute(insert_command, values)  
                logger.info(f"Dados inseridos com sucesso: {values}")
            except oracledb.Error as e:
                logger.error(f"Erro ao inserir os seguintes dados: {values} ERRO: {e})")
                self.connection.rollback() 
                raise

        self.connection.commit()

    def sequence_voip_commands_sql(self) -> None:
        """
        Function to execute SQL commands
        """
        try:
            self.cursor.execute(SQL_DELETE_VOIP)
            logger.info("Dados do VOIP deletados com sucesso!")
        except oracledb.Error as e:
            self.connection.rollback()
            error = "Erro ao deletar dados do VOIP!"
            logger.error(error)
            raise ValueError(error)
        
        try:
            self.cursor.execute(SQL_INSERT_VOIP)
            logger.info("Dados importados para o VOIP com sucesso!")
        except oracledb.Error as e:
            self.connection.rollback()
            error = f"Erro ao importar dados para o VOIP! {e}"
            logger.error(error)
            raise ValueError(error)
