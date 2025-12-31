"""Utility functions for SmartFarmingAI"""

from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_current_season(date: datetime = None) -> str:
    """Determine current agricultural season based on date."""
    if date is None:
        date = datetime.now()
    
    month = date.month
    
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Fall"
    else:
        return "Winter"


def get_crop_stage(crop_type: str, days_since_planting: int) -> str:
    """Estimate crop growth stage based on planting date."""
    if days_since_planting < 14:
        return "germination"
    elif days_since_planting < 30:
        return "seedling"
    elif days_since_planting < 60:
        return "vegetative"
    elif days_since_planting < 90:
        return "flowering"
    elif days_since_planting < 120:
        return "fruiting"
    else:
        return "maturity"


def get_time_context() -> Dict[str, str]:
    """Get current time context for prompt injection."""
    now = datetime.now()
    
    return {
        "current_date": now.strftime("%Y-%m-%d"),
        "current_time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "month": now.strftime("%B"),
        "season": get_current_season(now),
        "year": str(now.year)
    }


def build_context_string(data: Dict[str, Any]) -> str:
    """Build formatted context string from data dictionary."""
    lines = []
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').title()
        
        if isinstance(value, dict):
            lines.append(f"{formatted_key}:")
            for sub_key, sub_value in value.items():
                sub_formatted = sub_key.replace('_', ' ').title()
                lines.append(f"  - {sub_formatted}: {sub_value}")
        elif isinstance(value, list):
            lines.append(f"{formatted_key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{formatted_key}: {value}")
    
    return "\n".join(lines)


def format_price_trends(price_data: Dict[str, Any]) -> str:
    """Format market price trends for LLM context."""
    current = price_data.get('current_price', 0)
    avg_30d = price_data.get('avg_30_day', 0)
    avg_90d = price_data.get('avg_90_day', 0)
    min_price = price_data.get('min_90_day', 0)
    max_price = price_data.get('max_90_day', 0)
    
    return f"""
  - Current Price: ${current}/ton
  - 30-day Average: ${avg_30d}/ton
  - 90-day Average: ${avg_90d}/ton
  - 90-day Range: ${min_price} - ${max_price}
    """.strip()
