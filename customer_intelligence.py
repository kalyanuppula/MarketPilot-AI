
import pandas as pd


def build_customer_intelligence():
    # Load cleaned transaction data
    df = pd.read_csv("data/cleaned_retail_data.csv")

    # Validate required columns
    required_columns = [
        "InvoiceNo",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Prepare customer and transaction data
    df = df.dropna(subset=required_columns).copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="raise")
    df["CustomerID"] = df["CustomerID"].astype("int64")

    # Include valid purchases only
    df = df[
        (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    # Calculate transaction revenue
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Reference date: latest transaction in the dataset
    reference_date = df["InvoiceDate"].max()

    # Build one record per customer
    customers = (
        df.groupby("CustomerID")
        .agg(
            Country=("Country", lambda x: x.mode().iloc[0]),
            Purchase_Frequency=("InvoiceNo", "nunique"),
            Total_Quantity=("Quantity", "sum"),
            Total_Spend=("Revenue", "sum"),
            Last_Purchase=("InvoiceDate", "max"),
        )
        .reset_index()
    )

    # Calculate recency in days
    customers["Recency_Days"] = (
        reference_date - customers["Last_Purchase"]
    ).dt.days

    # Round spending to two decimal places
    customers["Total_Spend"] = customers["Total_Spend"].round(2)


    # Calculate RFM scores from 1 to 5
    customers["R_Score"] = pd.qcut(
        customers["Recency_Days"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1],
    ).astype(int)

    customers["F_Score"] = pd.qcut(
        customers["Purchase_Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    customers["M_Score"] = pd.qcut(
        customers["Total_Spend"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    customers["RFM_Score"] = (
        customers["R_Score"]
        + customers["F_Score"]
        + customers["M_Score"]
    )

        # Assign mutually exclusive marketing segments
    conditions = [
        (customers["RFM_Score"] >= 13)
        & (customers["R_Score"] >= 3),

        (customers["R_Score"] <= 2)
        & (customers["F_Score"] >= 3),

        (customers["RFM_Score"] >= 10)
        & (customers["R_Score"] >= 3),
    ]

    segments = [
        "High Value",
        "At Risk",
        "Loyal / Promising",
    ]

    import numpy as np

    customers["Customer_Segment"] = np.select(
        conditions,
        segments,
        default="Needs Attention",
    )

    # Rank customers by total spending
    customers = customers.sort_values(
        "Total_Spend", ascending=False
    ).reset_index(drop=True)

    # Save to the same file on every run
    customers.to_csv("data/customer_intelligence.csv", index=False)

    print("Customer intelligence analysis completed!")
    print(f"Total customers analyzed: {len(customers)}")
    print(f"Reference date: {reference_date.date()}")
    print("Output: data/customer_intelligence.csv")


if __name__ == "__main__":
    build_customer_intelligence()
