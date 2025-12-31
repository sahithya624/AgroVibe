"""
Soil Health Analyzer Model Handler
Uses Gradient Boosting for soil quality assessment.
"""

import joblib
import pandas as pd
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SoilAnalyzer:
    def __init__(self, model_path: str = "backend/ml_models/saved_models/soil_gb_model.joblib"):
        self.model_path = model_path
        self.model = self._load_model()
        
    def _load_model(self):
        """Load trained Gradient Boosting model."""
        if os.path.exists(self.model_path):
            try:
                model = joblib.load(self.model_path)
                logger.info(f"Loaded soil model from {self.model_path}")
                return model
            except Exception as e:
                logger.error(f"Error loading soil model: {e}")
        else:
            logger.warning(f"Soil model path {self.model_path} not found. Use mock logic for now.")
        return None

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze soil health."""
        if self.model:
            try:
                df = pd.DataFrame([data])
                score = self.model.predict(df)[0]
                return {"health_score": float(score)}
            except Exception as e:
                logger.error(f"Soil analysis model error: {e}")
        
        # Fallback simulation
        n_score = min(100, (data.get('nitrogen', 0) / 350) * 100)
        p_score = min(100, (data.get('phosphorus', 0) / 70) * 100)
        k_score = min(100, (data.get('potassium', 0) / 350) * 100)
        ph = data.get('ph', 7.0)
        ph_score = 100 if 6.0 <= ph <= 7.0 else 70
        
        health_score = (n_score + p_score + k_score + ph_score) / 4
        return {"health_score": round(health_score, 2)}

_analyzer = None

def get_soil_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = SoilAnalyzer()
    return _analyzer
