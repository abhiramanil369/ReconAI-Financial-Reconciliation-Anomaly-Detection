import pandas as pd

from reconciliation_engine import(
    normalize_data,
     build_reconcile_result
)

def make_internal(data):
    return pd.DataFrame(data)

def make_external(data):
    return pd.DataFrame(data)



# TEST 1 - MATCH

def test_exact_match():

    internal = make_internal({
        "Transaction_ID" : ["TXTN001"],
        "Customer_ID" : ["C001"],
        "Transaction_Amount" : [10000],
        "Transaction_Date" : ["2026-08-20"]
    })

    external = make_external({
        "Transaction_ID" : ["TXTN001"],
        "Customer_ID" : ["C001"],
        "Transaction_Amount" : [10000],
        "Transaction_Date" : ["2026-08-20"]
    })


    internal = normalize_data(internal)
    external = normalize_data(external)

    result = build_reconcile_result(
        internal, external
    )

    assert result.iloc[0]["status"] == "MATCH"


# TEST 2 - Amount Mismatch

def test_amount_mismatch():

    internal = make_internal({
       "Transaction_ID" : ["TXTN002"],
       "Customer_ID" : ["C001"],
       "Transaction_Amount" : [10000],
       "Transaction_Date" : ["2026-08-20"] 
    })

    external = make_external({
       "Transaction_ID" : ["TXTN002"],
       "Customer_ID" : ["C001"],
       "Transaction_Amount" : [9500],
       "Transaction_Date" : ["2026-08-20"] 
    })

    internal = normalize_data(internal)
    external = normalize_data(external)


    result = build_reconcile_result(internal , external)

    assert result.iloc[0]["status"] == "AMOUNT_MISMATCH"

    assert(
        result.iloc[0]["amount_difference"] == 500
    )



# TEST 3 - Date Mistmatch

def test_date_mismatch():

    internal = make_internal({
       "Transaction_ID" : ["TXTN003"],
       "Customer_ID" : ["C001"],
       "Transaction_Amount" : [10000],
       "Transaction_Date" : ["2026-08-20"] 
    })

    external = make_external({
       "Transaction_ID" : ["TXTN003"],
       "Customer_ID" : ["C001"],
       "Transaction_Amount" : [10000],
       "Transaction_Date" : ["2026-08-21"] 
    })

    internal = normalize_data(internal)
    external = normalize_data(external)

    result = build_reconcile_result(internal, external)

    assert result.iloc[0]["status"] == "DATE_MISMATCH"


# Test 4 - Missing External

def test_missing_external():

    internal = make_internal({
       "Transaction_ID" : ["TXTN004"],
       "Customer_ID" : ["C001"],
       "Transaction_Amount" : [5000],
       "Transaction_Date" : ["2026-08-20"] 
    })

    external = make_external({
       "Transaction_ID" : [],
       "Customer_ID" : [],
       "Transaction_Amount" : [],
       "Transaction_Date" : [] 
    })

    internal = normalize_data(internal)

    external = normalize_data(external)

    result = build_reconcile_result(internal, external)

    assert (
        result.iloc[0]["status"] 
        == "MISSING_EXTERNAL"
    )

# Test 5 - Misssing Internal

def test_missing_internal():

    internal = pd.DataFrame(
        columns=[
            "Transaction_ID",
            "Customer_ID",
            "Transaction_Amount",
            "Transaction_Date"
        ]
    )

    external = pd.DataFrame({
        "Transaction_ID": ["TXN005"],
        "Customer_ID": ["C001"],
        "Transaction_Amount": [5000],
        "Transaction_Date": ["2026-08-20"]
    })

    internal = normalize_data(internal)
    external = normalize_data(external)

    result = build_reconcile_result(
        internal,
        external
    )

    assert (
        result.iloc[0]["status"]
        == "MISSING_INTERNAL"
    )

# TEST 5 -- DUPLICATE

def test_duplicate():
    internal = make_internal({
        "Transaction_ID" :[
            "TXN006",
            "TXN006"
        ],
        "Customer_ID":[
            "C001",
            "C001"
        ],
        "Transaction_Amount" :[
            5000,
            5000
        ],
        "Transaction_Date" :[
            "2026-08-20",
            "2026-08-20"
        ]
    })

    external = make_external({
        "Transaction_ID" : ["TXN006"],
        "Customer_ID" : ["C001"],
        "Transaction_Amount" : [5000],
        "Transaction_Date" : ["2026-08-20"]
    })

    internal = normalize_data(internal)
    external = normalize_data(external)

    result = build_reconcile_result(
        internal,
        external
    )

    assert(
        result["status"]
        .eq("DUPLICATE")
        .all()
    )