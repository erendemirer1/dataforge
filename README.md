# DataForge

A deterministic demographic simulation and opinion dynamics engine for Turkey.

DataForge simulates large-scale public opinion shifts, policy responses, and macroeconomic counterfactuals across Turkey's 81 provinces and 973 districts.

Traditional survey polling is slow and expensive, while prompting generic language models often yields demographically flat, ungrounded responses. DataForge addresses this by pairing statistical micro-data (TÜİK income distributions, BDDK debt ratios, SEGE socioeconomic development indices) with discrete choice econometrics and structural causal graphs.

---

## Overview

DataForge generates representative synthetic cohorts constrained by empirical regional distributions. When evaluated against any proposed policy, economic shock, or public referendum, the engine calculates decision probabilities through discrete choice utility models rather than unconstrained text generation.

### Core Architecture

- **Stratified Demographic Sampler**: Generates representative citizen cohorts based on regional NUTS-2 data, district socioeconomic tiers (SEGE-2022), and ISCO-08 occupational-educational matrices.
- **Multivariate Joint Distributions**: Uses Gaussian Copulas to maintain realistic correlations across age, income percentiles, housing status, debt burden, and financial liquidity.
- **Structural Causal Decision Engine**: Combines discrete choice models (McFadden Multinomial Logit) with Kahneman loss aversion and Haidt moral foundations to evaluate policy acceptance across distinct demographic segments.
- **Live Environmental Ingestion**: Integrates live exchange rates, inflation metrics, and active public news feeds to reflect real-world economic sentiment.
- **Qualitative Probing & Stance Consistency**: Allows multi-turn qualitative interviews with any sampled individual while strictly binding their stated vote, income level, and regional identity.

---

## Quickstart

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Linux / WSL (recommended) or macOS / Windows

### Installation

```bash
git clone https://github.com/erendemirer1/dataforge.git
cd dataforge

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and package in editable mode
pip install -r requirements.txt
pip install -e .
```

### Running the Application

Start the local server:

```bash
python3 -m uvicorn dataforge.api.app:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
`http://localhost:8000`

---

## Testing

Run the test suite with pytest:

```bash
python3 -m pytest
```

All 79 unit and integration tests validate the data generators, statistical copula models, causal DAG transitions, and API routes.

---

## Project Structure

```
dataforge/
├── dataforge/
│   ├── api/
│   │   ├── app.py                     # FastAPI application entrypoint
│   │   ├── routes/                    # API route handlers
│   │   └── static/                    # Map explorer UI & assets
│   ├── cognitive/
│   │   ├── census_engine.py           # Polling and discrete choice engine
│   │   ├── causal_dag_engine.py       # Structural causal decision graph
│   │   ├── living_stream_engine.py    # Live macro data ingestion
│   │   ├── micro_biography_matrix.py  # Biographical parameter tensor
│   │   ├── interrogation_engine.py    # Qualitative interview handler
│   │   └── ideology_matrix.py         # Regional demographic weights
│   └── ml/
│       ├── copula_engine.py           # Gaussian copula joint distributions
│       └── reference_stats.py         # Empirical demographic reference tables
├── tests/                             # Test suite (79 tests)
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## License

Distributed under the MIT License.
