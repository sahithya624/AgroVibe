"""
Yield Prediction Model Handler
Uses Random Forest Regressor for crop yield forecasting.
"""

import joblib
import pandas as pd
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Crop-specific base yields (tons per hectare)
CROP_BASE_YIELDS = {
    # Cereals
    "Rice": 4.5, "Wheat": 4.0, "Maize": 5.5, "Bajra": 2.0, "Jowar": 1.5,
    "Barley": 3.0, "Oats": 2.5, "Ragi": 1.8,
    
    # Vegetables
    "Tomato": 35.0, "Potato": 25.0, "Onion": 20.0, "Cabbage": 30.0,
    "Cauliflower": 25.0, "Brinjal": 25.0, "Okra": 12.0, "Carrot": 20.0,
    "Radish": 15.0, "Beetroot": 20.0, "Pumpkin": 25.0, "Bitter Gourd": 15.0,
    "Bottle Gourd": 30.0, "Cucumber": 15.0, "Spinach": 10.0, "Coriander": 5.0,
    
    # Fruits
    "Banana": 40.0, "Mango": 15.0, "Grapes": 20.0, "Papaya": 45.0,
    "Guava": 20.0, "Pomegranate": 12.0, "Orange": 15.0,
    "Apple": 15.0, "Watermelon": 30.0, "Muskmelon": 20.0,
    
    # Commercial & Fiber
    "Sugarcane": 70.0, "Cotton": 2.5, "Jute": 2.5,
    "Tea": 2.0, "Coffee": 1.5,
    
    # Pulses
    "Chickpea": 2.0, "Pigeon Pea": 1.5, "Green Gram": 1.0,
    "Black Gram": 1.0, "Lentil": 1.2, "Red Gram": 1.5, "Soybean": 2.8,
    
    # Oilseeds
    "Groundnut": 2.2, "Mustard": 1.8, "Sunflower": 2.5,
    "Sesame": 0.8, "Safflower": 1.2, "Castor": 1.5, "Linseed": 1.0,
    
    # Spices
    "Turmeric": 25.0, "Ginger": 20.0, "Garlic": 10.0,
    "Chili": 3.0, "Black Pepper": 1.0, "Cardamom": 0.5,
    "Cumin": 0.8, "Coriander Seed": 1.2
}

class YieldPredictor:
    def __init__(self, model_path: str = "backend/ml_models/saved_models/yield_rf_model.joblib"):
        self.model_path = model_path
        self.model = self._load_model()
        
    def _load_model(self):
        """Load trained Random Forest model."""
        if os.path.exists(self.model_path):
            try:
                model = joblib.load(self.model_path)
                logger.info(f"Loaded yield model from {self.model_path}")
                return model
            except Exception as e:
                logger.error(f"Error loading yield model: {e}")
        else:
            logger.warning(f"Yield model path {self.model_path} not found. Using simulation logic.")
        return None

    def predict(self, features: Dict[str, Any]) -> float:
        """Perform yield prediction."""
        if self.model:
            try:
                # Convert features to DataFrame for prediction
                df = pd.DataFrame([features])
                prediction = self.model.predict(df)[0]
                return float(prediction)
            except Exception as e:
                logger.error(f"Yield prediction model error: {e}")
        
        # Fallback to simulation logic if model is missing or fails
        return self._simulate_yield(features)

    def _simulate_yield(self, features: Dict[str, Any]) -> float:
        """
        Fallback simulation logic using all input features.
        Ensures different inputs produce different outputs.
        """
        # Get crop-specific base yield
        crop_type = features.get('crop_type', 'Rice')
        base_yield_per_ha = CROP_BASE_YIELDS.get(crop_type, 5.0)
        
        # Soil quality factor (0-100 scale)
        soil_quality = features.get('soil_quality', 70)
        soil_factor = soil_quality / 100
        
        # Temperature factor (optimal around 25°C)
        avg_temp = features.get('avg_temperature', 25)
        temp_factor = 1.0 - abs(25 - avg_temp) / 50
        temp_factor = max(0.5, min(1.2, temp_factor))
        
        # Rainfall factor (optimal around 600mm)
        rainfall = features.get('total_rainfall', 500)
        rain_factor = min(1.3, rainfall / 600)
        rain_factor = max(0.4, rain_factor)
        
        # Fertilizer factor
        fertilizer = features.get('fertilizer_used', 100)
        fert_factor = min(1.25, fertilizer / 150)
        fert_factor = max(0.6, fert_factor)
        
        # Irrigation frequency factor
        irrigation = features.get('irrigation_frequency', 2)
        irrig_factor = min(1.2, irrigation / 3)
        irrig_factor = max(0.7, irrig_factor)
        
        # Field size
        field_size = features.get('field_size', 1.0)
        
        # Calculate total yield
        yield_per_ha = base_yield_per_ha * soil_factor * temp_factor * rain_factor * fert_factor * irrig_factor
        total_yield = yield_per_ha * field_size
        
        return round(total_yield, 2)

_predictor = None

def get_yield_predictor():
    global _predictor
    if _predictor is None:
        _predictor = YieldPredictor()
    return _predictor
