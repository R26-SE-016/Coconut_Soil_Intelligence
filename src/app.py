from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import time
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.predict import predict_soil_health
from src.cri_guidelines import ZONE_DEFINITIONS, SCIENTIFIC_DISCLAIMER

app = Flask(__name__)
CORS(app)

DATASET_DIR = ROOT_DIR / "dataset"
ZONES_FILE = DATASET_DIR / "drawn_zones.json"
SAMPLES_FILE = DATASET_DIR / "user_samples.json"

def load_json(path, default):
    if os.path.exists(path):
        with open(path, 'r') as f: return json.load(f)
    return default

@app.route('/api/stats', methods=['GET'])
def get_stats():
    lang = request.args.get('lang', 'EN')
    l = lang if lang in ['EN', 'SI', 'TA'] else 'EN'
    samples = load_json(SAMPLES_FILE, [])
    drawn_zones = load_json(ZONES_FILE, [])
    
    all_zones = []
    for k, v in ZONE_DEFINITIONS.items(): all_zones.append({**v, "type": "predefined"})
    for z in drawn_zones: all_zones.append({**z, "type": "user-defined"})

    avg_ph = sum([s.get('ph', 0) for s in samples]) / len(samples) if samples else 0
    avg_ec = sum([s.get('ec', 0) for s in samples]) / len(samples) if samples else 0
    avg_moisture = sum([s.get('humidity', 0) for s in samples]) / len(samples) if samples else 0
    avg_temp = sum([s.get('temperature', 0) for s in samples]) / len(samples) if samples else 0
    
    unstable_count = len([s for s in samples if s.get('status') == 'Unstable'])
    imbalance_count = len([s for s in samples if s.get('imbalance_type') not in ['Stable / Optimal', 'ස්ථාවර / ප්‍රශස්ත', 'நிலையான / உகந்த']])
    
    total_stability = "Unstable" if (unstable_count / len(samples) > 0.4 if samples else False) else "Stable"
    avg_balance = "Imbalance" if (imbalance_count / len(samples) > 0.3 if samples else False) else "Balanced"

    zone_stats = {}
    for z in all_zones:
        z_samples = [s for s in samples if s.get('zone_id') == z['id']]
        z_count = len(z_samples)
        if z_count > 0:
            z_ph = sum([s.get('ph', 0) for s in z_samples]) / z_count
            z_ec = sum([s.get('ec', 0) for s in z_samples]) / z_count
            z_moist = sum([s.get('humidity', 0) for s in z_samples]) / z_count
            z_unstable = len([s for s in z_samples if s.get('status') == 'Unstable'])
            z_imbalance = len([s for s in z_samples if s.get('imbalance_type') not in ['Stable / Optimal', 'ස්ථාවර / ප්‍රශස්ත', 'நிலையான / உகந்த']])
            
            zone_stats[z['id']] = {
                "zone_name": z['name'], "samples": z_count, "stable": z_count - z_unstable,
                "unstable": z_unstable, "avg_ph": z_ph, "avg_ec": z_ec, "avg_moisture": z_moist,
                "imbalance": z_imbalance > (z_count * 0.3)
            }
        else:
            zone_stats[z['id']] = { "zone_name": z['name'], "samples": 0, "stable": 0, "unstable": 0, "avg_ph": 0, "avg_ec": 0, "avg_moisture": 0, "imbalance": False }

    trends = {
        'EN': {"Acidic": "Acidic", "Optimal": "Optimal", "Alkaline": "Alkaline"},
        'SI': {"Acidic": "ආම්ලික", "Optimal": "විශිෂ්ට", "Alkaline": "භාෂ්මික"},
        'TA': {"Acidic": "அமிலத்தன்மை", "Optimal": "சிறந்த", "Alkaline": "காரத்தன்மை"}
    }
    raw_trend = "Acidic" if avg_ph < 5.5 else "Optimal" if avg_ph < 7.0 else "Alkaline"

    return jsonify({
        "total_zones": len(all_zones), "total_samples": len(samples),
        "avg_ph": round(avg_ph, 1), "avg_ec": round(avg_ec, 2),
        "avg_moisture": round(avg_moisture, 1), "avg_temp": round(avg_temp, 1),
        "total_stability": total_stability, "avg_balance": avg_balance,
        "ph_trend": trends[l][raw_trend],
        "zone_stats": zone_stats,
        "disclaimer": SCIENTIFIC_DISCLAIMER[l]
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_sample():
    data = request.json
    lang = request.args.get('lang', 'EN')
    result = predict_soil_health(data, lang=lang)
    
    samples = load_json(SAMPLES_FILE, [])
    new_sample = {
        **data,
        **result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M")
    }
    samples.append(new_sample)
    with open(SAMPLES_FILE, 'w') as f: json.dump(samples[-500:], f, indent=2)
    
    return jsonify(result)

@app.route('/api/zones', methods=['GET', 'POST'])
def handle_zones():
    if request.method == 'POST':
        zones = load_json(ZONES_FILE, [])
        zones.append(request.json)
        with open(ZONES_FILE, 'w') as f: json.dump(zones, f, indent=2)
        return jsonify({"status": "success"})
    
    drawn_zones = load_json(ZONES_FILE, [])
    all_zones = []
    for k, v in ZONE_DEFINITIONS.items():
        all_zones.append({**v, "type": "predefined"})
    all_zones.extend(drawn_zones)
    return jsonify(all_zones)

@app.route('/api/samples', methods=['GET'])
def get_samples():
    try:
        lang = request.args.get('lang', 'EN')
        all_samples = load_json(SAMPLES_FILE, [])
        recent_samples = all_samples[-500:]
        
        for s in recent_samples:
            try:
                res = predict_soil_health(s, lang=lang)
                s.update(res)
            except:
                continue
        return jsonify(recent_samples[::-1]) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
