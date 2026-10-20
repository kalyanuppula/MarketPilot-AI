
import pandas as pd


def score_customers():
    df = pd.read_csv("data/customer_features.csv")

    # Score each metric from 1 to 5.
    # Recency is reversed: fewer days means a higher score.
    df["R_Score"] = pd.qcut(
        df["Recency"].rank(method="first"),
        5,
        labels=[5, 4, 3, 2, 1],
    ).astype(int)

    df["F_Score"] = pd.qcut(
        df["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    df["M_Score"] = pd.qcut(
        df["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    df["RFM_Score"] = (
        df["R_Score"].astype(str)
        + df["F_Score"].astype(str)
        + df["M_Score"].astype(str)
    )

    df.to_csv("data/rfm_scored_customers.csv", index=False)

    print("RFM scoring completed!")
    print("Number of customers:", len(df))
    print("\nSample scored customers:")
    print(
        df[
            [
                "CustomerID",
                "Recency",
                "Frequency",
                "Monetary",
                "R_Score",
                "F_Score",
                "M_Score",
                "RFM_Score",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    score_customers()
