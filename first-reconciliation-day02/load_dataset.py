import pandas as pd

internal = pd.read_csv("transaction_data.csv", dtype={"Customer_ID": str}) # Read internal data from CSV with Customer_ID as string


external = internal.copy() # Create copy of internal

external.loc[0, 'Customer_ID'] = str(external.loc[0,'Customer_ID']).lower() # change first row of CustomerID to lowercase [Formatting differences]


external.loc[1, 'Transaction_Amount'] += 500 # Amount discrepancy in second row of Transaction_Amount [Data entry error]

external = external.drop(index = 2) # Remove third row due to missing Transaction_Amount [Missing data]

external = pd.concat([external, external.iloc[[3]]], ignore_index=True) # Duplicate fourth row to simulate duplicate transaction [Duplicate data]


external.to_csv("external.csv", index =False) # Save external data to CSV
internal.to_csv("internal.csv", index =False) # Save internal data to CSV