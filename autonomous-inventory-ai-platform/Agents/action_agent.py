import pandas as pd


def load_decisions():
    return pd.read_csv("data/decisions.csv")


def run_agent():
    df = load_decisions()

    actions = []

    for _, row in df.iterrows():
        decision = row["decision"]
        qty = row["recommended_quantity"]
        product = row["product"]
        store = row["store_id"]

        action = "No action"
        approval = "Not required"

        # 🔥 Agent logic
        if decision == "Immediate Reorder":
            action = f"Create urgent purchase order for {qty} units of {product}"
            if qty > 200:
                approval = "Manager approval required"

        elif decision == "Planned Reorder":
            action = f"Schedule reorder for {qty} units of {product}"
            if qty > 200:
                approval = "Manager approval required"

        elif decision == "Hold / Reduce Orders":
            action = "Pause reorder and review demand"

        actions.append({
            "store_id": store,
            "product": product,
            "decision": decision,
            "action": action,
            "approval_status": approval
        })

    actions_df = pd.DataFrame(actions)
    actions_df.to_csv("data/agent_actions.csv", index=False)

    print("Agent actions generated successfully!")
    print(actions_df.head(10))


if __name__ == "__main__":
    run_agent()