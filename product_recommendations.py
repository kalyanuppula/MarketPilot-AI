
import pandas as pd


def build_product_recommendations():
    # Load cleaned transaction data
    df = pd.read_csv("data/cleaned_retail_data.csv")

    # Validate required columns
    required_columns = ["StockCode", "Description", "InvoiceNo", "Quantity"]
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Remove records without essential product information
    df = df.dropna(subset=["StockCode", "Description", "InvoiceNo"])

    # Exclude cancelled invoices and non-positive quantities
    df = df[
        ~df["InvoiceNo"].astype(str).str.startswith("C")
        & (df["Quantity"] > 0)
    ]

    # Aggregate each product into one row
    recommendations = (
        df.groupby("StockCode", as_index=False)
        .agg(
            Description=("Description", lambda x: x.mode().iloc[0]),
            Purchase_Count=("InvoiceNo", "nunique"),
            Total_Quantity=("Quantity", "sum"),
        )
        .sort_values(
            by=["Purchase_Count", "Total_Quantity"],
            ascending=False,
        )
    )

    # Save to the same file, overwriting previous results
    recommendations.to_csv("data/product_popularity.csv", index=False)

    print("Product popularity analysis completed!")
    print(f"Unique products: {len(recommendations)}")


if __name__ == "__main__":
    build_product_recommendations()
