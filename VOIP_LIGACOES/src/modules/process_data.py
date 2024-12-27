import pandas as pd
import tkinter as tk
from tkinter import filedialog
from modules.logger import get_logger
from modules.database import Oracle
from queries_sql.sql_voips import SQL_VOIP_RANKING
from modules.config import X5_BASE_URL, X5_TOKEN
import csv
import os
import requests
from datetime import datetime

# Logger configuration
logger = get_logger()

# Collects current date and month
today = datetime.now()
month = today.month
year = today.year

def select_file() -> str:
    """
    Function to select a single CSV or EXCEL file
    """
    try:
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

        if not file:
            raise ValueError("Nenhum arquivo selecionado!")
        
        return file
    
    except Exception as e:
        error = f"Erro ao selecionar arquivo CSV! {e}"
        logger.error(error)
        raise ValueError(error)

def process_procon_to_df() -> pd.DataFrame:
    """
    Function to process csv file and convert into a dataframe
    """
    # Load the csv file
    csv_file = select_file()

    try:
        # Read the csv file
        file = pd.read_csv(csv_file, sep=';')

        # Create the dataFrame
        df = pd.DataFrame(file)

        # Rename columns
        df.rename(columns={' Data Incr': 'DATA_CADASTRO'}, inplace=True)

        # Convert to 'DDD' column to string 
        df['DDD'] = df['DDD'].astype(str)

        # Concatenate columns to create new column 'TEL_PROCON' 
        df['TEL_PROCON'] = df['DDD'] + df['Telefone'].astype(str)

        # Select specific columns 
        df_filtered = df[['DATA_CADASTRO', 'TEL_PROCON']]

        return df_filtered
    
    except Exception as e:
        error = f"Erro ao tratar dados: {e}"
        logger.error(error)
        raise ValueError(error)

def process_voip_ranking_paramns() -> dict:
    """
    Function to generating VOIP ranking parameters
    """
    oracle = Oracle()

    data = oracle.extract_data(sql=SQL_VOIP_RANKING)

    # Removing all lines with "VER"
    filtered_data = [row for row in data if row[0] != "VER"]
    
    # Dict of sorted VOIP ranking
    params = {
            'num0': filtered_data[0][0],
            'num1': filtered_data[1][0],
            'num2': filtered_data[2][0],
            'num3': filtered_data[3][0],
            'num4': filtered_data[4][0],
            'num5': filtered_data[5][0],
            'num6': filtered_data[6][0]
            }

    return params

def import_to_api(file_path: str, campaing_id: int) -> None:
    """
    Function to import csv file to an X5 campaign via the API

    :param file_path: Path to csv file
    :param campaing_id: Campaing ID 
    """
    import_endpoint = f"{X5_BASE_URL}{campaing_id}/contatos_upload"
    headers = {
        'Authorization': f'Bearer {X5_TOKEN}',
    }

    try:
        # Open csv file
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, 'text/csv')
            }
            # Send the file to endpoint
            response = requests.post(import_endpoint, headers=headers, files=files)

        if response.status_code == 200:
            logger.info(f"Dados importados com sucesso! Arquivo: {file_path}")
        else:
            logger.error(
                f"Erro ao importar dados!" 
                f"ARQUIVO: {file_path}," 
                f"CÓDIGO: {response.status_code}," 
                f"MOTIVO: {response.text}"
            )
            raise
        
    except Exception as e:
        logger.error(f"Erro ao acessar API! {e}")
        raise

