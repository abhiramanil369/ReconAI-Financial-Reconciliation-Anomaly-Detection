import json
from datetime import datetime
from pathlib import Path
from typing import Any

class AuditLogger:
    """
        Immutable Audit Logger for financial Reconciliation Operations.
        Logs every case step, agent decision, confidence and final action.
    """

    def __init__(self, output_file: str | Path = "audit_trail.json"):
        self.output_file = Path(output_file)
        self.logs: list[dict[str, Any]] = []

    def log_entry(
            self,
            case_id: str,
            transaction_id: str,
            step_name: str,
            agent_name: str,
            decision: str,
            reason: str ,
            confidence: float,
            evidence_summary: dict[str, Any] | None = None,
            final_action: str | None = None
    ):

        entry = {
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "transaction_id": transaction_id,
            "step_name": step_name,
            "agent_name": agent_name,
            "decision": decision,
            "reason": reason,
            "confidence": confidence,
            "evidence_summary": evidence_summary or {},
            "final_action": final_action or decision
        }

        self.logs.append(entry)


    def save(self):
        with open(self.output_file, "w") as f:
            json.dump(self.logs, f, indent=4, default=str)

        print(f"Audit log saved to {self.output_file.resolve()}")
        