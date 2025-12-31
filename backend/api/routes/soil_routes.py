from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.soil_service import analyze_soil_health, get_fertilizer_advice
from backend.api.deps import get_current_user

router = APIRouter()

class SoilData(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    crop_type: str
    field_size: float

@router.post("/soil-advice")
async def soil_advice(data: SoilData, current_user: dict = Depends(get_current_user)):
    result = await get_fertilizer_advice(data)
    return result

@router.post("/soil-health")
async def soil_health(data: SoilData, current_user: dict = Depends(get_current_user)):
    result = await analyze_soil_health(data)
    return result
