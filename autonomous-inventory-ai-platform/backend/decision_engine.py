import pandas as pd


def load_data():
    risk = pd.read_csv("data/risk_alerts.csv")
    forecast = pd.read_csv("data/demand_forecast.csv")

    df = risk.merge(forecast, on=["store_id", "product"], how="left")

    return df


def make_decisions():
    df = load_data()

    decisions = []

    for _, row in df.iterrows():
        risk_type = row["risk_type"]
        forecast_7 = row["forecast_7_days"]
        current_stock = row["current_stock"]
        max_stock = 300  # fallback if needed

        decision = "No action"
        priority = "Low"
        recommended_qty = 0

        # 🔥 Core logic
        if risk_type == "Stockout Risk":
            decision = "Immediate Reorder"
            priority = "High"
            recommended_qty = max(forecast_7 - current_stock, 0)

        elif risk_type == "Low Stock":
            decision = "Planned Reorder"
            priority = "Medium"
            recommended_qty = max(forecast_7 - current_stock, 0)

        elif risk_type == "Overstock":
            decision = "Hold / Reduce Orders"
            priority = "Low"
            recommended_qty = 0

        decisions.append({
            "store_id": row["store_id"],
            "product": row["product"],
            "risk_type": risk_type,
            "forecast_7_days": forecast_7,
            "current_stock": current_stock,
            "decision": decision,
            "priority": priority,
            "recommended_quantity": round(recommended_qty)
        })

    decision_df = pd.DataFrame(decisions)
    decision_df.to_csv("data/decisions.csv", index=False)

    print("Decisions generated successfully!")
    print(decision_df.head(10))


if __name__ == "__main__":
    make_decisions()