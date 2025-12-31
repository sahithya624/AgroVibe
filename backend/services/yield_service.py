"""
Yield Prediction Service with Dynamic AI Analysis

Uses Groq LLM for context-aware yield forecasting and optimization recommendations.
"""

import logging
from typing import Dict, Any, Optional
import random

from backend.services.llm_client import get_groq_client, TaskType
from backend.services.prompts import get_expert_prompt
from backend.services.utils import get_time_context
from backend.services.weather_service import get_weather_data
from backend.ml_models.yield_model import get_yield_predictor

logger = logging.getLogger(__name__)


async def predict_yield(data: Any, location: str = "North America") -> Dict[str, Any]:
    """
    Predict crop yield with dynamic AI analysis.
    """
    try:
        # Calculate base yield using ML model
        predictor = get_yield_predictor()
        features = {
            "crop_type": data.crop_type,
            "field_size": data.field_size,
            "soil_quality": data.soil_quality,
            "avg_temperature": data.avg_temperature,
            "total_rainfall": data.total_rainfall,
            "fertilizer_used": data.fertilizer_used,
            "irrigation_frequency": data.irrigation_frequency
        }
        base_yield = predictor.predict(features)
        
        # Calculate confidence based on data quality
        confidence = calculate_confidence(data)
        
        # Get context
        weather = await get_weather_data(location=location)
        time_ctx = get_time_context()
        
        # Build context for LLM
        context_str = f"""
Crop: {data.crop_type}
Field Size: {data.field_size} ha
Soil Quality: {data.soil_quality}/100
Avg Temp: {data.avg_temperature}°C
Rainfall: {data.total_rainfall} mm
Fertilizer: {data.fertilizer_used} kg/ha
Season: {time_ctx['season']}
Weather: {weather.get('description')}
        """
        
        # Generate dynamic analysis with LLM
        user_prompt = f"""
Analyze this yield prediction for {data.crop_type}. 
Identify risk factors and optimization recommendations.
Predicted yield is {round(base_yield, 2)} tons.
        """
        
        groq_client = get_groq_client()
        analysis = await groq_client.generate_structured(
            system_prompt=get_expert_prompt("yield"),
            user_prompt=user_prompt,
            context=context_str,
            schema={
                "quality_grade": "string (A/B/C/D)",
                "risk_factors": "list of strings",
                "recommendations": "list of strings",
                "revenue_estimate": "float",
                "confidence_reasoning": "string"
            },
            task_type=TaskType.DEEP_ANALYSIS
        )
        
        return {
            "success": True,
            "predicted_yield": round(base_yield, 2),
            "yield_unit": "tons",
            "quality_grade": analysis.get("quality_grade", "B"),
            "confidence_score": round(confidence, 2),
            "risk_factors": analysis.get("risk_factors", []),
            "recommendations": analysis.get("recommendations", []),
            "revenue_estimate": analysis.get("revenue_estimate", 0),
            "confidence_reasoning": analysis.get("confidence_reasoning", ""),
            "context_used": {
                "season": time_ctx["season"],
                "weather": weather.get("description")
            }
        }
        
    except Exception as e:
        logger.error(f"Yield prediction error: {str(e)}")
        return {"success": False, "error": str(e)}


def calculate_base_yield(data: Any) -> float:
    """Calculate base yield using simplified ML model simulation"""
    base_yield_per_ha = 5.0  # tons per hectare
    
    # Factors affecting yield
    soil_factor = data.soil_quality / 100
    rainfall_factor = min(1.2, data.total_rainfall / 600)
    fertilizer_factor = min(1.3, data.fertilizer_used / 150)
    irrigation_factor = min(1.2, data.irrigation_frequency / 3)
    
    yield_multiplier = soil_factor * rainfall_factor * fertilizer_factor * irrigation_factor
    total_yield = base_yield_per_ha * yield_multiplier * data.field_size
    
    # Add random variation
    total_yield *= random.uniform(0.95, 1.05)
    
    return total_yield


def calculate_confidence(data: Any) -> float:
    """Calculate prediction confidence based on data consistency"""
    confidence = 0.70  # Base
    if 60 <= data.soil_quality <= 90: confidence += 0.05
    if 400 <= data.total_rainfall <= 800: confidence += 0.05
    if 100 <= data.fertilizer_used <= 200: confidence += 0.05
    
    return min(0.98, max(0.65, confidence))
