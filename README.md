# DataForge

A deterministic demographic simulation and opinion dynamics engine for Turkey.

DataForge models large-scale public opinion shifts, policy responses, and macroeconomic counterfactuals across Turkey's 81 provinces and 973 districts.

Traditional survey polling is slow, expensive, and quickly invalidated by rapid news cycles. Conversely, prompting generic large language models produces demographically ungrounded, sycophantic responses. DataForge addresses this by coupling empirical micro-data (TÜİK income distributions, BDDK debt ratios, SEGE socioeconomic development indices) with discrete choice econometrics, Gaussian copulas, and structural causal graphs.

---

## Architectural Pipeline

```
                                [ Policy / Public Ballot Query ]
                                               │
                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. LIVE MACRO & SOCIAL PULSE INGESTION (living_stream_engine.py)                       │
│    ├── Real-time USD/TRY exchange rate feeds (open currency APIs)                      │
│    ├── Official benchmark inflation & interest rate calibration                        │
│    ├── Automated RSS headline scraping (BBC Türkçe / TRT Haber)                        │
│    └── Dynamic Societal Agitation Index computation (Ψ_live)                           │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. DETERMINISTIC STRATIFIED COHORT SAMPLING (N=1,000 in <15ms) (copula_engine.py)      │
│    ├── NUTS-2 Regional & SEGE-2022 District Stratification (Tiers 1 to 6)              │
│    ├── High-Dimensional Gaussian Copula (Age, Income, Housing, Debt Covariance)        │
│    └── 81-Province Empirical Demographic Weight Distribution (ideology_matrix.py)      │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
                      ┌────────────────────────┴────────────────────────┐
                      ▼                                                 ▼
┌───────────────────────────────────────────┐   ┌───────────────────────────────────────────┐
│ 3. STRUCTURAL CAUSAL DAG (causal_dag.py)  │   │ 4. COGNITIVE HABITUS & MORAL TENSOR       │
│    ├── Pearl SEM: Invariant Propagation   │   │    ├── Kahneman Loss Aversion (λ = 2.25)  │
│    ├── do(X) Macroeconomic Interventions  │   │    ├── Jonathan Haidt 6 Moral Foundations │
│    └── Discretionary Cash Flow Margins    │   │    └── 100+ Micro-Biographical Nuances    │
└───────────────────────────────────────────┘   └───────────────────────────────────────────┘
                                               │
                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 5. MULTINOMIAL DISCRETE CHOICE & VOCALIZATION (census_engine.py)                       │
│    ├── McFadden Logit Utility Calculation: P(Accept), P(Reject), P(Undecided)          │
│    ├── Domain-Specific Argumentation (Fiscal, Governance, Ecological, Urban)           │
│    └── Cross-Tabulation Generation across Regional Demographic Cohorts                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
                      ┌────────────────────────┴────────────────────────┐
                      ▼                                                 ▼
┌───────────────────────────────────────────┐   ┌───────────────────────────────────────────┐
│ 6. SOCRATIC INTERROGATION ENGINE          │   │ 7. SMALL-WORLD CONTAGION GRAPH            │
│    ├── Subconscious Bias vs Spoken Voice  │   │    ├── Watts-Strogatz Topology (K=4, p=0.1│
│    ├── Real-Time Bayesian Belief Shift ΔP │   │    ├── Local Opinion Cascades & Tipping   │
│    └── SQLite Persistent Episodic Memory  │   │    └── Polarization Clustering Indices    │
└───────────────────────────────────────────┘   └───────────────────────────────────────────┘
```

---

## Theoretical & Econometric Foundations

### 1. Multivariate Joint Distributions via Gaussian Copula
Demographic attributes cannot be generated independently. DataForge models joint dependencies across continuous and categorical variables (Age, Household Income, Credit Card Limits, Rent-to-Income ratios) using Gaussian Copulas:

$$C_R(u_1, u_2, \dots, u_d) = \Phi_R\left(\Phi^{-1}(u_1), \Phi^{-1}(u_2), \dots, \Phi^{-1}(u_d)\right)$$

This guarantees that every sampled profile reflects strictly accurate, correlated socioeconomic parameters calibrated to official census tables without demographic drift.

