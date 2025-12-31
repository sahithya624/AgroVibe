"""
Market Insights Service with Dynamic AI Analysis

Uses Groq LLM with real-time market data for intelligent selling strategies.
Pricing in Indian Rupees (INR) per quintal.
"""

import logging
from typing import Dict, Any, Optional

from backend.services.llm_client import get_groq_client, TaskType
from backend.services.prompts import get_expert_prompt
from backend.services.utils import get_time_context
from backend.services.market_adapter import get_current_market_price, get_price_trends, get_regional_comparison, get_nearby_regions

logger = logging.getLogger(__name__)

# Currency conversion (approximate, should be updated from live rates)
USD_TO_INR = 83.0


async def get_market_insights(data: Any, location: str = None) -> Dict[str, Any]:
    """
    Get market insights with dynamic AI analysis.
    Prices returned in INR per quintal.
    """
    try:
        region = location or data.region
        
        # Get market data
        current_price_data = await get_current_market_price(data.crop_type, region)
        price_trends = await get_price_trends(data.crop_type, region, days=90)
        
        # Regional comparison
        nearby_regions = get_nearby_regions(region)
        regional_prices = await get_regional_comparison(data.crop_type, nearby_regions)
        
        # Time context
        time_ctx = get_time_context()
        
        # Convert USD/ton to INR/quintal (1 ton = 10 quintals)
        current_price_usd = current_price_data.get('current_price', 1000)
        current_price_inr = int((current_price_usd * USD_TO_INR) / 10)  # Convert to INR per quintal
        
        # LLM Context
        context_str = f"""
Crop: {data.crop_type}
Quantity: {data.quantity} quintals
Region: {region}
Current Price: ₹{current_price_inr}/quintal
Trend: {price_trends.get('trend')}
Volatility: {price_trends.get('volatility')}%
Season: {time_ctx['season']}
        """
        
        # Generate dynamic strategy with LLM
        user_prompt = f"Analyze market conditions for {data.quantity} quintals of {data.crop_type} in {region} and provide a selling strategy with Indian market context."
        
        groq_client = get_groq_client()
        strategy = await groq_client.generate_structured(
            system_prompt=get_expert_prompt("market"),
            user_prompt=user_prompt,
            context=context_str,
            schema={
                "price_forecast_inr": "integer (price in INR per quintal)",
                "demand_level": "string",
                "best_selling_window": "string",
                "recommended_mandis": "list of strings (Indian market names)",
                "selling_strategy": "string",
                "risk_assessment": "string"
            },
            task_type=TaskType.DEEP_ANALYSIS
        )
        
        return {
            "success": True,
            "current_price": current_price_inr,
            "price_unit": "INR/quintal",
            "trend": price_trends.get("trend", "stable"),
            "percent_change": price_trends.get("volatility", 0),
            "forecast": f"₹{strategy.get('price_forecast_inr', current_price_inr)}/quintal",
            "demand_level": strategy.get("demand_level", "Moderate"),
            "best_market": strategy.get("recommended_mandis", [region])[0] if strategy.get("recommended_mandis") else region,
            "recommendation": strategy.get("selling_strategy", ""),
            "risk_factors": [strategy.get("risk_assessment", "No major risks")] if isinstance(strategy.get("risk_assessment"), str) else strategy.get("risk_assessment", []),
            "historical_data": price_trends.get("historical", [
                {"date": "1 Mar", "price": int(current_price_inr * 0.9)},
                {"date": "10 Mar", "price": int(current_price_inr * 0.95)},
                {"date": "20 Mar", "price": current_price_inr},
                {"date": "30 Mar", "price": int(current_price_inr * 1.05)},
            ]),
            "context_used": {
                "season": time_ctx["season"],
                "data_source": current_price_data.get("source", "real_time"),
                "currency": "INR",
                "unit": "quintal"
            }
        }
        
    except Exception as e:
        logger.error(f"Market insights error: {str(e)}")
        return {"success": False, "error": str(e)}
