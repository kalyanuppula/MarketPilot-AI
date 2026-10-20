import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_existing_customer():
    response = client.get("/customers/12346")

    assert response.status_code == 200
    assert response.json()["CustomerID"] == 12346
    assert response.json()["Customer_Segment"] == "Needs Attention"


def test_get_customer_recommendations():
    response = client.get("/recommendations/12346")

    assert response.status_code == 200

    data = response.json()
    assert data["customer_id"] == 12346
    assert len(data["recommendations"]) == 5
    assert data["recommendations"][0]["Rank"] == 1


def test_get_customer_segments():
    response = client.get("/segments")

    assert response.status_code == 200

    data = response.json()
    assert data["total_customers"] == 4338
    assert sum(data["segments"].values()) == 4338


def test_unknown_customer():
    response = client.get("/customers/99999999")

    assert response.status_code == 404


def test_get_next_best_offer():
    response = client.get("/offers/12346")

    assert response.status_code == 200
    data = response.json()
    assert data["CustomerID"] == 12346
    assert data["Customer_Segment"] == "Needs Attention"
    assert data["Offer_Type"] == "Targeted Incentive"
    assert data["Discount_Percent"] == 5
    assert data["Recommended_Description"]


def test_unknown_customer_offer():
    response = client.get("/offers/99999999")

    assert response.status_code == 404



def test_get_recommendation_explanations():
    response = client.get("/explanations/12346")

    assert response.status_code == 200
    data = response.json()

    assert data["customer_id"] == 12346
    assert len(data["explanations"]) == 5
    assert data["explanations"][0]["Rank"] == 1
    assert data["explanations"][0]["Recommendation_Reason"]
    assert data["explanations"][0]["Explanation"]


def test_unknown_customer_explanations():
    response = client.get("/explanations/99999999")

    assert response.status_code == 404


def test_marketing_simulation():
    response = client.get(
        "/simulate-marketing",
        params={
            "segment": "Needs Attention",
            "discounts": "5,10,15",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["segment"] == "Needs Attention"
    assert len(data["scenarios"]) == 3
    assert [
        scenario["Discount_Percent"]
        for scenario in data["scenarios"]
    ] == [5, 10, 15]


def test_marketing_simulation_rejects_invalid_discount():
    response = client.get(
        "/simulate-marketing",
        params={
            "segment": "Needs Attention",
            "discounts": "5,150",
        },
    )

    assert response.status_code == 400
