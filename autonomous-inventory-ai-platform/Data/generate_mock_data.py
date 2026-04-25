import pandas as pd
import random
from faker import Faker

fake = Faker()

# Stores
stores = []
for i in range(1, 11):
    stores.append({
        "store_id": i,
        "store_name": f"Store_{i}",
        "city": fake.city()
    })
stores_df = pd.DataFrame(stores)

# Products
products = ["Chicken", "Buns", "Fries", "Oil", "Sauce"]

# Inventory
inventory = []
for store in stores:
    for product in products:
        inventory.append({
            "store_id": store["store_id"],
            "product": product,
            "current_stock": random.randint(50, 300),
            "daily_usage": random.randint(10, 50)
        })
inventory_df = pd.DataFrame(inventory)

# Sales (last 30 days)
sales = []
for store in stores:
    for product in products:
        for day in range(30):
            sales.append({
                "store_id": store["store_id"],
                "product": product,
                "day": day,
                "units_sold": random.randint(5, 60)
            })
sales_df = pd.DataFrame(sales)

# Suppliers
suppliers = []
for product in products:
    suppliers.append({
        "product": product,
        "supplier_name": fake.company(),
        "lead_time_days": random.randint(1, 5)
    })
suppliers_df = pd.DataFrame(suppliers)

# Reorder rules
rules = []
for product in products:
    rules.append({
        "product": product,
        "reorder_threshold": random.randint(80, 120),
        "max_stock": random.randint(300, 500)
    })
rules_df = pd.DataFrame(rules)

# Save files
stores_df.to_csv("data/stores.csv", index=False)
inventory_df.to_csv("data/inventory.csv", index=False)
sales_df.to_csv("data/sales.csv", index=False)
suppliers_df.to_csv("data/suppliers.csv", index=False)
rules_df.to_csv("data/reorder_rules.csv", index=False)

print("Mock data generated successfully!")