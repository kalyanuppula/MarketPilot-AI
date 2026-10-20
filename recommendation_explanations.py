
import pandas as pd


def build_recommendation_explanations():
    recommendations = pd.read_csv(
        "data/personalized_recommendations.csv"
    )
    customers = pd.read_csv(
        "data/customer_intelligence.csv"
    )

    # Add customer context to each recommendation
    explanations = recommendations.merge(
        customers[
            [
                "CustomerID",
                "Purchase_Frequency",
                "Total_Spend",
                "Recency_Days",
                "Customer_Segment",
            ]
        ].drop(columns=["Customer_Segment"]),
        on="CustomerID",
        how="left",
        validate="many_to_one",
    )

    # Explain the recommendation using its actual reason and score
    explanations["Explanation"] = explanations.apply(
        lambda row: (
            f"Recommended because this product is "
            f"{row['Recommendation_Reason'].lower()}. "
            f"It has a recommendation score of "
            f"{row['Recommendation_Score']:.0f}. "
            f"The customer has made {row['Purchase_Frequency']:.0f} "
            f"distinct purchases and spent "
            f"{row['Total_Spend']:.2f} in total."
        ),
        axis=1,
    )

    output_columns = [
        "CustomerID",
        "Customer_Segment",
        "Rank",
        "Recommended_StockCode",
        "Recommended_Description",
        "Recommendation_Score",
        "Recommendation_Reason",
        "Purchase_Frequency",
        "Total_Spend",
        "Recency_Days",
        "Explanation",
    ]

    explanations = explanations[output_columns]

    # Overwrite the same file on every run
    explanations.to_csv(
        "data/recommendation_explanations.csv",
        index=False,
    )

    print("Recommendation explanations generated!")
    print(f"Total explanations: {len(explanations)}")
    print("\nSample explanations:")
    print(
        explanations[
            [
                "CustomerID",
                "Recommended_Description",
                "Explanation",
            ]
        ].head(3).to_string(index=False)
    )


if __name__ == "__main__":
    build_recommendation_explanations()
