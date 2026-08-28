import pandas as pd

# INTERNAL_FILE = "internal.csv"
# EXTERNAL_FILE = "external.csv"

OUTPUT_FILE = "outputs/reconciliation_results.csv"
DATE = "Transaction_Date"

def load_data():
    internal = pd.read_csv("internal.csv")
    external = pd.read_csv("external.csv")

    return internal, external

def normalize_data(df):
    df = df.copy()

    df["Transaction_ID"] = (
        df["Transaction_ID"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    if "Customer_ID" in df.columns:
        df["Customer_ID"] = ( 
            df["Customer_ID"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    df["Transaction_Amount"] = pd.to_numeric(
        df["Transaction_Amount"],
        errors = "coerce"

    ).round(2)

    df["Transaction_Date"] = pd.to_datetime(
        df["Transaction_Date"],
        errors = "coerce"
    )

    return df


def find_duplicate(df):
    duplicate_mask = df.duplicated(
        subset = ["Transaction_ID"],
        keep = False
    )

    duplicates = df[duplicate_mask].copy()

    return duplicates

def reconcile(internal, external):
    merged = internal.merge(
        external,
        on = "Transaction_ID",
        how = "outer",
        indicator = True,
        suffixes = ("_internal", "_external")
    )

    return merged

def classify_row(row, internal_duplicates_ids, external_duplicates_ids):
    transaction_id = row["Transaction_ID"]

    # MISSING RECORDS

    if(row["_merge"] == "left_only"):
        return "MISSING_EXTERNAL"

    if(row["_merge"] == "right_only"):
            return "MISSING_INTERNAL"


    # DUPLICATE DETECTION

    if(
         transaction_id in internal_duplicates_ids
         or transaction_id in external_duplicates_ids
    ):
         return "DUPLICATE"

    # AMOUNT COMPARISON

    internal_amount = row["Transaction_Amount_internal"]
    external_amount = row["Transaction_Amount_external"]

    if pd.isna(internal_amount) or pd.isna(external_amount):
         return "AMOUNT_MISMATCH"

    if round(internal_amount ,2) != round(external_amount, 2):
         return "AMOUNT_MISMATCH"


    # DATE COMPARISON

    internal_date = row["Transaction_Date_internal"]
    external_date = row["Transaction_Date_external"]

    if pd.isna(internal_date) or pd.isna(external_date):
         return "DATE_MISMATCH"

    if internal_date != external_date:
         return "DATE_MISMATCH"


    return "MATCH"

def build_reconcile_result(internal, external):

     # Find duplicate Ids b4 merging

     internal_duplicate = find_duplicate(internal)
     external_duplicate = find_duplicate(external)

     internal_duplicate_ids = set(
          internal_duplicate["Transaction_ID"]
     )

     external_duplicate_ids = set(
           external_duplicate["Transaction_ID"]
     )

     # MERGE datasets

     merged = reconcile(internal, external)

     # Classify every row

     merged["status"] = merged.apply(
          lambda row : classify_row(
               row, internal_duplicate_ids,
               external_duplicate_ids
          ),
          axis = 1
     )


     # AMOUNT DIFFERENCE

     merged["amount_difference"] = (
          merged["Transaction_Amount_internal"]
          - merged["Transaction_Amount_external"]
     )

     merged["amount_difference"] = (
          merged["amount_difference"].round(2)
     )


     # DATE Difference

     merged["date_difference_days"] = (
        merged[f"{DATE}_internal"]
        - merged[f"{DATE}_external"]
     ).dt.days


     # RENAME merge indicator

     merged["record_location"] = merged["_merge"]

     merged.drop(
          columns = ["_merge"],
          inplace = True
     )

     return merged



# PRINT Summary

def print_summary(result):
     print("-------------------------RECONCILIATION SUMMARY-------------------------")

     print("\n")

     print("Total record : " , len(result))

     print("\n")

     print("Status distribution : ")
     print("\n")

     print(
          result["status"]
          .value_counts()
          .to_string()
     )

     print("\n")

     print("Match Rate : ")
     match_rate = (
          result["status"].eq("MATCH").mean() * 100
     )

     print(f"{match_rate:.2f}%")
     print("\n")

     print("Exception count : ")
     exception_count = (
        result["status"] != "MATCH"
     ).sum()

 
     print(exception_count)
     print("\n")




def main():

     print("Loading data")

     internal, external = load_data()

     print(
          f"Internal records : {len(internal)}"
     )

     print(
          f"External records : {len(external)}"
     )


     print("\nNormalizing data...")

     internal = normalize_data(internal)
     external = normalize_data(external)

     result = build_reconcile_result(internal, external)

     print("\nReconciliation completed")

     print_summary(result)

     # Create output dir
     
     import os
     os.makedirs(
          "outputs",
          exist_ok = True
     )


     result.to_csv(
          OUTPUT_FILE,
          index = False
     )

     print(
          f"\nResults saved to : {OUTPUT_FILE}\n"
     )


if __name__ == "__main__":
     main()