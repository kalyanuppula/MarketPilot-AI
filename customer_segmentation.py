import pandas as pd


def segment_customers():
    df = pd.read_csv("data/rfm_scored_customers.csv")

    def assign_segment(row):
        r = row["R_Score"]
        f = row["F_Score"]
        m = row["M_Score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"

        elif f >= 4 and m >= 3:
            return "Loyal Customers"

        elif r >= 4 and f >= 2:
            return "Potential Loyalists"

        elif r <= 2 and f >= 3 and m >= 3:
            return "At Risk"

        elif r <= 2 and f <= 2 and m <= 2:
            return "Hibernating"

        else:
            return "Needs Attention"

    df["Segment"] = df.apply(assign_segment, axis=1)

    df.to_csv("data/customer_segments.csv", index=False)

    print("Customer segmentation completed!")
    print("Total customers:", len(df))
    print("\nCustomer segment counts:")
    print(df["Segment"].value_counts())

    print("\nSample segmented customers:")
    print(
        df[
            [
                "CustomerID",
                "RFM_Score",
                "Segment",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    segment_customers()