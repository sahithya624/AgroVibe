"""Market Data Adapter for SmartFarmingAI"""

import logging
from datetime import datetime
from typing import Dict, Any, List
import random

from backend.config import settings

logger = logging.getLogger(__name__)


async def get_current_market_price(crop_type: str, region: str = "North America") -> Dict[str, Any]:
    """Get current market price for crop in specified region."""
    return get_mock_current_price(crop_type, region)


async def get_price_trends(crop_type: str, region: str = "North America", days: int = 90) -> Dict[str, Any]:
    """Get historical price trends."""
    return get_mock_price_trends(crop_type, region, days)


async def get_regional_comparison(crop_type: str, regions: List[str]) -> Dict[str, float]:
    """Compare prices across multiple regions."""
    comparison = {}
    
    for region in regions:
        price_data = await get_current_market_price(crop_type, region)
        comparison[region] = price_data.get("current_price", 0)
    
    return comparison


def get_mock_current_price(crop_type: str, region: str) -> Dict[str, Any]:
    """Generate realistic mock price with time-based variation."""
    base_prices = {
        "tomato": 450, "corn": 180, "wheat": 250, "rice": 400, "potato": 300,
        "soybean": 420, "cotton": 1500, "lettuce": 600, "carrot": 350, "onion": 280
    }
    
    base_price = base_prices.get(crop_type.lower(), 400)
    
    regional_multipliers = {
        "North America": 1.0, "California": 1.15, "Florida": 1.05, "Midwest": 0.95,
        "Europe": 1.25, "Asia": 0.85, "India": 0.75, "South America": 0.90
    }
    
    regional_mult = regional_multipliers.get(region, 1.0)
    
    day_of_year = datetime.now().timetuple().tm_yday
    seasonal_factor = 1.0 + 0.15 * (day_of_year % 30) / 30
    
    daily_fluctuation = random.uniform(0.95, 1.05)
    
    current_price = base_price * regional_mult * seasonal_factor * daily_fluctuation
    
    return {
        "current_price": round(current_price, 2),
        "currency": "USD",
        "unit": "ton",
        "region": region,
        "crop_type": crop_type,
        "timestamp": datetime.now().isoformat(),
        "source": "mock_data"
    }


def get_mock_price_trends(crop_type: str, region: str, days: int) -> Dict[str, Any]:
    """Generate realistic mock price trends."""
    current_price_data = get_mock_current_price(crop_type, region)
    current_price = current_price_data["current_price"]
    
    prices = []
    base_trend = random.choice([-0.002, 0.002])
    
    for i in range(days, 0, -1):
        historical_price = current_price * (1 - base_trend * i)
        noise = random.uniform(-0.05, 0.05)
        price = historical_price * (1 + noise)
        prices.append(price)
    
    prices.reverse()
    
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)
    
    avg_30_day = sum(prices[-30:]) / 30 if len(prices) >= 30 else avg_price
    avg_60_day = sum(prices[-60:]) / 60 if len(prices) >= 60 else avg_price
    avg_90_day = sum(prices[-90:]) / 90 if len(prices) >= 90 else avg_price
    
    change_30d = ((current_price - avg_30_day) / avg_30_day) * 100 if avg_30_day > 0 else 0
    change_60d = ((current_price - avg_60_day) / avg_60_day) * 100 if avg_60_day > 0 else 0
    change_90d = ((current_price - avg_90_day) / avg_90_day) * 100 if avg_90_day > 0 else 0
    
    return {
        "current_price": current_price,
        "min_90_day": round(min_price, 2),
        "max_90_day": round(max_price, 2),
        "avg_30_day": round(avg_30_day, 2),
        "avg_60_day": round(avg_60_day, 2),
        "avg_90_day": round(avg_90_day, 2),
        "change_30d": round(change_30d, 2),
        "change_60d": round(change_60d, 2),
        "change_90d": round(change_90d, 2),
        "volatility": round(((max_price - min_price) / avg_price) * 100, 2),
        "trend": "bullish" if change_30d > 2 else "bearish" if change_30d < -2 else "stable",
        "prices_history": prices[-30:],
        "source": "mock_data"
    }


def get_nearby_regions(region: str) -> List[str]:
    """Get list of nearby regions for comparison."""
    region_groups = {
        "California": ["California", "Arizona", "Nevada", "Oregon"],
        "Florida": ["Florida", "Georgia", "Alabama", "South Carolina"],
        "Midwest": ["Midwest", "Illinois", "Iowa", "Nebraska"],
        "North America": ["North America", "California", "Midwest", "Florida"],
        "India": ["India", "Maharashtra", "Punjab", "Karnataka"],
        "Europe": ["Europe", "France", "Germany", "Spain"]
    }
    
    return region_groups.get(region, ["North America", "California", "Midwest"])
