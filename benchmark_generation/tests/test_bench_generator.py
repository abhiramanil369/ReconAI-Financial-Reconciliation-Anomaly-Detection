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
        documents["payment"].invoice_id
        == 
        documents["invoice"].invoice_id
    )

    assert (
        documents["payment"].transaction_id
        ==
        documents["transaction"].transaction_id
    )

    assert (
        documents["payment"].amount
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

    assert (
        ground_truth["label"] == "MATCH"
    )

    assert (
        ground_truth["is_clean"] is True
    )

    assert (
        ground_truth["fault_type"] is None
    )


def test_amount_mismatch_case(
        sample_transaction
):
    documents, ground_truth = (
        create_benchmark_case(
            transaction = sample_transaction,
            case_id = "CASE-002",
            fault_type="amount_mismatch"
        )
    )

    assert (
        documents["invoice"].amount 
        != 
        documents["transaction"].transaction_amount
    )

    assert (
        ground_truth["label"] == "AMOUNT_MISMATCH"
    )

def test_generate_benchmark_dataset(
        sample_transaction
):
    transactions = [
        sample_transaction,
        sample_transaction
    ]
    fault_types = [
        "clean",
        "amount_mismatch"
    ]

    cases, labels = (
        generate_benchmark_dataset(
            transactions,
            fault_types
        )
    )

    assert len(cases) == 2

    assert len(labels) == 2

    assert (
        labels[0]["label"] == "MATCH"
    )

    assert (
        labels[1]["label"] == "AMOUNT_MISMATCH"
    )