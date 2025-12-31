"""Crop Database for SmartFarmingAI"""

from typing import Dict, Any, List


CROP_GROWTH_STAGES = {
    "tomato": {"germination": (0, 14), "seedling": (14, 30), "vegetative": (30, 50), "flowering": (50, 70), "fruiting": (70, 90), "maturity": (90, 120)},
    "corn": {"germination": (0, 10), "seedling": (10, 25), "vegetative": (25, 55), "flowering": (55, 75), "grain_fill": (75, 100), "maturity": (100, 130)},
    "wheat": {"germination": (0, 14), "tillering": (14, 40), "stem_extension": (40, 70), "heading": (70, 90), "grain_fill": (90, 110), "maturity": (110, 140)},
    "rice": {"germination": (0, 15), "seedling": (15, 35), "tillering": (35, 60), "panicle_initiation": (60, 80), "flowering": (80, 100), "maturity": (100, 130)},
    "potato": {"sprouting": (0, 14), "vegetative": (14, 40), "tuber_initiation": (40, 60), "tuber_bulking": (60, 90), "maturity": (90, 120)}
}

WATER_REQUIREMENTS = {
    "tomato": {"germination": 3, "seedling": 4, "vegetative": 5, "flowering": 6, "fruiting": 7, "maturity": 5},
    "corn": {"germination": 3, "seedling": 4, "vegetative": 5, "flowering": 7, "grain_fill": 6, "maturity": 4},
    "wheat": {"germination": 2, "tillering": 3, "stem_extension": 4, "heading": 5, "grain_fill": 4, "maturity": 2},
    "rice": {"germination": 8, "seedling": 9, "tillering": 10, "panicle_initiation": 11, "flowering": 10, "maturity": 8},
    "potato": {"sprouting": 3, "vegetative": 4, "tuber_initiation": 5, "tuber_bulking": 6, "maturity": 4}
}


def get_crop_stage(crop_type: str, days_since_planting: int) -> str:
    """Determine current growth stage based on days since planting."""
    crop_type = crop_type.lower()
    
    if crop_type not in CROP_GROWTH_STAGES:
        if days_since_planting < 14:
            return "early_growth"
        elif days_since_planting < 60:
            return "vegetative"
        elif days_since_planting < 90:
            return "reproductive"
        else:
            return "maturity"
    
    stages = CROP_GROWTH_STAGES[crop_type]
    
    for stage_name, (start_day, end_day) in stages.items():
        if start_day <= days_since_planting < end_day:
            return stage_name
    
    return list(stages.keys())[-1]


def get_water_requirement(crop_type: str, growth_stage: str) -> float:
    """Get water requirement for crop at specific growth stage."""
    crop_type = crop_type.lower()
    
    if crop_type not in WATER_REQUIREMENTS:
        return 5.0
    
    requirements = WATER_REQUIREMENTS[crop_type]
    return requirements.get(growth_stage, 5.0)


def get_common_diseases(crop_type: str, season: str = None) -> List[str]:
    """Get common diseases for crop."""
    disease_database = {
        "tomato": ["Late Blight", "Early Blight", "Septoria Leaf Spot", "Bacterial Spot", "Fusarium Wilt"],
        "corn": ["Common Rust", "Northern Corn Leaf Blight", "Gray Leaf Spot", "Southern Corn Leaf Blight"],
        "wheat": ["Wheat Rust", "Powdery Mildew", "Septoria Tritici Blotch", "Fusarium Head Blight"],
        "rice": ["Rice Blast", "Bacterial Leaf Blight", "Sheath Blight", "Brown Spot"],
        "potato": ["Late Blight", "Early Blight", "Potato Virus Y", "Blackleg", "Common Scab"]
    }
    
    crop_type = crop_type.lower()
    return disease_database.get(crop_type, ["General Fungal Disease", "Bacterial Infection"])
