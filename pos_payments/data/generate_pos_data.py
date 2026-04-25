import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

payment_methods = ["CARD", "CASH", "MOBILE_WALLET", "GIFT_CARD"]
statuses = ["SUCCESS", "FAILED", "REFUNDED"]
event_types = ["PAYMENT_SUCCESS", "PAYMENT_FAILED", "REFUND_INITIATED"]

transactions = []

for i in range(1, 501):
    status = random.choices(
        statuses,
        weights=[80, 15, 5],
        k=1
    )[0]

    if status == "SUCCESS":
        event_type = "PAYMENT_SUCCESS"
    elif status == "FAILED":
        event_type = "PAYMENT_FAILED"
    else:
        event_type = "REFUND_INITIATED"

    transactions.append({
        "event_id": f"EVT-{1000+i}",
        "transaction_id": f"TXN-{1000+i}",
        "store_id": random.randint(1, 10),
        "customer_id": f"CUST-{random.randint(100, 999)}",
        "amount": round(random.uniform(5, 600), 2),
        "payment_method": random.choice(payment_methods),
        "status": status,
        "event_type": event_type,
        "source_system": "POS_SYSTEM",
        "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 5000))
    })

# Add intentional duplicate transactions
for _ in range(10):
    duplicate = random.choice(transactions).copy()
    duplicate["event_id"] = f"EVT-DUP-{random.randint(1000, 9999)}"
    transactions.append(duplicate)

df = pd.DataFrame(transactions)
df.to_csv("pos_payments/data/transactions.csv", index=False)

print("POS payment transaction data generated successfully!")
print(df.head())