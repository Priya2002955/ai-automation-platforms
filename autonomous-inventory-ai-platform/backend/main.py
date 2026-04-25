from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="Autonomous Inventory Optimization Platform",
    description="AI-powered inventory risk, forecasting, decision, and automation system",
    version="1.0.0"
)


def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def home():
    return {"message": "API is running successfully"}


@app.get("/inventory")
def get_inventory():
    return read_csv("data/inventory.csv")


@app.get("/risk-alerts")
def get_risk_alerts():
    return read_csv("data/risk_alerts.csv")


@app.get("/forecast")
def get_forecast():
    return read_csv("data/demand_forecast.csv")


@app.get("/decisions")
def get_decisions():
    return read_csv("data/decisions.csv")


@app.get("/agent-actions")
def get_agent_actions():
    return read_csv("data/agent_actions.csv")
