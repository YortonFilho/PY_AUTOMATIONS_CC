import pandas as pd

def process_data(df):
    """
    Function to process data from the dataframe
    """
    # Remove special characters using applymap for each column
    df = df.apply(lambda col: col.map(lambda x: x.encode('ascii', 'ignore').decode('ascii') if isinstance(x, str) else x))

    # Convert the date to the 'DD/MM/AAAA', replacing invalid values with None
    if 'DATA_AGENDA' in df.columns:
        df['DATA_AGENDA'] = pd.to_datetime(df['DATA_AGENDA'], errors='coerce').dt.strftime('%d/%m/%Y')

    # Replace all NaN values with None in the entire Dataframe
    for column in df.columns:
        df[column] = df[column].apply(lambda x: None if pd.isna(x) else x)

    # For string type columns, replace Nan with an empty string or the desired value
    for column in df.columns:
        df[column] = df[column].fillna('')

    return df
