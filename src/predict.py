import joblib
import numpy as np
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.cri_guidelines import analyze_stability, SCIENTIFIC_DISCLAIMER

MODELS_DIR = ROOT_DIR / "models"

def load_models():
    try:
        stability = joblib.load(MODELS_DIR / "stability_model.joblib")
        imbalance = joblib.load(MODELS_DIR / "imbalance_model.joblib")
        le = joblib.load(MODELS_DIR / "imbalance_label_encoder.joblib")
        return stability, imbalance, le
    except:
        return None, None, None

STABILITY_MODEL, IMBALANCE_MODEL, LABEL_ENC = load_models()

def predict_soil_health(sensor_data: dict, lang='EN'):
    """
    Analyzes sensor data using ML and CRI rules with multi-language support.
    """
    l = lang if lang in ['EN', 'SI', 'TA'] else 'EN'
    
    guideline_data = sensor_data.copy()
    if 'humidity' in guideline_data:
        guideline_data['moisture'] = guideline_data.pop('humidity')
        
    analysis = analyze_stability(guideline_data, lang=l)
    
    imbalance_type = "Stable / Optimal" 
    
    IMBALANCE_MAP = {
        'Stable / Optimal': {'EN': 'Stable / Optimal', 'SI': 'ස්ථාවර / ප්‍රශස්ත', 'TA': 'நிலையான / உகந்த'},
        'Nitrogen Imbalance (Low)': {'EN': 'Nitrogen Imbalance (Low)', 'SI': 'නයිට්‍රජන් අසමතුලිතතාවය (අඩු)', 'TA': 'நைட்ரஜன் சமநிலையின்மை (குறைந்த)'},
        'Nitrogen Imbalance (High)': {'EN': 'Nitrogen Imbalance (High)', 'SI': 'නයිට්‍රජන් අසමතුලිතතාවය (වැඩි)', 'TA': 'நைட்ரஜன் சமநிலையின்மை (அதிக)'},
        'Phosphorus Imbalance (Low)': {'EN': 'Phosphorus Imbalance (Low)', 'SI': 'පොස්පරස් අසමතුලිතතාවය (අඩු)', 'TA': 'பாஸ்பரஸ் சமநிலையின்மை (குறைந்த)'},
        'Phosphorus Imbalance (High)': {'EN': 'Phosphorus Imbalance (High)', 'SI': 'පොස්පරස් අසමතුලිතතාවය (වැඩි)', 'TA': 'பாஸ்பரஸ் சமநிலையின்மை (அதிக)'},
        'Potassium Imbalance (Low)': {'EN': 'Potassium Imbalance (Low)', 'SI': 'පොටෑසියම් අසමතුලිතතාවය (අඩු)', 'TA': 'பொட்டாசியம் சமநிலையின்மை (குறைந்த)'},
        'Potassium Imbalance (High)': {'EN': 'Potassium Imbalance (High)', 'SI': 'පොටෑසියම් අසමතුලිතතාවය (වැඩි)', 'TA': 'பொட்டாசியம் சமநிலையின்மை (அதிக)'},
        'pH/EC Imbalance': {'EN': 'pH/EC Imbalance', 'SI': 'pH/EC අසමතුලිතතාවය', 'TA': 'pH/EC சமநிலையின்மை'}
    }

    if STABILITY_MODEL and IMBALANCE_MODEL:
        features = [
            sensor_data.get('nitrogen', 0),
            sensor_data.get('phosphorus', 0),
            sensor_data.get('potassium', 0),
            sensor_data.get('ph', 7.0),
            sensor_data.get('ec', 500),
            sensor_data.get('humidity', 70),
            sensor_data.get('temperature', 28)
        ]
        
        imbalance_pred_idx = IMBALANCE_MODEL.predict([features])[0]
        raw_type = LABEL_ENC.inverse_transform([imbalance_pred_idx])[0]
        imbalance_type = IMBALANCE_MAP.get(raw_type, {}).get(l, raw_type)
    else:
        from src.data_generator import get_health_label
        raw_type = get_health_label(
            sensor_data.get('nitrogen', 0),
            sensor_data.get('phosphorus', 0),
            sensor_data.get('potassium', 0),
            sensor_data.get('ph', 7.0),
            sensor_data.get('ec', 500),
            sensor_data.get('humidity', 70),
            sensor_data.get('temperature', 28)
        )
        imbalance_type = IMBALANCE_MAP.get(raw_type, {}).get(l, raw_type)

    insight_header = {
        'EN': "Detected Trend",
        'SI': "හඳුනාගත් ප්‍රවණතාවය",
        'TA': "கண்டறியப்பட்ட போக்கு"
    }

    return {
        'status': analysis['status'],
        'monitoring_insight': f"{insight_header[l]}: {imbalance_type}",
        'imbalance_type': imbalance_type,
        'alerts': analysis['alerts'],
        'actions': analysis['actions'],
        'disclaimer': analysis['disclaimer'],
        'further_action': " | ".join(analysis['actions']) if analysis['actions'] else ""
    }
