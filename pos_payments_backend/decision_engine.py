import pandas as pd


def load_risk_data():
    return pd.read_csv("pos_payments/data/payment_risk_alerts.csv")


def generate_decisions():
    df = load_risk_data()

    decisions = []
    approval_queue = []

    for _, row in df.iterrows():
        risk_type = row["risk_type"]
        amount = row["amount"]

        decision = "No Action"
        priority = "Low"
        human_in_loop_required = False
        approval_status = "Auto-Approved"
        decision_reason = ""

        # 🔥 Decision logic

        if risk_type == "Failed Payment":
            decision = "Retry Payment"
            priority = "Medium"
            decision_reason = "Payment failed and needs retry or customer follow-up."

        elif risk_type == "Duplicate Transaction":
            decision = "Flag for Investigation"
            priority = "High"
            human_in_loop_required = True
            approval_status = "Pending Approval"
            decision_reason = "Duplicate transaction detected and requires manual review."

        elif risk_type == "High-Value Transaction":
            decision = "Require Manager Approval"
            priority = "High"
            human_in_loop_required = True
            approval_status = "Pending Approval"
            decision_reason = "High-value transaction requires managerial validation."

        elif risk_type == "Refund Event":
            decision = "Compliance Review"
            priority = "Medium"
            human_in_loop_required = True
            approval_status = "Pending Approval"
            decision_reason = "Refund must be verified against policy rules."

        decisions.append({
            "transaction_id": row["transaction_id"],
            "store_id": row["store_id"],
            "amount": amount,
            "risk_type": risk_type,
            "decision": decision,
            "priority": priority,
            "human_in_loop_required": human_in_loop_required,
            "approval_status": approval_status,
            "decision_reason": decision_reason
        })

        # 🔥 Approval queue (HITL)

        if human_in_loop_required:
            approval_queue.append({
                "transaction_id": row["transaction_id"],
                "store_id": row["store_id"],
                "amount": amount,
                "reason": decision_reason,
                "status": "Pending",
                "reviewed_by": "Not Assigned"
            })

    decision_df = pd.DataFrame(decisions)
    approval_df = pd.DataFrame(approval_queue)

    decision_df.to_csv("pos_payments/data/payment_decisions.csv", index=False)
    approval_df.to_csv("pos_payments/data/approval_queue.csv", index=False)

    print("Decisions generated successfully!")
    print(decision_df.head())


if __name__ == "__main__":
    generate_decisions()