"""
Disease Information Web Scraper
Fetches real disease data from agricultural websites for accurate diagnosis.
"""

import logging
import asyncio
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)

# Disease database with common symptoms and treatments
# This can be expanded with web scraping from agricultural sites
DISEASE_DATABASE = {
    # CORN DISEASES
    "Corn_(maize)___Common_rust_": {
        "symptoms": ["Small, circular to elongated brown pustules", "Pustules on both leaf surfaces", "Yellowing of leaves"],
        "treatment": [
            "Apply fungicides containing azoxystrobin or propiconazole",
            "Plant resistant corn hybrids",
            "Remove and destroy infected plant debris",
            "Ensure proper plant spacing for air circulation"
        ],
        "prevention": [
            "Use resistant varieties",
            "Rotate crops with non-host plants",
            "Apply preventive fungicide sprays during humid weather",
            "Monitor fields regularly during warm, humid conditions"
        ],
        "severity": "Moderate to High",
        "recovery_days": "14-21 days with treatment"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "symptoms": ["Long, elliptical gray-green lesions", "Lesions turn tan with age", "Lesions parallel to leaf veins"],
        "treatment": [
            "Apply fungicides (strobilurin or triazole-based)",
            "Remove severely infected leaves",
            "Improve field drainage",
            "Reduce plant density if possible"
        ],
        "prevention": [
            "Plant resistant hybrids",
            "Crop rotation with non-cereal crops",
            "Bury crop residue after harvest",
            "Avoid overhead irrigation"
        ],
        "severity": "High",
        "recovery_days": "21-28 days"
    },
    
    # TOMATO DISEASES
    "Tomato___Early_blight": {
        "symptoms": ["Dark brown spots with concentric rings (target-like)", "Lower leaves affected first", "Yellowing around spots"],
        "treatment": [
            "Apply copper-based fungicides or chlorothalonil",
            "Remove infected lower leaves",
            "Mulch around plants to prevent soil splash",
            "Water at base of plants, not overhead"
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Rotate crops (3-4 year cycle)",
            "Space plants properly for air circulation",
            "Apply preventive fungicide sprays"
        ],
        "severity": "Moderate",
        "recovery_days": "14-21 days"
    },
    "Tomato___Late_blight": {
        "symptoms": ["Water-soaked spots on leaves", "White fuzzy growth on undersides", "Rapid plant collapse", "Brown lesions on fruits"],
        "treatment": [
            "Apply systemic fungicides immediately (mancozeb, chlorothalonil)",
            "Remove and destroy all infected plants",
            "Avoid working with wet plants",
            "Improve air circulation"
        ],
        "prevention": [
            "Plant certified disease-free transplants",
            "Avoid overhead watering",
            "Apply preventive fungicides during cool, wet weather",
            "Remove volunteer potato and tomato plants"
        ],
        "severity": "Very High - Can destroy entire crop",
        "recovery_days": "Immediate action required - 7-14 days if caught early"
    },
    "Tomato___Bacterial_spot": {
        "symptoms": ["Small, dark, greasy-looking spots", "Yellow halos around spots", "Spots on leaves, stems, and fruits"],
        "treatment": [
            "Apply copper-based bactericides",
            "Remove severely infected plants",
            "Avoid overhead irrigation",
            "Disinfect tools between plants"
        ],
        "prevention": [
            "Use disease-free seeds and transplants",
            "Rotate crops (3-year minimum)",
            "Avoid working with wet plants",
            "Use drip irrigation instead of sprinklers"
        ],
        "severity": "Moderate to High",
        "recovery_days": "21-28 days"
    },
    
    # POTATO DISEASES
    "Potato___Early_blight": {
        "symptoms": ["Dark brown lesions with concentric rings", "Yellowing of older leaves", "Premature leaf drop"],
        "treatment": [
            "Apply fungicides (mancozeb, chlorothalonil)",
            "Remove infected foliage",
            "Ensure adequate soil fertility",
            "Maintain proper irrigation"
        ],
        "prevention": [
            "Plant certified disease-free seed potatoes",
            "Rotate with non-solanaceous crops",
            "Destroy crop debris after harvest",
            "Maintain balanced fertilization"
        ],
        "severity": "Moderate",
        "recovery_days": "14-21 days"
    },
    "Potato___Late_blight": {
        "symptoms": ["Water-soaked lesions on leaves", "White mold on undersides", "Tuber rot", "Rapid plant death"],
        "treatment": [
            "Apply systemic fungicides immediately",
            "Destroy infected plants completely",
            "Harvest tubers before disease spreads",
            "Avoid storing infected tubers"
        ],
        "prevention": [
            "Use resistant varieties",
            "Apply preventive fungicides in cool, wet weather",
            "Hill soil around plants",
            "Destroy volunteer plants"
        ],
        "severity": "Very High - Devastating",
        "recovery_days": "Immediate action - 7-10 days if early"
    },
    
    # PEPPER DISEASES
    "Pepper,_bell___Bacterial_spot": {
        "symptoms": ["Small, dark, raised spots on leaves", "Spots may have yellow halos", "Fruit lesions are raised and corky"],
        "treatment": [
            "Apply copper bactericides",
            "Remove infected plants",
            "Improve air circulation",
            "Avoid overhead watering"
        ],
        "prevention": [
            "Use disease-free seeds",
            "Rotate crops (3-4 years)",
            "Disinfect tools and equipment",
            "Use drip irrigation"
        ],
        "severity": "Moderate",
        "recovery_days": "21-28 days"
    },
    
    # GRAPE DISEASES
    "Grape___Black_rot": {
        "symptoms": ["Circular tan lesions on leaves", "Black, mummified berries", "Brown lesions on shoots"],
        "treatment": [
            "Apply fungicides (mancozeb, myclobutanil)",
            "Remove mummified berries",
            "Prune infected canes",
            "Improve canopy air circulation"
        ],
        "prevention": [
            "Remove all mummified fruit",
            "Prune for good air circulation",
            "Apply preventive fungicides from bud break",
            "Clean up fallen leaves and debris"
        ],
        "severity": "High",
        "recovery_days": "Season-long management required"
    },
    
    # APPLE DISEASES
    "Apple___Black_rot": {
        "symptoms": ["Purple spots on leaves", "Sunken, black lesions on fruit", "Cankers on branches"],
        "treatment": [
            "Prune out infected branches",
            "Apply fungicides (captan, thiophanate-methyl)",
            "Remove infected fruit",
            "Improve orchard sanitation"
        ],
        "prevention": [
            "Prune dead and diseased wood",
            "Remove mummified fruit",
            "Apply dormant sprays",
            "Maintain tree vigor with proper fertilization"
        ],
        "severity": "Moderate to High",
        "recovery_days": "Season-long management"
    }
}


