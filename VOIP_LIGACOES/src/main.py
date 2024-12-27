#from modules.database import Oracle
from modules.process_data import process_procon_to_df, process_voip_ranking_paramns, process_excel_and_send_api
from queries_sql.sql_voips import SQL_MAILING
from modules.database import Oracle
import pandas as pd
import openpyxl

def main():
    """
    Function to execute the main functions
    """
    # Database functions class
    oracle = Oracle()

    # max_date = oracle.extract_data("SELECT MAX(DATA_CADASTRO) FROM TEL_PROCON")
    # # Formating date to 'DD/MM/AAAA'
    # formatted_date = max_date[0][0].strftime("%d/%m/%Y")
    # print(formatted_date)

    # Convert the csv with the procon numbers into a dataframe
    df = process_procon_to_df()
    # Import data from the dataFrama into the database
    oracle.database_insert(df, "TEL_PROCON")

    # Execute a sequence of sql commands
    oracle.sequence_voip_commands_sql()

    # Generates a ranking of the best exams
    params_ranking = process_voip_ranking_paramns()
    # Execute a sql command with ranking data
    data = oracle.extract_data(sql=SQL_MAILING, params=params_ranking)

    # Defines the name of the columns
    columns = [
    'NOME_CAMP',
    'NOME;;;TELEFONE 1;CPF',
    'NAO'
    ]
    # Create a dataframe with the data collected from the ranking and the defined columns name
    df = pd.DataFrame(data, columns=columns)

    # Remove the last column
    df = df.iloc[:, :-1]  # Isso seleciona todas as colunas, exceto a última

    # Generate a excel file
    df.to_excel('2 - BASE_MAILING_VOIP.xlsx', engine="openpyxl", index=False)
    
    # Generates csv files and sends them via API to X5
    process_excel_and_send_api()
    

if __name__ == "__main__":
    main()