
SCIENTIFIC_DISCLAIMER = {
    'EN': "Decision Support Only: Professional CRI laboratory or leaf analysis is mandatory for final decision making.",
    'SI': "විද්‍යාත්මක තීරණ ගැනීමේ සහාය පමණි: අවසාන තීරණ සඳහා CRI රසායනාගාර හෝ පත්‍ර විශ්ලේෂණය අනිවාර්ය වේ.",
    'TA': "முடிவு ஆதரவு மட்டும்: இறுதி முடிவெடுப்பதற்கு தொழில்முறை CRI ஆய்வகம் அல்லது இலை பகுப்பாய்வு கட்டாயமாகும்."
}

CRI_THRESHOLD_GUIDELINES = {
    'nitrogen': {
        'unit': 'mg/kg', 'optimal_min': 30, 'optimal_max': 60,
        'alerts': {
            'EN': {'low': 'Potential Nitrogen Deficiency Detected', 'high': 'Excessive Nitrogen Trend'},
            'SI': {'low': 'නයිට්‍රජන් ඌනතාවයක් හඳුනාගෙන ඇත', 'high': 'නයිට්‍රජන් අතිරික්තයක් පවතී'},
            'TA': {'low': 'நைட்ரஜன் குறைபாடு கண்டறியப்பட்டது', 'high': 'அதிகப்படியான நைட்ரஜன் போக்கு'}
        },
        'actions': {
            'EN': {'low': 'Apply Urea or Nitrogen-rich organic compost.', 'high': 'Reduce nitrogen fertilization and monitor leaching.'},
            'SI': {'low': 'යුරියා හෝ නයිට්‍රජන් බහුල කාබනික පොහොර යොදන්න.', 'high': 'නයිට්‍රජන් පොහොර යෙදීම අඩු කර ජලවහනය පරීක්ෂා කරන්න.'},
            'TA': {'low': 'யுரியா அல்லது நைட்ரஜன் நிறைந்த கரிம உரம் பயன்படுத்தவும்.', 'high': 'நைட்ரஜன் உரமிடுவதைக் குறைத்து, கசிவைக் கண்காணிக்கவும்.'}
        }
    },
    'phosphorus': {
        'unit': 'mg/kg', 'optimal_min': 15, 'optimal_max': 30,
        'alerts': {
            'EN': {'low': 'Potential Phosphorus Imbalance Detected', 'high': 'High Phosphorus Trend'},
            'SI': {'low': 'පොස්පරස් අසමතුලිතතාවයක් හඳුනාගෙන ඇත', 'high': 'අධික පොස්පරස් ප්‍රවණතාවයක් පවතී'},
            'TA': {'low': 'பாஸ்பரஸ் சமநிலையின்மை கண்டறியப்பட்டது', 'high': 'அதிக பாஸ்பரஸ் போக்கு'}
        },
        'actions': {
            'EN': {'low': 'Apply Rock Phosphate (ERP) near the manure circle.', 'high': 'Suspend phosphorus application for one season.'},
            'SI': {'low': 'පොහොර වළල්ල ආසන්නයේ එප්පාවල රොක් පොස්පේට් (ERP) යොදන්න.', 'high': 'එක් කන්නයක් සඳහා පොස්පරස් යෙදීම නතර කරන්න.'},
            'TA': {'low': 'எப்பாவல ராக் பாஸ்பேட் (ERP) பயன்படுத்தவும்.', 'high': 'ஒரு பருவத்திற்கு பாஸ்பரஸ் பயன்படுத்துவதை நிறுத்தவும்.'}
        }
    },
    'potassium': {
        'unit': 'mg/kg', 'optimal_min': 40, 'optimal_max': 80,
        'alerts': {
            'EN': {'low': 'Potential Potassium Deficiency Detected', 'high': 'High Potassium Trend'},
            'SI': {'low': 'පොටෑසියම් ඌනතාවයක් හඳුනාගෙන ඇත', 'high': 'අධික පොටෑසියම් ප්‍රවණතාවයක් පවතී'},
            'TA': {'low': 'பொட்டாசியம் குறைபாடு கண்டறியப்பட்டது', 'high': 'அதிக பொட்டாசியம் போக்கு'}
        },
        'actions': {
            'EN': {'low': 'Apply Muriate of Potash (MOP) as recommended.', 'high': 'Monitor for potential salt toxicity.'},
            'SI': {'low': 'නිර්දේශිත පරිදි මියුරියේට් ඔෆ් පොටෑෂ් (MOP) යොදන්න.', 'high': 'ලවණ විෂ වීමේ හැකියාව පිළිබඳ විමසිලිමත් වන්න.'},
            'TA': {'low': 'மூரியேட் ஆஃப் பொட்டாஷ் (MOP) பயன்படுத்தவும்.', 'high': 'உப்பு நச்சுத்தன்மையைக் கண்காணிக்கவும்.'}
        }
    },
    'ph': {
        'unit': 'pH', 'optimal_min': 5.5, 'optimal_max': 7.0,
        'alerts': {
            'EN': {'low': 'Acidic Soil Warning', 'high': 'Alkaline Soil Warning'},
            'SI': {'low': 'ආම්ලික පස් පිළිබඳ අනතුරු ඇඟවීම', 'high': 'භාෂ්මික පස් පිළිබඳ අනතුරු ඇඟවීම'},
            'TA': {'low': 'அமில மண் எச்சரிக்கை', 'high': 'கார மண் எச்சரிக்கை'}
        },
        'actions': {
            'EN': {'low': 'Apply Dolomite (1-2 kg per tree) to correct acidity.', 'high': 'Use ammonium-based fertilizers to lower pH.'},
            'SI': {'low': 'ආම්ලිකතාවය පාලනයට ගසකට ඩොලමයිට් කිලෝග්‍රෑම් 1-2ක් යොදන්න.', 'high': 'pH අගය අඩු කිරීමට ඇමෝනියම් සහිත පොහොර භාවිතා කරන්න.'},
            'TA': {'low': 'அமிலத்தன்மையை சரிசெய்ய டோலமைட் பயன்படுத்தவும்.', 'high': 'pH ஐக் குறைக்க அம்மோனியம் அடிப்படையிலான உரங்களைப் பயன்படுத்தவும்.'}
        }
    },
    'ec': {
        'unit': 'µS/cm', 'optimal_min': 400, 'optimal_max': 1500,
        'alerts': {
            'EN': {'low': 'Low Nutrient Concentration', 'high': 'High Soil Salinity Warning'},
            'SI': {'low': 'අඩු පෝෂක සාන්ද්‍රණයක් හඳුනාගෙන ඇත', 'high': 'අධික ලවණතාවය පිළිබඳ අනතුරු ඇඟවීම'},
            'TA': {'low': 'குறைந்த ஊட்டச்சத்து செறிவு', 'high': 'அதிக மண் உப்புத்தன்மை எச்சரிக்கை'}
        },
        'actions': {
            'EN': {'low': 'General fertilization recommended.', 'high': 'Flush soil with fresh water and improve drainage.'},
            'SI': {'low': 'පොදු පොහොර යෙදීම නිර්දේශ කරනු ලැබේ.', 'high': 'පස පිරිසිදු ජලයෙන් සෝදා ජලවහනය වැඩි දියුණු කරන්න.'},
            'TA': {'low': 'பொதுவான உரமிடுதல் பரிந்துரைக்கப்படுகிறது.', 'high': 'மண்ணை நன்னீரால் கழுவி வடிகால் வசதியை மேம்படுத்தவும்.'}
        }
    },
    'moisture': {
        'unit': '%', 'optimal_min': 50, 'optimal_max': 80,
        'alerts': {
            'EN': {'low': 'Water Stress (Dry Soil)', 'high': 'Waterlogging Warning'},
            'SI': {'low': 'ජල හිඟය (වියළි පස)', 'high': 'අධික ජලයෙන් යටවීම පිළිබඳ අනතුරු ඇඟවීම'},
            'TA': {'low': 'நீர் அழுத்தம் (உலர் மண்)', 'high': 'நீர் தேக்க எச்சரிக்கை'}
        },
        'actions': {
            'EN': {'low': 'Increase irrigation frequency and use mulching.', 'high': 'Clear drainage paths to remove excess water.'},
            'SI': {'low': 'ජල සම්පාදනය වැඩි කර වසුන් (Mulching) භාවිතා කරන්න.', 'high': 'වැඩිපුර ජලය ඉවත් කිරීමට ජලාපවහන පද්ධති පිරිසිදු කරන්න.'},
            'TA': {'low': 'நீர்ப்பாசனத்தை அதிகரித்து தழைக்கூளம் பயன்படுத்தவும்.', 'high': 'அதிகப்படியான நீரை அகற்ற வடிகால் பாதைகளை சுத்தம் செய்யவும்.'}
        }
    },
    'temperature': {
        'unit': '°C', 'optimal_min': 25, 'optimal_max': 35,
        'alerts': {
            'EN': {'low': 'Low Soil Temperature', 'high': 'High Heat Stress'},
            'SI': {'low': 'අඩු පස් උෂ්ණත්වය', 'high': 'අධික තාප ආතතිය'},
            'TA': {'low': 'குறைந்த மண் வெப்பநிலை', 'high': 'அதிக வெப்ப அழுத்தம்'}
        },
        'actions': {
            'EN': {'low': 'Monitor for slow nutrient uptake.', 'high': 'Ensure adequate moisture and provide shade if possible.'},
            'SI': {'low': 'පෝෂක අවශෝෂණය මන්දගාමී වීම පිළිබඳ විමසිලිමත් වන්න.', 'high': 'ප්‍රමාණවත් තෙතමනයක් පවත්වා ගන්න.'},
            'TA': {'low': 'ஊட்டச்சத்து உறிஞ்சுதலைக் கண்காணிக்கவும்.', 'high': 'போதுமான ஈரப்பதத்தை உறுதிப்படுத்தவும்.'}
        }
    }
}

