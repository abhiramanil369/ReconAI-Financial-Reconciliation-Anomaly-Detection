from benchmark_generation.benchmark_generator import(
    create_clean_case,
    create_benchmark_case,
    generate_benchmark_dataset
)

def test_create_clean(sample_transaction):

    documents = create_clean_case(
        sample_transaction
    )

    assert (
        documents["invoice"].transaction_id
        ==
        documents["transaction"].transaction_id
    )

    assert (
        documents["invoice"].customer_id
        ==
        documents["transaction"].customer_id
    )

    assert (
        documents["invoice"].amount
        ==
        documents["transaction"].transaction_amount
    )

    assert (
        documents["payments"].invoice_id
        == 
        documents["invoice"].invoice_id
    )

    assert (
        documents["payments"].transaction_id
        ==
        documents["transaction"].transaction_id
    )

    assert (
        documents["payments"].amount
        ==
        documents["transaction"].transaction_amount
    )

    assert (
        documents["bank_transaction"].transaction_id
        ==
        documents["transaction"].transaction_id
    )

    assert (
        documents["bank_transaction"].amount
        ==
        documents["transaction"].transaction_amount
    )

def test_clean_benchmark_case(
        sample_transaction
):
    documents, ground_truth = (
        create_benchmark_case(
            transaction = sample_transaction,
            case_id = "CASE-001",
            fault_type="clean"
        )
    )