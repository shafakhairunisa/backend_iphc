import os
import json

# Load from JSON only once
file_path = os.path.join("dataset", "disease_knowledge.json")
with open(file_path, "r") as f:
    disease_knowledge = json.load(f)

def get_disease_info(name):
    key = name.strip().title()
    return disease_knowledge.get(key, {
        "message": f"No information found for '{name}'."
    })

def get_multiple_disease_info(disease_list):
    return {
        disease: get_disease_info(disease)
        for disease in disease_list
    }
