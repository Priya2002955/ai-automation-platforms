import pandas as pd


def load_transactions():
    return pd.read_csv("pos_payments/data/transactions.csv")


def detect_payment_risks():
    df = load_transactions()

    risk_alerts = []

    duplicate_counts = df["transaction_id"].value_counts()

    for _, row in df.iterrows():
        risk_type = "Normal"
        severity = "Low"
        risk_score = 0
        risk_reason = "No risk detected"

        transaction_id = row["transaction_id"]
        amount = row["amount"]
        status = row["status"]
        event_type = row["event_type"]

        if status == "FAILED":
            risk_type = "Failed Payment"
            severity = "Medium"
            risk_score = 60
            risk_reason = "Payment transaction failed and may require retry or customer follow-up."

        if amount >= 400:
            risk_type = "High-Value Transaction"
            severity = "High"
            risk_score = 75
            risk_reason = "Transaction amount exceeds high-value threshold and may require review."

        if duplicate_counts[transaction_id] > 1:
            risk_type = "Duplicate Transaction"
            severity = "High"
            risk_score = 85
            risk_reason = "Same transaction ID appears multiple times and may indicate duplicate charge."

        if event_type == "REFUND_INITIATED":
            risk_type = "Refund Event"
            severity = "Medium"
            risk_score = 65
            risk_reason = "Refund event detected and should be reviewed for policy compliance."

        risk_alerts.append({
            "event_id": row["event_id"],
            "transaction_id": transaction_id,
            "store_id": row["store_id"],
            "customer_id": row["customer_id"],
            "amount": amount,
            "payment_method": row["payment_method"],
            "status": status,
            "event_type": event_type,
            "risk_type": risk_type,
            "severity": severity,
            "risk_score": risk_score,
            "risk_reason": risk_reason
        })

    risk_df = pd.DataFrame(risk_alerts)
    risk_df.to_csv("pos_payments/data/payment_risk_alerts.csv", index=False)

    print("Payment risk alerts generated successfully!")
    print(risk_df.head(10))


if __name__ == "__main__":
    detect_payment_risks()