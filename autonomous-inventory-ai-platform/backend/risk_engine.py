import pandas as pd


def load_data():
    inventory = pd.read_csv("data/inventory.csv")
    rules = pd.read_csv("data/reorder_rules.csv")
    suppliers = pd.read_csv("data/suppliers.csv")

    return inventory, rules, suppliers


def calculate_risk():
    inventory, rules, suppliers = load_data()

    df = inventory.merge(rules, on="product", how="left")
    df = df.merge(suppliers, on="product", how="left")

    alerts = []

    for _, row in df.iterrows():
        current_stock = row["current_stock"]
        daily_usage = row["daily_usage"]
        threshold = row["reorder_threshold"]
        max_stock = row["max_stock"]
        lead_time = row["lead_time_days"]

        days_until_stockout = round(current_stock / daily_usage, 2)

        risk_type = "Normal"
        recommended_action = "No action needed"
        reorder_quantity = 0

        if current_stock <= threshold:
            risk_type = "Low Stock"
            reorder_quantity = max_stock - current_stock
            recommended_action = f"Reorder {reorder_quantity} units"

        if days_until_stockout <= lead_time:
            risk_type = "Stockout Risk"
            reorder_quantity = max_stock - current_stock
            recommended_action = f"Urgent reorder {reorder_quantity} units"

        if current_stock > max_stock:
            risk_type = "Overstock"
            recommended_action = "Pause reorder and review demand"

        alerts.append({
            "store_id": row["store_id"],
            "product": row["product"],
            "current_stock": current_stock,
            "daily_usage": daily_usage,
            "days_until_stockout": days_until_stockout,
            "supplier_name": row["supplier_name"],
            "lead_time_days": lead_time,
            "risk_type": risk_type,
            "recommended_action": recommended_action,
            "reorder_quantity": reorder_quantity
        })

    alerts_df = pd.DataFrame(alerts)
    alerts_df.to_csv("data/risk_alerts.csv", index=False)

    print("Risk alerts generated successfully!")
    print(alerts_df.head(10))


if __name__ == "__main__":
    calculate_risk()