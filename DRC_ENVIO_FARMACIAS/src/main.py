from modules.process_data import update_cpfs_in_excel, cross_cpfs, union_data
from modules.email_functions import no_new_subscribers, new_subscribers
from modules.logger import get_logger
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd
import os

# Logger configuration
logger = get_logger()

def files_path() -> str:
    """
    Function to define file paths 
    """
    # Date variables to nam the file to be saved
    date = datetime.now()
    day = f'{date.day:02d}'
    month = f'{date.month:02d}'
    year = date.year

    # File paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    excel_file = os.path.join(base_path, '05 - farmacia.xlsx')
    output_file = os.path.join(base_path, f'19013906000179 - DR_CENTRAL_FARMACIAS {day}{month}{year}.xlsx')

    return excel_file, output_file

def main():
    """
    Main function to cross data, and send email with
    all new subscribed CPFs
    """
    excel_file, output_file = files_path()

    df = union_data()

    # Check if the excel file exists
    if not os.path.exists(excel_file):
        logger.info(f"Arquvio {excel_file} não existe!")

    # Open the excel file and store the sheets to be checked and updated
    try:
        workbook = load_workbook(excel_file)
        sheet1 = workbook.active  
        sheet2 = workbook.worksheets[1] 
    except Exception as e:
        logger.info(f"Erro ao armazenar abas da planilha excel {excel_file}: {e}")
        raise e

    # Update the Excel file with all CPFs
    update_cpfs_in_excel(sheet1, workbook, excel_file, df)
    # Cross the CPFs to find the new ones and generate the file to send by email
    response = cross_cpfs(sheet1, sheet2, excel_file, workbook, output_file)

    if response != 'EMAIL ENVIADO':
        # Send an email with the new subscriptions
        new_subscribers(output_file)
        
if __name__ == "__main__":
    main()