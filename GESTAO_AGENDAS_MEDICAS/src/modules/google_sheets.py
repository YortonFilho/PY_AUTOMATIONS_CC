import gspread
import pandas as pd
from modules.logger import get_logger
from datetime import datetime
from google.oauth2.service_account import Credentials
from modules.config import URL_GOOGLE_SHEETS, SCOPE_AUTH_DRIVE, SCOPE_AUTH_SPREADSHEETS, JSON_PATH

# Logging configuration
logger = get_logger()

def google_sheets_connect() -> None:
    """
    Function to connect to google sheets    
    """
    # JSON file path
    try:   
        credentials = Credentials.from_service_account_file(
            JSON_PATH,
            scopes=[SCOPE_AUTH_SPREADSHEETS, SCOPE_AUTH_DRIVE]
        )

        # Authenticate and open the client
        client = gspread.authorize(credentials)
        logger.info("Conexão com planilha google efetuada com sucesso!")
        return client
    except Exception as e:
        logger.error(f'Falha ao se conectar com planilha google: {e}')
        raise e

def google_sheets_extract() -> pd.DataFrame:
    """
    Function to extract data from google sheets
    """
    try:
        # Connecting to google sheets
        client = google_sheets_connect()
        # Acess the specific sheet by name
        sheet = client.open_by_url(URL_GOOGLE_SHEETS).worksheet('Gestão de Agendas')
        # Get all values from the sheet
        data = sheet.get_all_values()

        # Select columns name
        columns = data[0]
        # Convert the data to a dataFrame
        df = pd.DataFrame(data[1:], columns=columns)

        logger.info("Dados extraídos com sucesso da planilha google!")
        return df
    except Exception as e:
        logger.error(f'Falha ao extrair dados da planilha google: {e}')
        raise e

def google_sheets_process_data() -> pd.DataFrame:
    """
    Function to process and rename columns of the dataFrame
    """
    df = google_sheets_extract()

    try:
        # Dictionary for renaming columns
        colmuns_mapping = {
            'Carimbo de data/hora': 'DATA',
            'Endereço de e-mail': 'EMAIL',
            'SOLICITAÇÃO': 'SOLICITACAO',
            'PROFISSIONAL': 'PROFISSIONAL',
            'ÁREA':'AREA',
            'CLINICA':'CLINICA',
            'DATA DA AGENDA':'DATA_AGENDA',
            'DESCRIÇÃO':'DESCRICAO',
            'REMARCAÇÃO':'REMARCACAO',
            'RESPONSÁVEL':'RESPOSAVEL',
            'PROFISSIONAL MENSALISTA':'PROFISSIONAL_MENSALISTA'
        }

        # Select and rename columns
        df_filtered = df[colmuns_mapping.keys()].rename(columns=colmuns_mapping)
        
        # Converting 'DATA' to 'dd/mm/aaaa hh:mm:ss'
        df_filtered['DATA'] = pd.to_datetime(df_filtered['DATA'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        # Converting 'DATA' to 'dd/mm/aaaa'
        df_filtered['DATA_AGENDA'] = pd.to_datetime(df_filtered['DATA_AGENDA'], format='%d/%m/%Y', errors='coerce')
        
        logger.info("Colunas renomeadas e ajustadas com sucesso!")
        return df_filtered
    
    except Exception as e:
        logger.error(f"Falha ao renomear colunas do dataFrame: {e}")
        raise e
