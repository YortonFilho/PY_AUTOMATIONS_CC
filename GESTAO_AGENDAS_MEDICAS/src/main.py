from modules.google_sheets import google_sheets_process_data
from modules.database import database_update

# Main function
def main():
    # Extract and process data
    df = google_sheets_process_data()

    # Update table in the dataBase 
    database_update(df=df, table='GESTAO_AGENDAS')

if __name__ == "__main__":
    main()