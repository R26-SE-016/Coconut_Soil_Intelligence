import pandas as pd
import numpy as np
import json
import time
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
DATASET_DIR = ROOT_DIR / "dataset"
DATASET_DIR.mkdir(exist_ok=True)

from src.cri_guidelines import CRI_THRESHOLD_GUIDELINES

ZONE_PROFILES = {
    'A': { 
        'nitrogen': (35, 55), 'phosphorus': (18, 28), 'potassium': (45, 75), 
        'ph': (6.0, 6.8), 'ec': (400, 600), 'moisture': (45, 55), 'temperature': (26, 29)
    },
    'B': { 
        'nitrogen': (30, 60), 'phosphorus': (15, 30), 'potassium': (40, 80), 
        'ph': (5.5, 7.0), 'ec': (300, 700), 'moisture': (40, 60), 'temperature': (25, 30)
    },
    'C': { 
        'nitrogen': (10, 25), 'phosphorus': (5, 12), 'potassium': (20, 35), 
        'ph': (4.0, 5.0), 'ec': (100, 300), 'moisture': (20, 40), 'temperature': (28, 32)
    },
    'D': {'nitrogen': (30, 65), 'phosphorus': (16, 36), 'potassium': (40, 85), 'ph': (5.4, 7.0), 'ec': (380, 1400), 'moisture': (58, 82), 'temperature': (25, 30)},
    'E': {'nitrogen': (35, 60), 'phosphorus': (18, 30), 'potassium': (45, 75), 'ph': (5.6, 6.8), 'ec': (400, 1200), 'moisture': (60, 75), 'temperature': (26, 29)}
}

def get_health_label(n, p, k, ph, ec, mst, tmp):
    """Categorizes soil health into imbalance trends instead of prescriptions."""
    g = CRI_THRESHOLD_GUIDELINES
    
    if ph < g['ph']['optimal_min']: return 'Acidic Trend'
    if n < g['nitrogen']['optimal_min']: return 'Nitrogen Imbalance (Low)'
    if k < g['potassium']['optimal_min']: return 'Potassium Imbalance (Low)'
    if p < g['phosphorus']['optimal_min']: return 'Phosphorus Imbalance (Low)'
    if ec > g['ec']['optimal_max']: return 'High Salinity Trend'
    
    checks = [
        g['nitrogen']['optimal_min'] <= n <= g['nitrogen']['optimal_max'],
        g['phosphorus']['optimal_min'] <= p <= g['phosphorus']['optimal_max'],
        g['potassium']['optimal_min'] <= k <= g['potassium']['optimal_max'],
        g['ph']['optimal_min'] <= ph <= g['ph']['optimal_max']
    ]
    return 'Stable / Optimal' if all(checks) else 'Variable Stability'

def generate_scientific_dataset(samples_per_zone=200):
    np.random.seed(42)
    samples = []
    
    print("Generating Scientifically Aligned Dataset with Realistic Noise...")
    for zone_id, profile in ZONE_PROFILES.items():
        for i in range(samples_per_zone):
            noise_scale = 0.4 if zone_id in ['A', 'B'] else 1.0
            
            n = round(np.random.uniform(*profile['nitrogen']) + np.random.normal(0, 30 * noise_scale), 2)
            p = round(np.random.uniform(*profile['phosphorus']) + np.random.normal(0, 20 * noise_scale), 2)
            k = round(np.random.uniform(*profile['potassium']) + np.random.normal(0, 40 * noise_scale), 2)
            ph = round(np.random.uniform(*profile['ph']) + np.random.normal(0, 1.2 * noise_scale), 2)
            ec = round(np.random.uniform(*profile['ec']) + np.random.normal(0, 700 * noise_scale), 2)
            mst = round(np.random.uniform(*profile['moisture']) + np.random.normal(0, 25 * noise_scale), 2)
            tmp = round(np.random.uniform(*profile['temperature']) + np.random.normal(0, 10 * noise_scale), 1)

            ph = max(3.5, min(8.5, ph))
            
            label = get_health_label(n, p, k, ph, ec, mst, tmp)
            
            
            if np.random.random() < 0.35:
                possible_labels = [
                    'Acidic Trend', 'High Salinity Trend', 'Nitrogen Imbalance (Low)', 
                    'Phosphorus Imbalance (Low)', 'Potassium Imbalance (Low)', 
                    'Stable / Optimal', 'Variable Stability'
                ]
                label = np.random.choice(possible_labels)

            status = 'Stable' if label == 'Stable / Optimal' else 'Unstable'
            
            if np.random.random() < 0.15:
                status = 'Unstable' if status == 'Stable' else 'Stable'

            samples.append({
                'zone': zone_id,
                'sample_id': f"S_{zone_id}_{i+1:03d}",
                'nitrogen': n, 'phosphorus': p, 'potassium': k,
                'ph': ph, 'ec': ec, 'moisture': mst, 'temperature': tmp,
                'status': status,
                'imbalance_type': label,
                'timestamp': int(time.time()) - (i * 3600)
            })

    df = pd.DataFrame(samples)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    out_csv = DATASET_DIR / "coconut_soil_zone_dataset.csv"
    df.to_csv(out_csv, index=False)
    
    out_json = DATASET_DIR / "user_samples.json"
    df_json = df.rename(columns={'zone': 'zone_id', 'moisture': 'humidity'})
    with open(out_json, 'w') as f:
        json.dump(df_json.to_dict(orient='records'), f, indent=2)

    print(f"Generated {len(df)} records. Saved to {out_csv}")

if __name__ == "__main__":
    generate_scientific_dataset(1200)
