# Benchmark Dataset Generation and Fault Injection

## Overview

This module generates a reproducible benchmark dataset for evaluating the financial reconciliation and exception-classification system.

The benchmark contains both clean financial document cases and intentionally corrupted cases. Each corrupted case contains a controlled contradiction along with a corresponding ground-truth label.

The purpose is to create known test scenarios that can later be used to evaluate whether a reconciliation engine or AI system can correctly identify and classify financial inconsistencies.

---

## Architecture

```text
Ground Truth Transaction
        │
        ▼
Synthetic Document Generation
        │
        ├── Invoice
        ├── Payment
        └── Bank Transaction
        │
        ▼
Create Clean Financial Case
        │
        ├──────────────► Clean Case
        │                     │
        │                     ▼
        │                   MATCH
        │
        ▼
Fault Injection
        │
        ├── Amount Mismatch
        ├── Date Mismatch
        ├── Duplicate Document
        ├── Missing Document
        ├── Wrong Customer
        └── Broken Reference
        │
        ▼
Ground Truth Generation
        │
        ▼
Benchmark Dataset
```

---

## Project Structure

```text
benchmark_generation/
│
├── __init__.py
├── benchmark_generator.py
├── fault_injection.py
├── ground_truth.py
├── main.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_bench_generator.py
    └── test_fault_injection.py
```

---

# Components

## `benchmark_generator.py`

This is the main benchmark generation module.

It performs three major tasks:

1. Creates clean financial document cases.
2. Applies controlled faults to create contradictory cases.
3. Generates corresponding ground-truth labels.

### Clean Case Generation

A ground-truth transaction is converted into multiple related financial documents:

```text
Transaction
    │
    ├── Invoice
    ├── Payment
    └── Bank Transaction
```

In a clean case, all references, customer IDs, amounts, and dates remain consistent.

Example:

```text
Transaction Amount: 10,000
Invoice Amount:     10,000
Payment Amount:     10,000
Bank Amount:        10,000

Expected Label: MATCH
```

---

## `fault_injection.py`

This module deliberately introduces controlled contradictions into otherwise valid financial documents.

The following fault types are supported:

### Amount Mismatch

The invoice amount is modified so that it no longer matches the original transaction amount.

```text
Transaction Amount: 10,000
Invoice Amount:      10,100

Expected Result: AMOUNT_MISMATCH
```

### Date Mismatch

The payment date is changed so that it differs from the original transaction date.

```text
Transaction Date: August 25
Payment Date:     August 26

Expected Result: DATE_MISMATCH
```

### Duplicate Document

A duplicate invoice is created with the same invoice information.

```text
Invoice 1: INV-TXN001
Invoice 2: INV-TXN001

Expected Result: DUPLICATE_DOCUMENT
```

### Missing Document

A required financial document is removed.

```text
Transaction ✓
Invoice ✓
Payment ✗ Missing
Bank Transaction ✓

Expected Result: MISSING_DOCUMENT
```

### Wrong Customer

The customer ID in a financial document is changed.

```text
Transaction Customer: C102
Invoice Customer:     WRONG-C102

Expected Result: WRONG_CUSTOMER
```

### Broken Reference

A document's transaction reference is intentionally replaced with an invalid value.

```text
Transaction ID: TXN001
Invoice Transaction ID: INVALID-TXN-REFERENCE

Expected Result: BROKEN_REFERENCE
```

---

## `ground_truth.py`

This module creates the expected labels for each benchmark case.

Example clean case:

```python
{
    "case_id": "CASE-0001",
    "label": "MATCH",
    "is_clean": True,
    "fault_type": None
}
```

Example faulty case:

```python
{
    "case_id": "CASE-0002",
    "label": "AMOUNT_MISMATCH",
    "is_clean": False,
    "fault_type": "amount_mismatch"
}
```

The ground truth acts as the answer key for evaluating the system.

---

# Benchmark Generation Flow

The benchmark generator follows this process:

```text
1. Receive a ground-truth transaction
                │
                ▼
2. Generate invoice, payment, and bank transaction
                │
                ▼
3. Create a clean financial case
                │
                ▼
4. Select a fault type
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
     Clean Case      Inject Fault
        │                │
        ▼                ▼
      MATCH       Exception Type
        │                │
        └───────┬────────┘
                ▼
       Generate Ground Truth
                │
                ▼
        Benchmark Dataset
```

---

# Benchmark Dataset

The generator can process multiple transactions and assign fault types cyclically.

Example:

```python
transactions = [
    transaction_1,
    transaction_2,
    transaction_3
]

fault_types = [
    "clean",
    "amount_mismatch",
    "date_mismatch"
]
```

Generated output:

```text
CASE-0001
Fault Type: clean
Ground Truth: MATCH

CASE-0002
Fault Type: amount_mismatch
Ground Truth: AMOUNT_MISMATCH

CASE-0003
Fault Type: date_mismatch
Ground Truth: DATE_MISMATCH
```

The generated benchmark cases and ground-truth labels are returned separately.

This allows the documents to be provided to a reconciliation or AI system while keeping the expected answers separate for evaluation.

---

# Testing

The project includes automated tests for benchmark generation and fault injection.

The tests verify:

* Clean document generation.
* Clean benchmark case generation.
* Amount mismatch generation.
* Date mismatch generation.
* Duplicate document generation.
* Missing document generation.
* Broken reference generation.
* Benchmark dataset generation.

Run the tests from the project root:

```bash
pytest benchmark_generation/tests -v
```

All implemented test cases are currently passing successfully.

---

# Learning Concepts

This module helped explore the following concepts:

* Ground truth
* Benchmark dataset design
* Positive and negative test cases
* Synthetic dataset generation
* Controlled fault injection
* Edge cases
* Reproducibility
* Automated testing
* Financial document relationships
* Referential integrity
* Exception classification

---

# Future Improvements

The next steps for this module include:

* Adding automated testing for the wrong customer fault type.
* Generating a larger benchmark dataset from the available financial transaction dataset.
* Creating balanced distributions of clean and contradictory cases.
* Adding more realistic fault scenarios.
* Saving benchmark cases to JSON or CSV files.
* Keeping ground-truth labels hidden from the evaluation system.
* Splitting data into training, validation, and test sets.
* Connecting the benchmark dataset to the reconciliation and exception-classification engine.
* Using the hidden ground truth to measure system performance using metrics such as accuracy, precision, recall, and F1-score.

---

## Outcome

A reproducible benchmark generation pipeline was successfully built to create clean and contradictory financial document cases. The system can generate related financial documents from ground-truth transactions, deliberately inject controlled inconsistencies, assign expected ground-truth labels, and produce benchmark cases for evaluating the accuracy and robustness of the financial reconciliation and exception-classification system.
