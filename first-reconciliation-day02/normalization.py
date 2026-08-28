import pandas as pd

def normalize_data(df):
    df = df.copy() # Create a copy of the DataFrame to avoid modifying the original data

    df["Customer_ID"] = df["Customer_ID"].astype(str).str.strip().str.upper() # Normalize Customer_ID to uppercase and remove leading/trailing whitespace

    df["Account_Type"] = df["Account_Type"].astype(str).str.strip().str.upper() # Normalize Account_Type to uppercase and remove leading/trailing whitespace

    df["Investment_Type"] = df["Investment_Type"].astype(str).str.strip().str.upper() # Normalize Investment_Type to uppercase and remove leading/trailing whitespace

    numeric_columns = [
        "Total_Balance",
        "Transaction_Amount",
        "Investment_Amount",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors = "coerce"
        )

    df["Transaction_Date"] = pd.to_datetime(
        df["Transaction_Date"],
        errors = "coerce"

    )

    return df