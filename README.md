# DataForge

**A Deterministic Causal Engine & Stratified Simulation System for Turkish Demographics and Social Dynamics.**

DataForge is a high-performance computational framework designed to simulate large-scale demographic distributions, public opinion shifts, and macroeconomic counterfactuals across Turkey's 81 provinces and 973 districts.

Unlike prompt-only language model workflows—which suffer from token degeneration, demographic hallucination, and lack of stateful probability distributions—DataForge couples a **deterministic Directed Acyclic Graph (DAG)** with **Kahneman's Cumulative Prospect Theory**, **Watts-Strogatz social network percolation**, and a multi-model cognitive vocalization gateway.

---

## Architectural Pillars

```
                                  [ Policy / Ballot Query ]
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DETERMINISTIC CAUSAL SAMPLER (CPU / N=1,000 in 12ms)            │
│  ├── NUTS-2 Regional Stratification (TR10 to TRA2)                                     │
│  ├── SEGE-2022 District Socioeconomic Development Indices (Tiers 1 to 6)               │
│  ├── ISCO-08 Occupational-Educational-Income Joint Distributions                       │
│  └── BDDK / SGK Household Balance Sheets (Net Salary, Rent, Debt-to-Income)            │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
┌───────────────────────────────────────────┐ ┌──────────────────────────────────────────┐
│        COGNITIVE HABITUS MATRICES         │ │     DYNAMIC NETWORK CONTAGION GRAPH      │
│  ├── Kahneman Prospect Theory (λ = 2.25)  │ │  ├── Watts-Strogatz Topology (K=6, p=0.15│
│  ├── Laibson Quasi-Hyperbolic Discounting │ │  ├── Granovetter Threshold Cascade       │
│  ├── Bourdieu 4-Capital Habitus Vector    │ │  └── Viral Reproduction Number (R₀)      │
│  └── Haidt 6 Moral Foundations            │ └──────────────────────────────────────────┘
└───────────────────────────────────────────┘                      │
                      │                                            │
                      └──────────────────────┬─────────────────────┘
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                  UNIVERSAL AI INHABITATION & DIALOGUE GATEWAY                          │
│  ├── Longitudinal Stance Anchoring (Deterministic State Binding)                       │
│  ├── Dual-Channel Vocalization (System 1 Subconscious Bias + System 2 Spoken Reply)    │
│  └── Priority Model Failover Chain (gemini-3.5-flash -> 3.1-flash-lite -> local SLM)  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Capabilities

### 1. Stratified Quantitative Census (`MunicipalCensusEngine`)
Samples representative synthetic cohorts ($N=100$ to $N=10,000$) calibrated to Turkish demographic tables. Computes 95% confidence intervals, margins of error, and cross-tabulations across age groups, socioeconomic tiers, housing status, and geographical districts.

### 2. Socratic Interrogation & Stance Anchoring (`InterrogationEngine`)
Allows direct multi-turn qualitative probing of any individual agent in the ballot. The engine binds each agent's prior vote, economic constraints, and moral coordinates as an immutable constraint, exposing both public statements and internal System 1 reflections.

### 3. Sub-100ms Macroeconomic Stress-Testing (`CounterfactualEngine`)
Applies instantaneous macroeconomic shocks (minimum wage revisions, CPI inflation, residential rent spikes) across the entire simulated population. Updates individual discretionary liquidity and shifts voting distributions in real-time using asymmetric loss aversion ($\lambda = 2.25$).

### 4. Social Contagion & Echo Chamber Simulation (`SocialContagionEngine`)
Models opinion diffusion through small-world graph topologies. Measures network clustering coefficients, polarization indices, tipping points, and peer pressure cascades.

---

## Quickstart

### Option A: Docker (Recommended)

```bash
git clone https://github.com/erendemirer1/dataforge.git
cd dataforge

# Copy environment template (Gemini API key is optional)
cp .env.example .env

# Build and start container
docker compose up --build
```

Access the interactive interface at `http://localhost:8000`.

---

### Option B: Local Python Environment

Requirements: Python 3.10, 3.11, or 3.12.

```bash
# Clone and setup virtual environment
git clone https://github.com/erendemirer1/dataforge.git
cd dataforge
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and local package
pip install -r requirements.txt
pip install -e .

# Launch local server
uvicorn dataforge.api.app:app --host 0.0.0.0 --port 8000 --reload
```

---

## Command Line Interface (CLI)

DataForge provides a CLI tool for generating compliant synthetic datasets and verifying schema referential integrity:

```bash
# Generate 1,000 NUTS-2 calibrated Turkish citizen profiles
dataforge generate --schema users --count 1000 --format json --output output/citizens.json

# Export high-throughput Parquet or SQL relational data
dataforge generate --schema users --count 50000 --format parquet --output output/population.parquet
dataforge generate --schema orders --count 100000 --format sql --output output/transactions.sql

# Validate synthetic data against TCKN checksum algorithms
dataforge validate output/citizens.json
```

---

## REST API Reference

The FastAPI backend exposes OpenAPI endpoints documented interactively at `/docs`:

| Endpoint | Method | Payload | Description |
|:---|:---|:---|:---|
| `/api/v1/census/poll` | `POST` | `{ city, district, question, sample_size }` | Executes quantitative census polling. |
| `/api/v1/society/interrogate` | `POST` | `{ persona_dict, user_question, conversation_history }` | Conducts 1-on-1 Socratic interview turn. |
| `/api/v1/counterfactual/simulate-shock` | `POST` | `{ current_ballots, delta_wage, delta_inflation, delta_rent }` | Recomputes population ballots under economic stress. |
| `/api/v1/focus-group/simulate` | `POST` | `{ target_audience, pitch_or_question, count }` | Runs multi-agent deliberative focus group. |
| `/api/v1/society/export-report` | `POST` | `{ report_data }` | Produces an institutional whitepaper / PDF report. |

---

## Performance & Verification

The deterministic causal graph generates 1,000 fully articulated 50-parameter profiles in under 15 milliseconds on a single modern CPU thread.

```bash
pytest -v
```

```
============================== test session starts ==============================
collected 74 items

tests/test_api.py ...                                                    [  4%]
tests/test_behavior.py .......                                           [ 13%]
tests/test_calibration.py ..                                             [ 16%]
tests/test_causal.py ..                                                  [ 18%]
tests/test_causal_framework.py ...                                       [ 22%]
tests/test_census.py ..                                                  [ 25%]
tests/test_contagion.py .                                                [ 27%]
tests/test_counterfactual.py .                                           [ 28%]
tests/test_generators.py ......................................          [ 79%]
tests/test_interrogation.py .                                            [ 81%]
tests/test_ml.py .                                                       [ 82%]
tests/test_society_api.py ...                                            [ 86%]
tests/test_tckn.py ..........                                            [100%]

======================== 74 passed in 1.25s ========================
```

---

## Data Privacy & Governance

All profiles, identities, national ID numbers (TCKN), and financial balances generated by DataForge are purely mathematical constructs derived from aggregate macroeconomic distributions. No personally identifiable information (PII) is stored or processed, ensuring full compliance with KVKK (Turkey) and GDPR (EU) research mandates.

---

## License

This software is released under the [MIT License](LICENSE).