ZONE_DEFINITIONS = {
    'A': {'id': 'A', 'name': 'Zone A (West Segment)', 'polygon': [[6.0580, 80.2250], [6.0583, 80.2250], [6.0583, 80.2260], [6.0580, 80.2260]], 'color': '#16a34a'},
    'B': {'id': 'B', 'name': 'Zone B (West-Central Segment)', 'polygon': [[6.0583, 80.2250], [6.0586, 80.2250], [6.0586, 80.2260], [6.0583, 80.2260]], 'color': '#16a34a'},
    'C': {'id': 'C', 'name': 'Zone C (Central Segment)', 'polygon': [[6.0586, 80.2250], [6.0589, 80.2250], [6.0589, 80.2260], [6.0586, 80.2260]], 'color': '#16a34a'},
    'D': {'id': 'D', 'name': 'Zone D (East Central Segment)', 'polygon': [[6.0589, 80.2250], [6.0592, 80.2250], [6.0592, 80.2260], [6.0589, 80.2260]], 'color': '#16a34a'},
    'E': {'id': 'E', 'name': 'Zone E (East Segment)', 'polygon': [[6.0592, 80.2250], [6.0595, 80.2250], [6.0595, 80.2260], [6.0592, 80.2260]], 'color': '#16a34a'}
}

def analyze_stability(row: dict, lang='EN') -> dict:
    alerts = []
    actions = []
    status = 'Stable'
    l = lang if lang in ['EN', 'SI', 'TA'] else 'EN'
    
    for param, guide in CRI_THRESHOLD_GUIDELINES.items():
        val = row.get(param)
        if val is None: continue
        
        if val < guide['optimal_min']:
            alerts.append(guide['alerts'][l]['low'])
            if 'actions' in guide: actions.append(guide['actions'][l]['low'])
            status = 'Unstable'
        elif val > guide['optimal_max']:
            alerts.append(guide['alerts'][l]['high'])
            if 'actions' in guide: actions.append(guide['actions'][l]['high'])
            status = 'Unstable'

    stable_msg = {
        'EN': "Stability Optimal - Maintain Monitoring",
        'SI': "පස ස්ථාවරයි - අධීක්ෂණය පවත්වා ගන්න",
        'TA': "நிலைத்தன்மை சிறந்தது - கண்காணிப்பைத் தொடரவும்"
    }

    return {
        'status': status,
        'alerts': alerts if alerts else [stable_msg[l]],
        'actions': actions,
        'disclaimer': SCIENTIFIC_DISCLAIMER[l]
    }
