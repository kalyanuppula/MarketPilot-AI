import pandas as pd


def load_and_clean_data(file_path="data/Online Retail.xlsx"):
    df = pd.read_excel(file_path)

    # Remove transactions without customer IDs
    df = df.dropna(subset=["CustomerID"])

    # Remove cancelled invoices
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Keep only positive quantities and prices
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Remove duplicate records
    df = df.drop_duplicates()

    return df


if __name__ == "__main__":
    df = load_and_clean_data()

    output_path = "data/cleaned_retail_data.csv"
    df.to_csv(output_path, index=False)

    print("Data cleaning completed!")
    print("Cleaned dataset saved to:", output_path)
    print("Rows after cleaning:", len(df))
    print("Unique customers:", df["CustomerID"].nunique())
    print("Unique products:", df["StockCode"].nunique())