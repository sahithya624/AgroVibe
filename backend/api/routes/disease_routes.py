from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import Optional
import logging
from backend.services.disease_service import analyze_disease
from backend.api.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/disease-detect")
async def detect_disease(
    image: UploadFile = File(...), 
    crop_type: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Received disease detection request for crop: {crop_type}")
    try:
        result = await analyze_disease(image, crop_type=crop_type)
        logger.info("Disease analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in detect_disease route: {str(e)}", exc_info=True)
        return {"success": False, "error": str(e)}

@router.get("/disease-info/{disease_name}")
async def get_disease_info(disease_name: str, current_user: dict = Depends(get_current_user)):
    return {"disease_name": disease_name, "info": "Disease information"}
