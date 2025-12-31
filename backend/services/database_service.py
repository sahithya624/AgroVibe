import os
import logging
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from backend.config import settings

logger = logging.getLogger(__name__)

# Supabase client (for storage, auth, realtime)
supabase_url = settings.SUPABASE_URL
supabase_key = settings.SUPABASE_KEY

supabase: Optional[Client] = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

async def get_db():
    """Returns the supabase client if initialized."""
    return supabase

# Helper functions for database operations

async def save_disease_detection(
    user_id: str,
    crop_type: str,
    disease_name: str,
    confidence_score: float,
    image_url: str,
    treatment: str,
    severity: str
):
    """Save disease detection to Supabase"""
    if not supabase or not settings.ENABLE_REAL_DB:
        logger.warning("Supabase not initialized or real DB disabled. Skipping save.")
        return {"success": False, "error": "Database not available"}
        
    try:
        result = supabase.table("disease_detections").insert({
            "user_id": user_id,
            "crop_type": crop_type,
            "disease_name": disease_name,
            "confidence_score": confidence_score,
            "image_url": image_url,
            "treatment_recommendation": treatment,
            "severity": severity
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"Error saving disease detection: {e}")
        return {"success": False, "error": str(e)}

async def get_disease_history(user_id: str, limit: int = 10):
    """Get user's disease detection history"""
    if not supabase or not settings.ENABLE_REAL_DB:
        return {"success": False, "error": "Database not available"}
        
    try:
        result = supabase.table("disease_detections")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("detection_date", desc=True)\
            .limit(limit)\
            .execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"Error fetching disease history: {e}")
        return {"success": False, "error": str(e)}

async def save_soil_analysis(
    user_id: str,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    crop_type: str,
    field_size: float,
    soil_health_score: float,
    recommendations: dict,
    advisory: str
):
    """Save soil analysis to Supabase"""
    if not supabase or not settings.ENABLE_REAL_DB:
        return {"success": False, "error": "Database not available"}
        
    try:
        result = supabase.table("soil_analyses").insert({
            "user_id": user_id,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph,
            "crop_type": crop_type,
            "field_size": field_size,
            "soil_health_score": soil_health_score,
            "fertilizer_recommendations": recommendations,
            "advisory": advisory
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"Error saving soil analysis: {e}")
        return {"success": False, "error": str(e)}

async def create_notification(
    user_id: str,
    title: str,
    message: str,
    notification_type: str,
    severity: str = "info"
):
    """Create a notification for user"""
    if not supabase or not settings.ENABLE_REAL_DB:
        return {"success": False, "error": "Database not available"}
        
    try:
        result = supabase.table("notifications").insert({
            "user_id": user_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "severity": severity
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        return {"success": False, "error": str(e)}
