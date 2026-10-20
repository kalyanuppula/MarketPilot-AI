
# MarketPilot AI — Explainable Customer Growth & Next-Best-Offer Engine

MarketPilot AI is a data-driven customer intelligence and marketing decision-support system that transforms retail transaction data into customer segments, personalized product recommendations, explainable offers, and marketing discount simulations.

It exposes these capabilities through a REST API built with **Python, Pandas, and FastAPI**, with interactive API documentation and a live deployment on Render.

## Live Demo

- **Live API:** https://marketpilot-ai-mvlb.onrender.com
- **Interactive API Docs:** https://marketpilot-ai-mvlb.onrender.com/docs

> Note: The Render free instance may spin down after inactivity. The first request after a period of inactivity can take around 50 seconds or more to respond.

## Business Problem

Retail businesses need to understand customer value, recommend relevant products, choose appropriate offers, and evaluate marketing decisions.

MarketPilot AI addresses these needs by combining customer analytics, personalized recommendations, offer selection, recommendation explanations, and discount scenario analysis in one API.

## Key Features

- **Customer Intelligence:** Customer-level profiles, RFM-based analysis, and customer segments.
- **Personalized Recommendations:** Product recommendations based on purchasing patterns, with popularity-based fallback recommendations.
- **Next-Best-Offer Engine:** Segment-aware marketing offers with different discount levels.
- **Explainable Recommendations:** Customer-facing explanations describing why products are recommended.
- **Marketing Scenario Simulation:** Compare discount scenarios and their estimated revenue impact.
- **REST API:** Access customer intelligence and marketing features through FastAPI endpoints.
- **Automated Testing:** Pytest tests for successful responses, missing customers, and invalid discount inputs.

## System Architecture

```text
Retail Transaction Dataset
          |
          v
Data Cleaning & Feature Engineering
          |
          v
Customer Intelligence & RFM Analysis
          |
          v
Product Recommendations & Offer Selection
          |
          v
Recommendation Explanations
          |
          v
Marketing Scenario Simulation
          |
          v
Precomputed CSV Data + FastAPI
          |
          v
Render Deployment + Swagger UI
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/customers/{customer_id}` | Retrieve customer intelligence |
| GET | `/recommendations/{customer_id}` | Retrieve personalized recommendations |
| GET | `/segments` | View customer segment counts |
| GET | `/offers/{customer_id}` | Retrieve the customer's next-best offer |
| GET | `/explanations/{customer_id}` | Retrieve recommendation explanations |
| GET | `/simulate-marketing` | Compare marketing discount scenarios |

### Example Requests

Health check:

```http
GET /health
```

Customer segments:

```http
GET /segments
```

Customer recommendations:

```http
GET /recommendations/17850
```

Marketing simulation:

```http
GET /simulate-marketing?segment=Needs%20Attention&discounts=5,10,15
```

The customer ID in the example is illustrative; use an ID present in the customer dataset. Explore and execute all endpoints through the [interactive Swagger documentation](https://marketpilot-ai-mvlb.onrender.com/docs).

## Technology Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **API Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Testing:** Pytest
- **Dependency Management:** uv
- **Deployment:** Render
- **Version Control:** Git and GitHub

## Dataset

The project uses the Online Retail transaction dataset for customer and product analytics.

The application uses precomputed CSV datasets for customer intelligence, recommendations, offers, and recommendation explanations. Raw and intermediate datasets are excluded from the repository to avoid unnecessary repository size.

## Marketing Simulation Methodology

The marketing simulator compares discount scenarios and calculates their estimated revenue impact using historical segment revenue.

**Important:** These are scenario-based calculations, not predictions of incremental revenue or causal estimates of discount effectiveness. Actual customer response and campaign uplift would require suitable experimental or historical campaign data.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/kalyanuppula/MarketPilot-AI.git
cd MarketPilot-AI
```

### 2. Create and activate a virtual environment

```bash
uv sync
```

### 3. Start the API

```bash
uv run uvicorn main:app --reload
```

Open the local API at `http://127.0.0.1:8000` and the documentation at `http://127.0.0.1:8000/docs`.

Ensure the required CSV files are available in the `data/` directory before starting the application.

### 4. Run the tests

```bash
uv run pytest -v
```

The project has passed **10 automated tests** in the local development environment.

## Project Structure

```text
MarketPilot-AI/
├── data/
│   ├── customer_intelligence.csv
│   ├── next_best_offers.csv
│   ├── personalized_recommendations.csv
│   └── recommendation_explanations.csv
├── tests/
│   └── test_main.py
├── customer_features.py
├── customer_intelligence.py
├── customer_segmentation.py
├── data_processing.py
├── main.py
├── marketing_simulator.py
├── next_best_offer.py
├── personalized_recommendations.py
├── product_recommendations.py
├── recommendation_explanations.py
├── rfm_scoring.py
├── requirements.txt
└── pyproject.toml
```

## Future Improvements

- Add campaign response prediction and uplift modeling.
- Introduce model monitoring and recommendation quality metrics.
- Add a business dashboard for customer and marketing insights.
- Implement scheduled data refresh and pipeline orchestration.
- Add authentication, rate limiting, and production observability.

## Author

**Kalyan Uppula**

GitHub: https://github.com/kalyanuppula
