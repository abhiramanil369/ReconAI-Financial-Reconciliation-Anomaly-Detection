# DAY - 1 Task 

import pandas as pd

df = pd.read_csv('sample_dataset/transaction_data.csv')

# print(df)
# print(df.head())

# print(df.info())

# print(df.describe())

# print(df.shape)

# print(df.columns)

# print(df.columns.tolist())  # ['Transaction_ID', 'Customer_ID', 'Account_Type', 'Total_Balance', 
                            # 'Transaction_Amount', 'Investment_Amount', 'Investment_Type', 'Transaction_Date']

# print(df.dtypes)

# transaction_sum = df.groupby('Customer_ID')['Transaction_Amount'].sum().reset_index()

# print(transaction_sum)


# print(df['Transaction_Amount'].sum())

# print(df.isnull().sum()) # TO identify the null values in the dataset

# print(df.duplicated().sum()) # TO identify the duplicate values in the dataset



# print(df['Account_Type'].value_counts()) # TO identify the unique values in the dataset
# print(df['Investment_Type'].value_counts()) # TO identify the unique values in the dataset

# financial_columns = ['Transaction_Amount', 'Total_Balance', 'Investment_Amount']

# print(df.describe()[financial_columns]) # TO identify the statistical summary of the dataset



df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])

# print(df.dtypes) # TO identify the data types of the dataset

# print("Earliest Transaction Date:", df['Transaction_Date'].min())
# print("Latest Transaction Date:", df['Transaction_Date'].max())

print(df.info())