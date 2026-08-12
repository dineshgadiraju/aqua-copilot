# Aqua Copilot

AI-powered shrimp pond risk monitoring platform.

## Milestone 1
This starter version includes:
- Synthetic shrimp pond dataset generation
- ML training pipeline using Random Forest
- Saved prediction model
- FastAPI prediction endpoint

## Features
Inputs:
- temperature_c
- ph
- dissolved_oxygen_mg_l
- salinity_ppt
- ammonia_mg_l
- feed_kg_day
- shrimp_age_days
- stocking_density_per_m2

Output:
- risk_level
- risk_probability
- risk factors
- recommended actions

## Run locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate starter data

```bash
python ml/generate_data.py
```

### 3. Train model

```bash
python ml/train.py
```

### 4. Start API

```bash
uvicorn backend.app.main:app --reload
```

Then open:
http://127.0.0.1:8000/docs
