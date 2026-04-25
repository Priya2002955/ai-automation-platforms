import pandas as pd


def load_sales_data():
    sales = pd.read_csv("data/sales.csv")
    return sales


def forecast_demand():
    sales = load_sales_data()

    forecasts = []

    grouped = sales.groupby(["store_id", "product"])

    for (store_id, product), group in grouped:
        avg_daily_sales = group["units_sold"].mean()

        forecast_3_days = round(avg_daily_sales * 3, 2)
        forecast_7_days = round(avg_daily_sales * 7, 2)

        forecasts.append({
            "store_id": store_id,
            "product": product,
            "avg_daily_sales": round(avg_daily_sales, 2),
            "forecast_3_days": forecast_3_days,
            "forecast_7_days": forecast_7_days
        })

    forecast_df = pd.DataFrame(forecasts)
    forecast_df.to_csv("data/demand_forecast.csv", index=False)

    print("Demand forecast generated successfully!")
    print(forecast_df.head(10))


if __name__ == "__main__":
    forecast_demand()