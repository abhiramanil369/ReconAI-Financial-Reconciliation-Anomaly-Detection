from copy import deepcopy
from datetime import timedelta

def inject_amount_mismatch(documents):
    """
    Change the invoice amount so it does not match
    the original transaction amount.
    """

    faulty_documents = deepcopy(documents)

    original_amount = (
        faulty_documents["transaction"]
        .transaction_amount
    )

    faulty_documents["invoice"].amount = (
        original_amount + 100
    )

    return faulty_documents


def inject_date_mismatch(documents):
    """
    Change the payment date so it does not much
    the original transaction date.
    """

    faulty_documents = deepcopy(documents)

    original_date = (
        faulty_documents["transaction"]
        .transaction_date
    )

    faulty_documents["payments"].payment_date = (
        original_date + timedelta(days=1)
    )

    return faulty_documents

def inject_duplicate_documents(documents):
    """
    Create a duplicates invoice documents
    """

    faulty_documents = deepcopy(documents)

    duplicate_invoice = deepcopy(
        faulty_documents["invoice"]
    )

    faulty_documents["duplicate_invoice"] = (
        duplicate_invoice
    )

    return faulty_documents


def inject_missing_document(documents):
    """
    Remove the payment document
    """

    faulty_documents = deepcopy(documents)

    faulty_documents["payments"] = None

    return faulty_documents


def inject_wrong_customer(documents):
    """
        Change the customer ID in the invoice
    """

    faulty_documents = deepcopy(documents)

    original_customer = (
        faulty_documents["transaction"].
        customer_id
    )

    faulty_documents["invoice"].customer_id  = (
        f"WRONG{original_customer}"
    )

    return faulty_documents

def inject_broken_references(documents):
    """
        Break the transactio reference
        inside the invoice
    """

    faulty_documents = deepcopy(documents)

    faulty_documents["invoice"].transaction_id = (
        "INVALID-TXN-REFERENCE"
    )

    return faulty_documents


