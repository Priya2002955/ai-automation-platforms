import pandas as pd
from datetime import datetime
import uuid


decisions_df = pd.read_csv("pos_payments/data/payment_decisions.csv")

agent_actions = []
audit_logs = []

for _, row in decisions_df.iterrows():
    transaction_id = row["transaction_id"]
    risk_type = row["risk_type"]
    decision = row["decision"]
    priority = row["priority"]
    approval_status = row["approval_status"]

    action_taken = "No action"
    action_status = "Skipped"

    if decision == "Retry Payment":
        action_taken = "Trigger payment retry workflow"
        action_status = "Completed"

    elif decision == "Investigate":
        action_taken = "Create investigation ticket"
        action_status = "Pending Human Review"

    elif decision == "Manager Approval":
        action_taken = "Route transaction to manager approval queue"
        action_status = "Pending Approval"

    elif decision == "Review Refund":
        action_taken = "Route refund to compliance review"
        action_status = "Pending Compliance Review"

    action_id = f"ACT-{uuid.uuid4().hex[:8]}"
    timestamp = datetime.now().isoformat()

    agent_actions.append({
        "action_id": action_id,
        "transaction_id": transaction_id,
        "risk_type": risk_type,
        "decision": decision,
        "priority": priority,
        "action_taken": action_taken,
        "action_status": action_status,
        "agent_name": "PaymentAutomationAgent",
        "timestamp": timestamp
    })

    audit_logs.append({
        "audit_id": f"AUD-{uuid.uuid4().hex[:8]}",
        "action_id": action_id,
        "transaction_id": transaction_id,
        "agent_name": "PaymentAutomationAgent",
        "decision": decision,
        "action_taken": action_taken,
        "approval_status": approval_status,
        "before_state": risk_type,
        "after_state": action_status,
        "timestamp": timestamp
    })


agent_actions_df = pd.DataFrame(agent_actions)
audit_logs_df = pd.DataFrame(audit_logs)

agent_actions_df.to_csv("pos_payments/data/payment_agent_actions.csv", index=False)
audit_logs_df.to_csv("pos_payments/data/audit_log.csv", index=False)

print("Payment agent actions and audit logs generated successfully!")
print(agent_actions_df.head())