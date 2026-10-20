
import pandas as pd


def simulate_marketing_campaign(
    segment="Needs Attention",
    discount_rates=None,
):
    if discount_rates is None:
        discount_rates = [5, 10, 15]

    customers = pd.read_csv("data/customer_intelligence.csv")

    # Select customers in the requested segment
    target_customers = customers[
        customers["Customer_Segment"] == segment
    ].copy()

    if target_customers.empty:
        raise ValueError(f"No customers found in segment: {segment}")

    customer_count = len(target_customers)
    historical_revenue = target_customers["Total_Spend"].sum()

    results = []

    for discount in discount_rates:
        if not 0 <= discount <= 100:
            raise ValueError("Discount rates must be between 0 and 100.")

        # Scenario assumes every targeted customer redeems the offer
        estimated_discount_cost = (
            historical_revenue * discount / 100
        )
        estimated_revenue_after_discount = (
            historical_revenue - estimated_discount_cost
        )

        results.append(
            {
                "Customer_Segment": segment,
                "Discount_Percent": discount,
                "Customers_Targeted": customer_count,
                "Historical_Revenue_Baseline": round(
                    historical_revenue, 2
                ),
                "Estimated_Discount_Cost": round(
                    estimated_discount_cost, 2
                ),
                "Estimated_Revenue_After_Discount": round(
                    estimated_revenue_after_discount, 2
                ),
                "Assumption": (
                    "All targeted customers redeem the discount; "
                    "spending remains at historical levels before "
                    "the discount."
                ),
            }
        )

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        "data/marketing_simulation_results.csv",
        index=False,
    )

    print("Marketing campaign simulation completed!")
    print(f"Segment: {segment}")
    print(f"Customers targeted: {customer_count}")
    print("\nScenario comparison:")
    print(results_df.to_string(index=False))
    print("\nSaved to data/marketing_simulation_results.csv")

    return results_df


if __name__ == "__main__":
    simulate_marketing_campaign()