def save_csv(df_temp: pd.DataFrame, name: str, num: int) -> str:
    """
    Function to save the dataDrame in CSV with a custom delimiter and replace ';;' with ';'

    :param df_temp: A copy of the DataFrame
    :param name: The name of the consultation type
    :param num: The number of lots for the consultation type
    """
    try:
        path = f"H:/Tecnologia/EQUIPE - DADOS/6 - Voip/00 - AUDIOS VOIP {year}/{year}-{month + 1}"
        file_name = f'{name}_num_{num}.csv'
        # Constructing path to save the files
        file_path = os.path.join(path, file_name)

        # Save the dataFrame to CSV
        df_temp.to_csv(file_path, sep="|", index=False, header=['NOME;;;TELEFONE 1;CPF'], quoting=csv.QUOTE_NONE, escapechar=';')
        logger.info(f"Arquivo {file_name} salvo com sucesso!")

        # Read and replace ';;' with ';' in the csv file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace(';;', ';')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return file_path

    except Exception as e:
        error = f"Erro ao salvar o arquivo {name}_num_{num}.csv: {e}"
        logger.error(error)
        raise ValueError(error)

def process_excel_and_send_api() -> None:
    """
    Function to process data and generate csv files, grouped by with 'NOME_CAMP'
    """
    excel_file = select_file()

    df = pd.read_excel(excel_file)

    names = df['NOME_CAMP'].drop_duplicates()

    # Defining campaign IDs if the month number is pair or odd
    if month % 2 != 0:
        # voip A
        endpoints_voip = {
            "CARDIOLOGIA": 119,
            "CHECK UP SAUDE": 118,
            "CHECKUP_MULHER": 120,
            "ODONTO GERAL": 127,
            "ODONTO": 122,
            "OFTALMOLOGIA": 121,
            "PSICOLOGO E PSIQUIATRIA": 126,
        }
    
    else:
        # voip B
        endpoints_voip = {
            "CARDIOLOGIA": 107,
            "CHECK UP SAUDE": 105,
            "CHECKUP_HOMEM": 106,
            "CHECKUP_MULHER": 109,
            "ODONTO GERAL": 110,
            "ODONTO": 113,
            "OFTALMOLOGIA": 111,
            "PSICOLOGO E PSIQUIATRIA": 108,
        }

    # Delete all data for each campaign from each endpoint
    for index, value in endpoints_voip.items():
        delete_endpoint = f"{X5_BASE_URL}{value}/contatos"
        headers = {
            'Authorization': f'Bearer {X5_TOKEN}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.delete(delete_endpoint, headers=headers)
            if response.status_code == 200:
                logger.info(f"Dados deletados com sucesso! Endpoint {index}")
            else:
                logger.error(
                    f"Erro ao deletar dados!"
                    f"ENDPOINT: {index},"
                    f"CÓDIGO: {response.status_code}," 
                    f"MOTIVO: {response.text}"
                    )
                raise e
        except Exception as e:
            logger.error(f"Erro ao acessar API! {e}")
            raise

    # Divides the excel file into several files of 10000 lines grouping by name
    for name in names:
        try:
            logger.info(f"Processando exame: {name}")
            data = df[df['NOME_CAMP'] == name]['NOME;;;TELEFONE 1;CPF']
            num = 0
            count = 0
            arquivo = []

            # Process the data in blocks of 20.000 lines
            for i in data:
                count += 1
                arquivo.append(i)

                if count == 10000:
                    num += 1
                    count = 0

                    # Create a temporary dataFrame and save it to CSV
                    df_temp = pd.DataFrame(arquivo, columns=['NOME;;;TELEFONE 1;CPF'])
                    file_path = save_csv(df_temp, name, num)

                    arquivo = []  # Clear the list for the next block

                    # Import the generated file to the endpoint
                    if name in endpoints_voip:
                        import_to_api(file_path=file_path, campaing_id=endpoints_voip[name])

            # Process any remaining that was not included in the block of 20.000 lines
            if arquivo:
                num += 1
                df_temp = pd.DataFrame(arquivo, columns=['NOME;;;TELEFONE 1;CPF'])
                file_path = save_csv(df_temp, name, num)

                if name in endpoints_voip:
                    import_to_api(file_path=file_path, campaing_id=endpoints_voip[name])

        except Exception as e:
            error = f"Erro ao processar exame {name}: {e}"
            logger.error(error)
            raise ValueError(error)
