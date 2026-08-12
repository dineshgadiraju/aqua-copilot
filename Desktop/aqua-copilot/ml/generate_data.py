from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 3000

temperature = rng.normal(29.0, 2.0, n).clip(22, 36)
ph = rng.normal(7.8, 0.55, n).clip(6.0, 9.5)
do = rng.normal(5.0, 1.25, n).clip(1.0, 9.0)
salinity = rng.normal(18, 6.0, n).clip(2, 35)
ammonia = rng.gamma(1.8, 0.08, n).clip(0, 1.0)
feed = rng.normal(42, 15, n).clip(5, 100)
age = rng.integers(10, 130, n)
density = rng.normal(45, 15, n).clip(10, 100)

risk_score = (
    1.8 * (do < 3.5)
    + 1.4 * (ammonia > 0.25)
    + 1.2 * ((ph < 7.0) | (ph > 8.6))
    + 1.0 * ((temperature < 26) | (temperature > 32))
    + 0.8 * ((salinity < 8) | (salinity > 28))
    + 0.8 * (density > 65)
    + 0.5 * (feed > 65)
)

risk_score += rng.normal(0, 0.45, n)

risk = np.where(risk_score >= 2.2, 1, 0)

df = pd.DataFrame({
    "temperature_c": temperature.round(2),
    "ph": ph.round(2),
    "dissolved_oxygen_mg_l": do.round(2),
    "salinity_ppt": salinity.round(2),
    "ammonia_mg_l": ammonia.round(3),
    "feed_kg_day": feed.round(2),
    "shrimp_age_days": age,
    "stocking_density_per_m2": density.round(1),
    "high_risk": risk
})

out = Path(__file__).parent / "data" / "shrimp_pond_data.csv"
df.to_csv(out, index=False)

print(f"Saved {len(df)} rows to {out}")
print(df["high_risk"].value_counts(normalize=True))
