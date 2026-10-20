
import pandas as pd


def build_next_best_offers():
    # Load existing project outputs
    customers = pd.read_csv("data/customer_intelligence.csv")
    recommendations = pd.read_csv(
        "data/personalized_recommendations.csv"
    )

    # Select a marketing strategy for each customer segment
    offer_rules = {
        "High Value": {
            "Offer_Type": "VIP Reward",
            "Discount_Percent": 10,
            "Offer_Reason": "Reward a high-value customer and encourage repeat purchases.",
        },
        "At Risk": {
            "Offer_Type": "Win-Back Discount",
            "Discount_Percent": 15,
            "Offer_Reason": "Encourage a customer who may be drifting away to return.",
        },
        "Loyal / Promising": {
            "Offer_Type": "Loyalty Reward",
            "Discount_Percent": 10,
            "Offer_Reason": "Strengthen loyalty and encourage another purchase.",
        },
        "Needs Attention": {
            "Offer_Type": "Targeted Incentive",
            "Discount_Percent": 5,
            "Offer_Reason": "Provide a small incentive to encourage another purchase.",
        },
    }

    # Choose the top-ranked product recommendation for each customer
    top_recommendations = (
        recommendations.sort_values("Rank")
        .drop_duplicates(subset="CustomerID", keep="first")
        [["CustomerID", "Recommended_StockCode",
          "Recommended_Description"]]
    )

    # Combine customer intelligence with the recommended product
    offers = customers.merge(
        top_recommendations,
        on="CustomerID",
        how="left",
        validate="one_to_one",
    )

    # Assign the offer based on customer segment
    offers["Offer_Type"] = offers["Customer_Segment"].map(
        lambda segment: offer_rules.get(segment, {}).get("Offer_Type")
    )
    offers["Discount_Percent"] = offers["Customer_Segment"].map(
        lambda segment: offer_rules.get(segment, {}).get(
            "Discount_Percent"
        )
    )
    offers["Offer_Reason"] = offers["Customer_Segment"].map(
        lambda segment: offer_rules.get(segment, {}).get("Offer_Reason")
    )

    # Save one offer per customer; overwrite on every run
    output_columns = [
        "CustomerID",
        "Country",
        "Customer_Segment",
        "Total_Spend",
        "Recency_Days",
        "Offer_Type",
        "Discount_Percent",
        "Recommended_StockCode",
        "Recommended_Description",
        "Offer_Reason",
    ]

    offers = offers[output_columns].sort_values("CustomerID")
    offers.to_csv("data/next_best_offers.csv", index=False)

    print("Next-best-offer generation completed!")
    print(f"Customers with offers: {len(offers)}")
    print("\nOffer distribution:")
    print(offers["Offer_Type"].value_counts())
    print("\nSample offers:")
    print(offers.head())


if __name__ == "__main__":
    build_next_best_offers()
