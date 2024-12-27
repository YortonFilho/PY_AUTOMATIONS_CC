from modules.database import database_extract, database_update
from modules.process_data import process_data

def main():
    # Extract data
    df = database_extract()
    
    # Process data
    formatted_df = process_data(df)

    # Insert data into the databse
    database_update(formatted_df)

if __name__ == "__main__":
    main()