### 2. Structural Causal Models & do-calculus
The decision pipeline enforces invariant causal graphs based on Judea Pearl's Structural Equation Modeling (SEM):

$$\text{SEGE Tier} \longrightarrow \text{Gross Income} \longrightarrow \text{Expense Pressure} \longrightarrow \text{Loss Aversion } (\lambda) \longrightarrow \text{Utility } (U)$$

Interventions such as $do(\Delta\text{Inflation} = +20\%)$ dynamically shock household discretionary liquidity and shift policy resistance through non-linear behavioral loss penalties ($\lambda = 2.25$).

### 3. Discrete Choice Logit Formulation
Citizen decisions are calculated using Random Utility Maximization (McFadden Multinomial Logit):

$$P(y_i = k) = \frac{\exp(V_{ik})}{\sum_{j \in \{Accept, Reject, Undecided\}} \exp(V_{ij})}$$

Where $V_{ik}$ integrates fiscal utility, value alignment, and moral foundation weights.

---

## Core Capabilities

### Stratified Sociodemographic & Regional Segmentation
DataForge models regional public opinion across 81 provinces by mapping population cohorts to empirical demographic profiles:

| Demographic Cohort | Regional Focus | Core Concerns & Primary Decision Drivers |
| :--- | :--- | :--- |
| **Metropolitan Working-Class & Tenants** | Urban Centers (Istanbul, Ankara, Izmir) | Housing affordability, public transport, inflation resilience |
| **Agrarian & Rural Producers** | Inner & Eastern Anatolia | Agricultural subsidies, input costs, local infrastructure |
| **Industrial & Small Business Operators** | Marmara, Central Anatolia | Commercial credit access, tax policies, supply chain stability |
| **Young Professionals & Students** | Major Metropolitan & University Hubs | Youth employment, meritocracy, digital freedom, purchasing power |
| **Public Sector & Fixed Income Retirees** | Nationwide Suburban & Provincial Centers | Pension indexing, healthcare access, social stability |

### Live Environmental Stream (`LivingStreamEngine`)
The platform continuously ingests external signals to reflect active societal pressure:
- **Live Currency Feed**: Fetches real-time USD/TRY exchange rates from public financial endpoints.
- **News Agenda Ingestion**: Scrapes active headlines via RSS feeds (BBC Türkçe, TRT Haber).
- **Composite Agitation Score ($\Psi_{live}$)**: Evaluates inflation sentiment and macro volatility to adjust risk aversion across the population tensor.

### Socratic Qualitative Interrogation (`InterrogationEngine`)
Conduct multi-turn interviews with individual simulated citizens:
- **System 1 (Subconscious Reflection)**: Unvarnished, raw emotional and self-interested reaction.
- **System 2 (Spoken Articulation)**: Socially calibrated justification.
- **Bayesian Belief Update ($\Delta P$)**: Calculates persuasion vulnerability when presented with logical, economic, or moral counter-arguments.
- **Longitudinal Memory**: Stores interaction history in SQLite (`episodic_memory.py`) to maintain stance consistency across extended sessions.

---

## API Reference

The FastAPI backend exposes endpoints for polling, persona interrogation, network contagion, and macro telemetry.

### 1. Run Stratified Census Poll
`POST /api/v1/census/poll`

```bash
curl -X POST "http://localhost:8000/api/v1/census/poll" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Should municipal public transit fare subsidies be expanded?",
       "city": "Diyarbakır",
       "sample_size": 1000
     }'
```

**Response Preview:**
```json
{
  "soru_veya_politika": "Should municipal public transit fare subsidies be expanded?",
  "hedef_bolge": "Diyarbakır",
  "orneklem_buyuklugu": 1000,
  "genel_kabul_yuzde": 68.4,
  "genel_ret_yuzde": 21.2,
  "genel_kararsiz_yuzde": 10.4,
  "siyasi_taban_kirilimi": [
    {
      "segment": "Metropolitan Working-Class & Tenants",
      "orneklem_sayisi": 420,
      "kabul_yuzde": 78.5,
      "ret_yuzde": 12.1,
      "kararsiz_yuzde": 9.4
    }
  ]
}
```

### 2. Conduct Socratic 1-on-1 Interview
`POST /api/v1/society/interrogate`

