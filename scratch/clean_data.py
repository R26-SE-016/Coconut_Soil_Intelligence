import json
import os

files = [
    r"e:\Coconut_Soil_Intelligence\dataset\user_samples.json",
    r"e:\Coconut_Soil_Intelligence\dashboard\public\dataset\user_samples.json"
]

for file_path in files:
    if os.path.exists(file_path):
        print(f"Cleaning {file_path}...")
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for item in data:
            if 'further_action' in item:
                item['further_action'] = ""
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print("Done.")
