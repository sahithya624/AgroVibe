from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.market_service import get_market_insights
from backend.api.deps import get_current_user

router = APIRouter()

class MarketData(BaseModel):
    crop_type: str
    region: str
    quantity: float

@router.post("/market-insights")
async def market_insights(data: MarketData, current_user: dict = Depends(get_current_user)):
    result = await get_market_insights(data)
    return result
