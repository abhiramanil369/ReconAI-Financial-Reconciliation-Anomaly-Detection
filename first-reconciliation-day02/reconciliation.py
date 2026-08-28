import pandas as pd
from normalization import normalize_data

def create_match_key(df):
    df = df.copy()

    df["match_key"] = (
        df["Customer_ID"].astype(str)
        + "|"
        + df["Transaction_Date"].dt.strftime("%Y-%m-%d")
        + "|"
        + df["Transaction_Amount"].round(2).astype(str)
    )

    return df


def reconcile(internal, external):

    # Normalize
    internal = normalize_data(internal)
    external = normalize_data(external)

    # Create matching keys
    internal = create_match_key(internal)
    external = create_match_key(external)
    
    # Find duplicates
    internal_duplicates = internal[
        internal["match_key"].duplicated(keep = False)
    ]

    external_duplicates = external[
        external["match_key"].duplicated(keep = False)
    ]


    # Compare keys

    internal_keys = set(internal["match_key"])
    external_keys = set(external["match_key"])

    matched_keys = internal_keys & external_keys

    missing_external = internal_keys - external_keys

    missing_internal = external_keys - internal_keys

    results = []

    for key in matched_keys:
        results.append({
            "match_key" : key,
            "status" : "MATCH"
        })

    for key in missing_external:
            results.append({
                "match_key" : key,
                "status" : "Exception - Missing in External"
            })

    for key in missing_internal:
                results.append({
                    "match_key" : key,
                    "status" : "Exception - Missing in Internal"
                })


    results = pd.DataFrame(results)

    return results, internal_duplicates, external_duplicates