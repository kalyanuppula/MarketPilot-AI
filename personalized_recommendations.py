
import itertools
from collections import Counter, defaultdict

import pandas as pd


def build_personalized_recommendations():
    # Load existing project outputs
    transactions = pd.read_csv("data/cleaned_retail_data.csv")
    customers = pd.read_csv("data/customer_intelligence.csv")
    popularity = pd.read_csv("data/product_popularity.csv")

    # Keep valid purchases
    transactions = transactions.dropna(
        subset=["CustomerID", "InvoiceNo", "StockCode", "Description"]
    )
    transactions = transactions[
        (transactions["Quantity"] > 0)
        & (transactions["UnitPrice"] > 0)
    ].copy()

    transactions["CustomerID"] = transactions["CustomerID"].astype(int)
    transactions["StockCode"] = transactions["StockCode"].astype(str)

    # Map product codes to descriptions
    descriptions = (
        transactions.drop_duplicates("StockCode")
        .set_index("StockCode")["Description"]
        .to_dict()
    )

    # Count products purchased together in the same invoice
    pair_counts = Counter()

    for _, basket in transactions.groupby("InvoiceNo"):
        products = sorted(set(basket["StockCode"]))
        pair_counts.update(itertools.combinations(products, 2))

    # Make product associations available in both directions
    associations = defaultdict(Counter)

    for (product_a, product_b), count in pair_counts.items():
        associations[product_a][product_b] = count
        associations[product_b][product_a] = count

    # Identify products each customer has already purchased
    customer_products = (
        transactions.groupby("CustomerID")["StockCode"]
        .apply(set)
        .to_dict()
    )

    # Global popularity is the fallback when no associations exist
    popularity["StockCode"] = popularity["StockCode"].astype(str)
    popular_products = popularity.sort_values(
        ["Purchase_Count", "Total_Quantity"],
        ascending=False,
    )["StockCode"].tolist()

    segment_lookup = customers.set_index("CustomerID")[
        "Customer_Segment"
    ].to_dict()

    recommendations = []

    for customer_id, purchased_products in customer_products.items():
        scores = Counter()

        # Recommend products associated with the customer's purchase history
        for product in purchased_products:
            for candidate, count in associations[product].items():
                if candidate not in purchased_products:
                    scores[candidate] += count

        # Fill any remaining slots with globally popular products
        for product in popular_products:
            if product not in purchased_products and product not in scores:
                scores[product] = 0

        ranked_products = sorted(
            scores.items(),
            key=lambda item: (
                item[1],
                item[0] in popular_products[:100],
            ),
            reverse=True,
        )[:5]

        for rank, (product, score) in enumerate(ranked_products, start=1):
            recommendations.append(
                {
                    "CustomerID": customer_id,
                    "Customer_Segment": segment_lookup.get(
                        customer_id, "Unknown"
                    ),
                    "Rank": rank,
                    "Recommended_StockCode": product,
                    "Recommended_Description": descriptions.get(
                        product, "Unknown product"
                    ),
                    "Recommendation_Score": score,
                    "Recommendation_Reason": (
                        "Frequently purchased together"
                        if score > 0
                        else "Popular product fallback"
                    ),
                }
            )

    result = pd.DataFrame(recommendations)

    # Overwrite the same output file on every run
    result.to_csv("data/personalized_recommendations.csv", index=False)

    print("Personalized recommendations completed!")
    print(f"Customers recommended for: {result['CustomerID'].nunique()}")
    print(f"Recommendations generated: {len(result)}")
    print("Output: data/personalized_recommendations.csv")


if __name__ == "__main__":
    build_personalized_recommendations()
