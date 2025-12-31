"""
Soil Health Service with Dynamic AI Analysis

Uses Groq LLM for intelligent fertilizer recommendations and soil health optimization.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from backend.services.llm_client import get_groq_client, TaskType
from backend.services.prompts import get_expert_prompt
from backend.services.utils import get_time_context, build_context_string
from backend.ml_models.soil_analyzer import get_soil_analyzer

logger = logging.getLogger(__name__)


async def analyze_soil_health(data: Any) -> Dict[str, Any]:
    """
    Analyze soil health using Groq LLM for dynamic, context-aware analysis.
    """
    try:
        time_ctx = get_time_context()
        
        # Build comprehensive context for LLM
        context_data = {
            "soil_parameters": {
                "nitrogen": data.nitrogen,
                "phosphorus": data.phosphorus,
                "potassium": data.potassium,
                "ph": data.ph
            },
            "crop_type": data.crop_type,
            "field_size": data.field_size,
            "season": time_ctx["season"],
            "region": getattr(data, 'region', 'India')
        }
        
        # Use LLM for comprehensive soil analysis
        user_prompt = f"""
Analyze the soil health for {data.crop_type} cultivation based on these parameters:
- Nitrogen (N): {data.nitrogen} kg/ha
- Phosphorus (P): {data.phosphorus} kg/ha
- Potassium (K): {data.potassium} kg/ha
- pH Level: {data.ph}
- Field Size: {data.field_size} hectares
- Season: {time_ctx['season']}

Provide a detailed analysis including:
1. Overall soil health score (0-100)
2. Status of each nutrient (Optimal/Moderate/Deficient)
3. pH assessment
4. Specific fertilizer recommendations with quantities
5. Application timing and methods
6. Expected improvement timeline
"""
        
        groq_client = get_groq_client()
        response = await groq_client.generate_structured(
            system_prompt=get_expert_prompt("soil"),
            user_prompt=user_prompt,
            context=build_context_string(context_data),
            schema={
                "health_score": "integer (0-100)",
                "status": "string (Excellent/Good/Fair/Poor)",
                "nitrogen_status": "string",
                "phosphorus_status": "string",
                "potassium_status": "string",
                "ph_status": "string",
                "fertilizer_recommendations": "list of objects with {nutrient, quantity_kg_per_ha, timing}",
                "application_method": "string",
                "monitoring_tips": "list of strings",
                "expected_improvement_days": "integer"
            },
            task_type=TaskType.DEEP_ANALYSIS
        )
        
        # Extract and structure the response
        return {
            "success": True,
            "health_score": response.get("health_score", 70),
            "status": response.get("status", "Good"),
            "npk_status": {
                "nitrogen": response.get("nitrogen_status", "Moderate"),
                "phosphorus": response.get("phosphorus_status", "Moderate"),
                "potassium": response.get("potassium_status", "Moderate")
            },
            "ph_status": response.get("ph_status", "Optimal"),
            "recommendations": response.get("fertilizer_recommendations", []),
            "application_method": response.get("application_method", ""),
            "monitoring_tips": response.get("monitoring_tips", []),
            "expected_improvement_days": response.get("expected_improvement_days", 30),
            "context_used": {
                "season": time_ctx["season"],
                "crop": data.crop_type,
                "field_size": data.field_size
            }
        }
    except Exception as e:
        logger.error(f"Soil health analysis error: {str(e)}")
        # Fallback to basic analysis
        return get_fallback_soil_analysis(data)


async def get_fertilizer_advice(data: Any) -> Dict[str, Any]:
    """
    Get dynamic fertilizer advice - wrapper for analyze_soil_health.
    """
    return await analyze_soil_health(data)


def get_fallback_soil_analysis(data: Any) -> Dict[str, Any]:
    """Fallback analysis when LLM is unavailable."""
    # Calculate basic health score
    n_score = min(100, (data.nitrogen / 300) * 100)
    p_score = min(100, (data.phosphorus / 80) * 100)
    k_score = min(100, (data.potassium / 300) * 100)
    ph_score = 100 if 6.0 <= data.ph <= 7.0 else 70
    
    health_score = int((n_score + p_score + k_score + ph_score) / 4)
    
    return {
        "success": True,
        "health_score": health_score,
        "status": "Good" if health_score >= 70 else "Fair",
        "npk_status": {
            "nitrogen": "Optimal" if data.nitrogen >= 280 else "Deficient",
            "phosphorus": "Optimal" if data.phosphorus >= 60 else "Deficient",
            "potassium": "Optimal" if data.potassium >= 280 else "Deficient"
        },
        "ph_status": "Optimal" if 6.0 <= data.ph <= 7.0 else "Needs Adjustment",
        "recommendations": [
            {"nutrient": "Nitrogen", "quantity_kg_per_ha": max(0, 300 - data.nitrogen), "timing": "Pre-planting"},
            {"nutrient": "Phosphorus", "quantity_kg_per_ha": max(0, 80 - data.phosphorus), "timing": "At sowing"},
            {"nutrient": "Potassium", "quantity_kg_per_ha": max(0, 300 - data.potassium), "timing": "Split application"}
        ],
        "application_method": "Broadcast and incorporate into soil",
        "monitoring_tips": ["Monitor plant growth weekly", "Test soil after 30 days"],
        "expected_improvement_days": 30,
        "context_used": {
            "season": "Current",
            "crop": data.crop_type,
            "field_size": data.field_size
        }
    }
