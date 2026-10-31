from pathlib import Path
import random
import pandas as pd

def generate(path="data/synthetic_steam_traps.csv", n=500, seed=42):
    rng = random.Random(seed)
    rows = []
    types = ["Float & Thermostatic", "Thermodynamic", "Inverted Bucket", "Thermostatic"]
    for i in range(1, n + 1):
        trap_type = rng.choice(types)
        pressure = round(rng.uniform(4, 12), 1)
        label = rng.choices(["Healthy", "Leaking", "Blocked", "Degraded"], [0.70, 0.12, 0.08, 0.10])[0]
        if label == "Healthy":
            temp, ultra, loss = round(rng.uniform(125,165),1), round(rng.uniform(8,35),1), round(rng.uniform(0,0.8),2)
        elif label == "Leaking":
            temp, ultra, loss = round(rng.uniform(150,190),1), round(rng.uniform(65,100),1), round(rng.uniform(3,18),2)
        elif label == "Blocked":
            temp, ultra, loss = round(rng.uniform(45,105),1), round(rng.uniform(5,40),1), round(rng.uniform(0,1.5),2)
        else:
            temp, ultra, loss = round(rng.uniform(100,175),1), round(rng.uniform(35,70),1), round(rng.uniform(0.8,5),2)
        rows.append({
            "trap_id": f"ST-{i:03d}", "trap_type": trap_type,
            "steam_pressure_bar": pressure, "temperature_c": temp,
            "ultrasonic_index": ultra, "operating_hours_per_day": rng.randint(8,24),
            "inspection_age_days": rng.randint(1,180), "estimated_loss_kg_hr": loss,
            "steam_cost_inr_per_tonne": rng.choice([1200,1500,1800,2200]),
            "synthetic_reference_label": label
        })
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Wrote {n} synthetic records to {path}")

if __name__ == "__main__":
    generate()
