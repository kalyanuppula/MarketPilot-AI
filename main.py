from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = FastAPI(
    title="MarketPilot AI",
    description="Explainable Customer Growth & Next-Best-Offer Engine",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to MarketPilot AI!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    df = pd.read_csv(DATA_DIR / "customer_intelligence.csv")
    customer = df[df["CustomerID"] == customer_id]

    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.iloc[0].to_dict()


@app.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: int):
    df = pd.read_csv(DATA_DIR / "personalized_recommendations.csv")
    recommendations = df[df["CustomerID"] == customer_id]

    if recommendations.empty:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found for this customer",
        )

    return {
        "customer_id": customer_id,
        "customer_segment": recommendations.iloc[0]["Customer_Segment"],
        "recommendations": recommendations.sort_values("Rank").to_dict(
            orient="records"
        ),
    }


@app.get("/segments")
def get_customer_segments():
    df = pd.read_csv(DATA_DIR / "customer_intelligence.csv")

    return {
        "total_customers": len(df),
        "segments": df["Customer_Segment"].value_counts().to_dict(),
    }


@app.get("/offers/{customer_id}")
def get_next_best_offer(customer_id: int):
    df = pd.read_csv(DATA_DIR / "next_best_offers.csv")
    offer = df[df["CustomerID"] == customer_id]

    if offer.empty:
        raise HTTPException(
            status_code=404,
            detail="No offer found for this customer",
        )

    return offer.iloc[0].to_dict()


@app.get("/explanations/{customer_id}")
def get_recommendation_explanations(customer_id: int):
    df = pd.read_csv(DATA_DIR / "recommendation_explanations.csv")
    explanations = df[df["CustomerID"] == customer_id]

    if explanations.empty:
        raise HTTPException(
            status_code=404,
            detail="No recommendation explanations found for this customer",
        )

    return {
        "customer_id": customer_id,
        "explanations": explanations.sort_values("Rank").to_dict(
            orient="records"
        ),
    }



@app.get("/simulate-marketing")
def simulate_marketing(
    segment: str = "Needs Attention",
    discounts: str = "5,10,15",
):
    from marketing_simulator import simulate_marketing_campaign

    try:
        discount_rates = [
            float(value.strip())
            for value in discounts.split(",")
        ]

        if not discount_rates:
            raise ValueError("Provide at least one discount rate.")

        if any(not 0 <= rate <= 100 for rate in discount_rates):
            raise ValueError("Discount rates must be between 0 and 100.")

        results = simulate_marketing_campaign(
            segment=segment,
            discount_rates=discount_rates,
        )

        return {
            "segment": segment,
            "scenarios": results.to_dict(orient="records"),
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
