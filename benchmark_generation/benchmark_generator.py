from fault_injection import(
    inject_amount_mismatch,
    inject_date_mismatch,
    inject_missing_document,
    inject_wrong_customer,
    inject_duplicate_documents,
    inject_broken_references
)

from ground_truth import create_ground_truth

from syndata_generation.generators import(
    generate_invoice,
    generate_bank_transaction,
    generate_payment
)

FAULT_INJECTIONS ={
    "amount_mismatch" : inject_amount_mismatch,
    "date_mismatch" : inject_date_mismatch,
    "duplicate_document" : inject_duplicate_documents,
    "missing_document" : inject_missing_document,
    "wrong_customer" : inject_wrong_customer,
    "broken_reference" : inject_broken_references
}


def create_clean_case(transaction):
    """
        Generate a complete and consistent set of financial documents
    """

    invoice = generate_invoice(transaction)

    payment = generate_payment(transaction, invoice)

    bank_transaction = generate_bank_transaction(transaction)


    return {
        "transaction": transaction,
        "invoice" : invoice,
        "payment" : payment,
        "bank_transaction" : bank_transaction
    }