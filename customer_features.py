
import pandas as pd


def build_customer_features():
    df = pd.read_csv("data/cleaned_retail_data.csv")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    customer_features = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda dates: (
            analysis_date - dates.max()
        ).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum"),
    ).reset_index()

    customer_features.to_csv(
        "data/customer_features.csv",
        index=False
    )

    print("Customer features created successfully!")
    print("Number of customers:", len(customer_features))
    print("\nFirst five customers:")
    print(customer_features.head())


if __name__ == "__main__":
    build_customer_features()