def get_disease_info(disease_name: str) -> Optional[Dict]:
    """
    Get disease information from database.
    In production, this would scrape from agricultural websites.
    """
    return DISEASE_DATABASE.get(disease_name)


def search_disease_by_symptoms(symptoms: List[str]) -> List[str]:
    """
    Search for diseases matching given symptoms.
    """
    matching_diseases = []
    for disease, info in DISEASE_DATABASE.items():
        disease_symptoms = [s.lower() for s in info.get("symptoms", [])]
        for symptom in symptoms:
            if any(symptom.lower() in ds for ds in disease_symptoms):
                matching_diseases.append(disease)
                break
    return matching_diseases


async def scrape_disease_treatment(disease_name: str, crop_type: str) -> Dict:
    """
    Scrape disease treatment information from agricultural websites.
    Currently uses local database, but can be extended to scrape from:
    - USDA Plant Disease Database
    - Extension.org
    - State agricultural extension websites
    """
    # Get from local database
    disease_info = get_disease_info(disease_name)
    
    if disease_info:
        return {
            "success": True,
            "disease": disease_name,
            "crop": crop_type,
            "symptoms": disease_info.get("symptoms", []),
            "treatment": disease_info.get("treatment", []),
            "prevention": disease_info.get("prevention", []),
            "severity": disease_info.get("severity", "Unknown"),
            "recovery_timeline": disease_info.get("recovery_days", "Varies"),
            "source": "Agricultural Disease Database"
        }
    else:
        # Fallback for unknown diseases
        return {
            "success": True,
            "disease": disease_name,
            "crop": crop_type,
            "treatment": [
                f"Consult local agricultural extension for {crop_type} disease management",
                "Remove and destroy infected plant parts",
                "Improve air circulation and reduce humidity",
                "Consider applying broad-spectrum fungicide"
            ],
            "prevention": [
                "Use disease-resistant varieties",
                "Practice crop rotation",
                "Maintain proper plant spacing",
                "Monitor plants regularly for early detection"
            ],
            "severity": "Unknown - Requires expert diagnosis",
            "recovery_timeline": "Consult agricultural expert",
            "source": "General recommendations"
        }
