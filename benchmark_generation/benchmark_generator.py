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

def create_benchmark_case(
        transaction, 
        case_id,
        fault_type ="clean"
):
    """
        Create either a clean case or case containining an injected contradiction.
    """

    
    documents = create_benchmark_case(transaction)

    if fault_type == "clean":
        ground_truth = create_ground_truth(case_id, "clean")

        return documents, ground_truth

    injector = FAULT_INJECTIONS[fault_type]

    faulty_documents = injector(documents)

    ground_truth = create_ground_truth(case_id, fault_type)

    return faulty_documents, ground_truth


def generate_benchmark_dataset(
        transactions,
        fault_types
):
    """
        Generate benchmark cases from multiple transactions.
        Fault types are assigned cyclically.
    """

    benchmark_cases = []

    ground_truth_labels = []


    for index, transaction in enumerate(
        transactions
    ):
        case_id = (
            f"CASE{index + 1:04d}"
        )

        fault_type = fault_types[
            index % len(fault_types)
        ]

        documents, ground_truth = (
            create_benchmark_case(
                transaction = transaction,
                case_id = case_id,
                fault_type = fault_type
            )
        )

        benchmark_cases.append({
            "case_id" : case_id,
            "documents" : documents
        })

        ground_truth_labels.append(
            ground_truth
        )

        return (
            benchmark_cases,
            ground_truth_labels
        )


