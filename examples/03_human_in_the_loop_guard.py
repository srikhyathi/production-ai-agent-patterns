"""
Pattern 03: Human-in-the-Loop (HITL) Guardrail
Prevents unapproved execution of sensitive operational actions.
"""

import uuid
from typing import Dict, Any

class ApprovalGate:
    def __init__(self):
        self._pending: Dict[str, dict] = {}

    def request_approval(self, action: str, payload: dict) -> str:
        ticket_id = str(uuid.uuid4())[:8]
        self._pending[ticket_id] = {
            "action": action,
            "payload": payload,
            "status": "PENDING"
        }
        print(f"[SECURITY] Action '{action}' intercepted. Approval Ticket: {ticket_id}")
        return ticket_id

    def approve_and_execute(self, ticket_id: str) -> dict:
        if ticket_id not in self._pending:
            return {"error": "Invalid ticket ID"}
        record = self._pending[ticket_id]
        record["status"] = "APPROVED"
        print(f"[SECURITY] Ticket {ticket_id} approved. Executing '{record['action']}'...")
        return {"status": "SUCCESS", "executed": record["action"]}

if __name__ == "__main__":
    gate = ApprovalGate()
    t_id = gate.request_approval("drop_database_partition", {"partition": "audit_2025_q1"})
    res = gate.approve_and_execute(t_id)
    print(f"[Result] {res}")
