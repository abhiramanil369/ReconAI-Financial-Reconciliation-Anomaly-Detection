from benchmark_generation.fault_injection import(
    inject_broken_references,
    inject_wrong_customer,
    inject_missing_document,
    inject_duplicate_documents,
    inject_date_mismatch,
    inject_amount_mismatch
)

def test_amount_mismatch(clean_documents):
    faulty_documents = inject_amount_mismatch(
        clean_documents
    )

    assert (
        faulty_documents["invoice"].amount != 
        faulty_documents["transaction"].transaction_amount
    )

def test_date_mismatch(clean_documents):

    faulty_documents = inject_date_mismatch(
        clean_documents
    )

    assert (
        faulty_documents["payments"].payments_date
        != 
        faulty_documents["transaction"].transaction_date
    )

def test_duplicate_document(clean_documents):

    faulty_documents = inject_duplicate_documents(
        clean_documents
    )

    assert (
        "duplicate_invoice"
        in faulty_documents
    )

    assert (
        faulty_documents["duplicates_invoices"].invoice_id
        == 
        faulty_documents["invoice"].invoice_id
    )



def test_missing_document(clean_documents):

    faulty_documents = inject_missing_document(
        clean_documents
    )

    assert (
        faulty_documents["invoice"].customer_id
        !=
        faulty_documents["transaction"].customer_id
    )

def test_broken_reference(clean_documents):

    faulty_documents = inject_broken_references(clean_documents)

    assert (
        faulty_documents["invoice"].transaction_id
        !=
        faulty_documents["transaction"].transaction_id
    )

    