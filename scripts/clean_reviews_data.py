import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_reviews(df: pd.DataFrame, drop_columns: list, rename_columns: dict, new_columns: dict):
    """
    Cleans the reviews DataFrame by dropping specified columns, renaming others, and adding new columns.
    
    Args:
        df (pd.DataFrame): The DataFrame containing reviews data.
        drop_columns (list): List of columns to drop.
        rename_columns (dict): Dictionary mapping old column names to new names.
        new_columns (dict): Dictionary of new columns to add with their default values.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Drop specified columns
    df.drop(columns=drop_columns, inplace=True, errors='ignore')
    
    # Rename columns
    df.rename(columns=rename_columns, inplace=True)
    
    # Add new columns with default values
    for col, value in new_columns.items():
        df[col] = value
    
    logging.info(f"Data cleaned. New shape: {df.shape}")
    
    return df