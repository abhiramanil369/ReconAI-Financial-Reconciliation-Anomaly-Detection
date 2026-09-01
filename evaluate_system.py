import json
import time
from pathlib import Path
import pandas as pd

from syndata_generation.models import Transaction
from benchmark_generation.benchmark_generator import generate_benchmark_dataset
from agents.orchestrator import MultiAgentOrchestrator


def load_or_generate_transactions():
    csv_path = Path("syndata_generation/data/transaction_data.csv")
    if not csv_path.exists():
        csv_path = Path("sample_dataset/transaction_data.csv")

    df = pd.read_csv(csv_path)

    transactions = []
    from datetime import datetime
    for _, row in df.iterrows():
        raw_date = row["Transaction_Date"]
        tx_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if isinstance(raw_date, str) else raw_date
        transactions.append(
            Transaction(
                transaction_id=str(row["Transaction_ID"]),
                customer_id=str(row["Customer_ID"]),
                account_type=row["Account_Type"],
                total_balance=float(row["Total_Balance"]),
                transaction_amount=float(row["Transaction_Amount"]),
                investment_amount=float(row["Investment_Amount"]),
                investment_type=row["Investment_Type"],
                transaction_date=tx_date
            )
        )
    return transactions


def run_evaluation():
    print("=" * 65)
    print("      AI FINANCE CONTROLLER — BENCHMARK EVALUATION ENGINE")
    print("=" * 65)

    # 1. Load transactions & generate benchmark dataset
    transactions = load_or_generate_transactions()
    fault_types = ["clean", "amount_mismatch", "date_mismatch", "duplicate_document", "missing_document", "wrong_customer", "broken_reference"]

    print(f"\n[1/4] Generating Benchmark Dataset for {len(transactions)} transactions across 7 case types...")
    benchmark_cases, ground_truth_list = generate_benchmark_dataset(transactions, fault_types)
    ground_truth = {item["case_id"]: item for item in ground_truth_list}

    # 2. Instantiate Orchestrator
    orchestrator = MultiAgentOrchestrator(audit_log_path="audit_trail.json")

    print(f"\n[2/4] Executing 5-Agent Pipeline on {len(benchmark_cases)} Benchmark Cases...\n")

    start_time = time.perf_counter()

    tp = tn = fp = fn = 0
    clean_matches = 0
    auto_resolved = 0
    escalated = 0
    honest_exceptions = []

    for idx, case in enumerate(benchmark_cases, 1):
        case_id = case["case_id"]
        is_clean_gt = ground_truth[case_id]["is_clean"]
        docs_dict = case["documents"]

        # Reconstruct document models
        doc_objs = []
        if docs_dict.get("transaction"):
            doc_objs.append(docs_dict["transaction"])
        if docs_dict.get("invoice"):
            doc_objs.append(docs_dict["invoice"])
        if docs_dict.get("payment"):
            doc_objs.append(docs_dict["payment"])
        if docs_dict.get("bank_transaction"):
            doc_objs.append(docs_dict["bank_transaction"])
        if docs_dict.get("duplicate_invoice"):
            doc_objs.append(docs_dict["duplicate_invoice"])

        # Execute Orchestrator
        result = orchestrator.process_case(case_id, doc_objs)
        predicted_status = result["status"]
        final_action = result["final_action"]

        # Track Financial Ops metrics
        if predicted_status == "MATCH":
            clean_matches += 1
        elif final_action in ["AUTO_RECONCILE", "CREATE_JOURNAL_ENTRY", "WAIT_FOR_SETTLEMENT"]:
            auto_resolved += 1
        else:
            escalated += 1
            honest_exceptions.append({
                "case_id": case_id,
                "transaction_id": result["transaction_id"],
                "fault_type": ground_truth[case_id]["fault_type"],
                "predicted_status": predicted_status,
                "final_action": final_action,
                "reason": result.get("compliance", {}).get("override_reason") or result.get("anomaly", {}).get("explanation", "Escalated for human audit")
            })

        # Confusion Matrix (Fault Detection Accuracy)
        predicted_fault = (predicted_status != "MATCH")
        actual_fault = (not is_clean_gt)

        if actual_fault and predicted_fault:
            tp += 1
        elif not actual_fault and not predicted_fault:
            tn += 1
        elif not actual_fault and predicted_fault:
            fp += 1
        elif actual_fault and not predicted_fault:
            fn += 1

        if idx % 100 == 0 or idx == len(benchmark_cases):
            print(f"   Processed {idx}/{len(benchmark_cases)} cases...")

    end_time = time.perf_counter()
    duration = end_time - start_time
    throughput = len(benchmark_cases) / duration if duration > 0 else 0

    # 3. Calculate Metrics
    total = len(benchmark_cases)
    accuracy = ((tp + tn) / total) * 100 if total > 0 else 0
    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
    fpr = (fp / (fp + tn)) * 100 if (fp + tn) > 0 else 0
    fnr = (fn / (fn + tp)) * 100 if (fn + tp) > 0 else 0

    match_rate = (clean_matches / total) * 100
    exception_total = total - clean_matches
    auto_recon_rate = (auto_resolved / exception_total * 100) if exception_total > 0 else 0
    escalation_rate = (escalated / exception_total * 100) if exception_total > 0 else 0

    # Save Audit Log & Outputs
    orchestrator.save_audit_log()

    with open("honest_exceptions.json", "w") as f:
        json.dump(honest_exceptions, f, indent=4, default=str)

    metrics_summary = {
        "total_records": total,
        "processing_time_seconds": round(duration, 2),
        "throughput_records_per_sec": round(throughput, 2),
        "overall_accuracy_pct": round(accuracy, 2),
        "precision_pct": round(precision, 2),
        "recall_pct": round(recall, 2),
        "f1_score": round(f1, 4),
        "false_positive_rate_pct": round(fpr, 2),
        "false_negative_rate_pct": round(fnr, 2),
        "match_rate_pct": round(match_rate, 2),
        "auto_reconciliation_rate_pct": round(auto_recon_rate, 2),
        "escalation_rate_pct": round(escalation_rate, 2)
    }

    with open("evaluation_metrics.json", "w") as f:
        json.dump(metrics_summary, f, indent=4)

    # 4. Print Dashboard Summary
    print("\n" + "=" * 65)
    print("             BENCHMARK EVALUATION RESULTS DASHBOARD")
    print("=" * 65)
    print(f"Total Batch Records Processed  : {total}")
    print(f"Total Execution Duration        : {duration:.2f} seconds")
    print(f"System Throughput              : {throughput:.2f} records/second")
    print("-" * 65)
    print("CLASSIFICATION & ACCURACY METRICS:")
    print(f"  • Overall Accuracy           : {accuracy:.2f}%")
    print(f"  • Precision                  : {precision:.2f}%")
    print(f"  • Recall (Sensitivity)       : {recall:.2f}%")
    print(f"  • F1-Score                   : {f1:.4f}")
    print(f"  • False Positive Rate (FPR)  : {fpr:.2f}%")
    print(f"  • False Negative Rate (FNR)  : {fnr:.2f}%  (Target: ~0%)")
    print("-" * 65)
    print("FINANCIAL OPERATIONS METRICS:")
    print(f"  • Match Rate (Clean Cases)   : {match_rate:.2f}%")
    print(f"  • Auto-Reconciliation Rate   : {auto_recon_rate:.2f}%")
    print(f"  • Escalation Rate (Honest)   : {escalation_rate:.2f}%")
    print("=" * 65)
    print("Artifacts generated:")
    print("  - Audit Trail Log        : audit_trail.json")
    print("  - Honest Exception List  : honest_exceptions.json")
    print("  - Benchmark Metrics      : evaluation_metrics.json")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_evaluation()