```bash
curl -X POST "http://localhost:8000/api/v1/society/interrogate" \
     -H "Content-Type: application/json" \
     -d '{
       "persona_dict": {
         "first_name": "Serkan",
         "last_name": "Yılmaz",
         "age": 34,
         "occupation": "Esnaf",
         "city": "Diyarbakır",
         "housing_status": "Kiracı",
         "monthly_income": 32000.0
       },
       "user_question": "What is your primary concern regarding local commercial tax increases?",
       "survey_context": "Municipal budget expansion"
     }'
```

### 3. Fetch Live Macro Telemetry
`GET /api/v1/society/live-pulse`

---

## Quickstart

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Linux / WSL (recommended) or macOS / Windows

### Installation

```bash
# Clone the repository
git clone https://github.com/erendemirer1/dataforge.git
cd dataforge

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies and local package
pip install -r requirements.txt
pip install -e .
```

### Running the Application

```bash
# Start the FastAPI web service and interactive map explorer
python3 -m uvicorn dataforge.api.app:app --host 0.0.0.0 --port 8000 --reload
```

Navigate to: `http://localhost:8000`

---

## CLI Data Generation Engine

DataForge includes a standalone CLI tool for generating high-fidelity relational synthetic datasets:

```bash
# Generate synthetic users with validated Turkish TCKN and socioeconomic profiles
dataforge generate --schema users --count 1000 --format json

# Generate financial transaction logs
dataforge generate --schema transactions --count 5000 --format parquet

# List available built-in relational schemas
dataforge schema list
```

---

## Test Suite & Verification

DataForge includes 79 automated unit and integration tests covering econometrics, causal DAG transformations, copula joint distributions, and REST routes:

```bash
python3 -m pytest
```

```text
============================= test session starts ==============================
collected 79 items

tests/test_api.py ...                                                    [  3%]
tests/test_behavior.py .......                                           [ 12%]
tests/test_calibration.py ..                                             [ 15%]
tests/test_causal.py ..                                                  [ 17%]
tests/test_causal_framework.py ...                                       [ 21%]
tests/test_census.py ..                                                  [ 24%]
tests/test_contagion.py .                                                [ 25%]
tests/test_counterfactual.py .                                           [ 26%]
tests/test_generators.py ......................................          [ 74%]
tests/test_historical_backtesting.py .....                               [ 81%]
tests/test_interrogation.py .                                            [ 82%]
tests/test_ml.py .                                                       [ 83%]
tests/test_society_api.py ...                                            [ 87%]
tests/test_tckn.py ..........                                            [100%]

======================== 79 passed, 1 warning in 14.71s ========================
```

---

## Project Structure

```
dataforge/
├── dataforge/
│   ├── api/
│   │   ├── app.py                     # FastAPI application entrypoint
│   │   ├── routes/
│   │   │   ├── society.py             # Polling, interrogation, and pulse endpoints
│   │   │   └── generators.py          # Synthetic dataset generation routes
│   │   └── static/
│   │       ├── index.html             # D3 GeoJSON interactive gazette UI
│   │       └── assets/tr-cities.json  # 81-Province spatial vector geometry
│   ├── cognitive/
│   │   ├── census_engine.py           # McFadden Logit & stratified polling engine
│   │   ├── ideology_matrix.py         # Regional sociodemographic cohort matrices
│   │   ├── living_stream_engine.py    # Live FX and RSS news pulse ingestion
│   │   ├── micro_biography_matrix.py  # 100+ parameter human biographical tensor
│   │   ├── causal_dag_engine.py       # Judea Pearl Structural Causal DAG
│   │   ├── interrogation_engine.py    # Socratic qualitative interview handler
│   │   ├── episodic_memory.py         # SQLite persistent longitudinal agent memory
│   │   └── social_graph.py            # Watts-Strogatz small-world network engine
│   ├── ml/
│   │   ├── copula_engine.py           # Multivariate Gaussian Copula engine
│   │   └── reference_stats.py         # Empirical TÜİK, BDDK, SGK & ISCO-08 tables
│   └── generators/                    # Relational data generators (Users, Products, etc.)
├── tests/                             # 79 Automated pytest test suites
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## License

Distributed under the MIT License. Developed by Eren Demirer (2026).
