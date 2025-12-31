from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.yield_service import predict_yield
from backend.api.deps import get_current_user

router = APIRouter()

class YieldData(BaseModel):
    crop_type: str
    field_size: float
    soil_quality: float
    avg_temperature: float
    total_rainfall: float
    fertilizer_used: float
    irrigation_frequency: float

@router.post("/yield-predict")
async def yield_predict(data: YieldData, current_user: dict = Depends(get_current_user)):
    result = await predict_yield(data)
    return result
