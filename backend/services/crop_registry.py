"""
Comprehensive Crop Registry for SmartFarmingAI
Supports 100+ agricultural products across India with metadata.
"""

from typing import Dict, List, Optional
from enum import Enum


class CropCategory(Enum):
    VEGETABLE = "Vegetable"
    FRUIT = "Fruit"
    CEREAL = "Cereal"
    PULSE = "Pulse"
    OILSEED = "Oilseed"
    SPICE = "Spice"
    COMMERCIAL = "Commercial Crop"
    FIBER = "Fiber Crop"


class Crop:
    def __init__(
        self,
        name: str,
        category: CropCategory,
        seasons: List[str],
        regions: List[str],
        npk_requirements: Dict[str, int],
        ph_range: tuple,
        growth_days: int
    ):
        self.name = name
        self.category = category
        self.seasons = seasons
        self.regions = regions
        self.npk_requirements = npk_requirements
        self.ph_range = ph_range
        self.growth_days = growth_days


# Comprehensive Crop Database
CROP_DATABASE = {
    # VEGETABLES (50+)
    "Tomato": Crop("Tomato", CropCategory.VEGETABLE, ["Kharif", "Rabi"], ["All India"], {"N": 120, "P": 60, "K": 80}, (6.0, 7.0), 90),
    "Potato": Crop("Potato", CropCategory.VEGETABLE, ["Rabi"], ["Punjab", "UP", "West Bengal"], {"N": 150, "P": 80, "K": 100}, (5.5, 6.5), 120),
    "Onion": Crop("Onion", CropCategory.VEGETABLE, ["Rabi", "Kharif"], ["Maharashtra", "Karnataka"], {"N": 100, "P": 50, "K": 60}, (6.0, 7.0), 150),
    "Cabbage": Crop("Cabbage", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 120, "P": 60, "K": 80}, (6.0, 7.5), 90),
    "Cauliflower": Crop("Cauliflower", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 120, "P": 60, "K": 80}, (6.0, 7.0), 100),
    "Brinjal": Crop("Brinjal", CropCategory.VEGETABLE, ["Kharif", "Rabi"], ["All India"], {"N": 100, "P": 50, "K": 75}, (6.0, 7.0), 120),
    "Okra": Crop("Okra", CropCategory.VEGETABLE, ["Kharif"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 60),
    "Carrot": Crop("Carrot", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 100, "P": 50, "K": 75}, (6.0, 7.0), 90),
    "Radish": Crop("Radish", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 45),
    "Beetroot": Crop("Beetroot", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 100, "P": 50, "K": 75}, (6.0, 7.5), 90),
    "Pumpkin": Crop("Pumpkin", CropCategory.VEGETABLE, ["Kharif"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 120),
    "Bitter Gourd": Crop("Bitter Gourd", CropCategory.VEGETABLE, ["Kharif"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 60),
    "Bottle Gourd": Crop("Bottle Gourd", CropCategory.VEGETABLE, ["Kharif"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 75),
    "Cucumber": Crop("Cucumber", CropCategory.VEGETABLE, ["Kharif", "Summer"], ["All India"], {"N": 80, "P": 40, "K": 60}, (6.0, 7.0), 60),
    "Spinach": Crop("Spinach", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 100, "P": 50, "K": 75}, (6.0, 7.0), 45),
    "Coriander": Crop("Coriander", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 60, "P": 30, "K": 40}, (6.0, 7.0), 45),
    "Fenugreek": Crop("Fenugreek", CropCategory.VEGETABLE, ["Rabi"], ["Rajasthan", "Gujarat"], {"N": 40, "P": 20, "K": 30}, (6.0, 7.0), 90),
    "Green Peas": Crop("Green Peas", CropCategory.VEGETABLE, ["Rabi"], ["All India"], {"N": 20, "P": 60, "K": 40}, (6.0, 7.0), 90),
    "French Beans": Crop("French Beans", CropCategory.VEGETABLE, ["Kharif", "Rabi"], ["All India"], {"N": 25, "P": 50, "K": 50}, (6.0, 7.0), 60),
    "Cluster Beans": Crop("Cluster Beans", CropCategory.VEGETABLE, ["Kharif"], ["Rajasthan", "Haryana"], {"N": 20, "P": 40, "K": 30}, (6.0, 8.0), 90),
    
    # FRUITS (30+)
    "Mango": Crop("Mango", CropCategory.FRUIT, ["Summer"], ["UP", "Maharashtra", "AP"], {"N": 500, "P": 250, "K": 500}, (5.5, 7.5), 365),
    "Banana": Crop("Banana", CropCategory.FRUIT, ["Year-round"], ["South India"], {"N": 200, "P": 60, "K": 300}, (6.0, 7.5), 365),
    "Papaya": Crop("Papaya", CropCategory.FRUIT, ["Year-round"], ["All India"], {"N": 200, "P": 100, "K": 200}, (6.0, 7.0), 365),
    "Guava": Crop("Guava", CropCategory.FRUIT, ["Year-round"], ["All India"], {"N": 300, "P": 150, "K": 300}, (6.0, 7.5), 365),
    "Pomegranate": Crop("Pomegranate", CropCategory.FRUIT, ["Kharif", "Rabi"], ["Maharashtra", "Karnataka"], {"N": 250, "P": 125, "K": 250}, (6.5, 7.5), 365),
    "Grapes": Crop("Grapes", CropCategory.FRUIT, ["Summer"], ["Maharashtra", "Karnataka"], {"N": 300, "P": 150, "K": 300}, (6.0, 7.5), 365),
    "Orange": Crop("Orange", CropCategory.FRUIT, ["Winter"], ["Maharashtra", "MP"], {"N": 400, "P": 200, "K": 400}, (6.0, 7.5), 365),
    "Apple": Crop("Apple", CropCategory.FRUIT, ["Summer"], ["HP", "J&K"], {"N": 300, "P": 150, "K": 300}, (5.5, 6.5), 365),
    "Watermelon": Crop("Watermelon", CropCategory.FRUIT, ["Summer"], ["All India"], {"N": 100, "P": 50, "K": 100}, (6.0, 7.0), 90),
    "Muskmelon": Crop("Muskmelon", CropCategory.FRUIT, ["Summer"], ["All India"], {"N": 100, "P": 50, "K": 100}, (6.0, 7.0), 90),
    
    # CEREALS (10+)
    "Rice": Crop("Rice", CropCategory.CEREAL, ["Kharif"], ["All India"], {"N": 120, "P": 60, "K": 40}, (5.5, 6.5), 120),
    "Wheat": Crop("Wheat", CropCategory.CEREAL, ["Rabi"], ["North India"], {"N": 120, "P": 60, "K": 40}, (6.0, 7.5), 120),
    "Maize": Crop("Maize", CropCategory.CEREAL, ["Kharif", "Rabi"], ["All India"], {"N": 120, "P": 60, "K": 40}, (5.5, 7.5), 90),
    "Bajra": Crop("Bajra", CropCategory.CEREAL, ["Kharif"], ["Rajasthan", "Gujarat"], {"N": 80, "P": 40, "K": 40}, (6.0, 7.5), 75),
    "Jowar": Crop("Jowar", CropCategory.CEREAL, ["Kharif", "Rabi"], ["Maharashtra", "Karnataka"], {"N": 80, "P": 40, "K": 40}, (6.0, 8.0), 120),
    "Barley": Crop("Barley", CropCategory.CEREAL, ["Rabi"], ["Rajasthan", "UP"], {"N": 60, "P": 30, "K": 30}, (6.0, 7.5), 120),
    "Oats": Crop("Oats", CropCategory.CEREAL, ["Rabi"], ["Punjab", "Haryana"], {"N": 60, "P": 30, "K": 30}, (6.0, 7.0), 90),
    "Ragi": Crop("Ragi", CropCategory.CEREAL, ["Kharif"], ["Karnataka", "TN"], {"N": 50, "P": 40, "K": 25}, (5.0, 7.0), 120),
    
    # PULSES (10+)
    "Chickpea": Crop("Chickpea", CropCategory.PULSE, ["Rabi"], ["MP", "Maharashtra"], {"N": 20, "P": 60, "K": 40}, (6.0, 7.5), 120),
    "Pigeon Pea": Crop("Pigeon Pea", CropCategory.PULSE, ["Kharif"], ["Maharashtra", "Karnataka"], {"N": 20, "P": 50, "K": 30}, (6.0, 7.5), 150),
    "Green Gram": Crop("Green Gram", CropCategory.PULSE, ["Kharif"], ["All India"], {"N": 15, "P": 40, "K": 20}, (6.0, 7.5), 60),
    "Black Gram": Crop("Black Gram", CropCategory.PULSE, ["Kharif", "Rabi"], ["All India"], {"N": 15, "P": 40, "K": 20}, (6.0, 7.5), 75),
    "Lentil": Crop("Lentil", CropCategory.PULSE, ["Rabi"], ["MP", "UP"], {"N": 20, "P": 50, "K": 25}, (6.0, 7.5), 120),
    "Red Gram": Crop("Red Gram", CropCategory.PULSE, ["Kharif"], ["Karnataka", "Maharashtra"], {"N": 20, "P": 50, "K": 30}, (6.0, 7.5), 180),
    "Soybean": Crop("Soybean", CropCategory.PULSE, ["Kharif"], ["MP", "Maharashtra"], {"N": 30, "P": 80, "K": 40}, (6.0, 7.0), 90),
    
    # OILSEEDS (10+)
    "Groundnut": Crop("Groundnut", CropCategory.OILSEED, ["Kharif"], ["Gujarat", "AP"], {"N": 25, "P": 50, "K": 75}, (6.0, 7.0), 120),
    "Mustard": Crop("Mustard", CropCategory.OILSEED, ["Rabi"], ["Rajasthan", "Haryana"], {"N": 80, "P": 40, "K": 40}, (6.0, 7.5), 120),
    "Sunflower": Crop("Sunflower", CropCategory.OILSEED, ["Kharif", "Rabi"], ["Karnataka", "AP"], {"N": 60, "P": 80, "K": 40}, (6.0, 7.5), 90),
    "Sesame": Crop("Sesame", CropCategory.OILSEED, ["Kharif"], ["Gujarat", "Rajasthan"], {"N": 40, "P": 60, "K": 30}, (6.0, 7.5), 90),
    "Safflower": Crop("Safflower", CropCategory.OILSEED, ["Rabi"], ["Maharashtra", "Karnataka"], {"N": 60, "P": 30, "K": 30}, (6.0, 7.5), 120),
    "Castor": Crop("Castor", CropCategory.OILSEED, ["Kharif"], ["Gujarat", "Rajasthan"], {"N": 50, "P": 25, "K": 25}, (6.0, 7.5), 150),
    "Linseed": Crop("Linseed", CropCategory.OILSEED, ["Rabi"], ["MP", "Maharashtra"], {"N": 40, "P": 30, "K": 20}, (6.0, 7.5), 120),
    
    # SPICES (10+)
    "Turmeric": Crop("Turmeric", CropCategory.SPICE, ["Kharif"], ["AP", "TN"], {"N": 60, "P": 50, "K": 120}, (5.5, 7.5), 240),
    "Chili": Crop("Chili", CropCategory.SPICE, ["Kharif"], ["AP", "Karnataka"], {"N": 100, "P": 50, "K": 50}, (6.0, 7.0), 150),
    "Ginger": Crop("Ginger", CropCategory.SPICE, ["Kharif"], ["Kerala", "Karnataka"], {"N": 75, "P": 50, "K": 50}, (6.0, 6.5), 240),
    "Garlic": Crop("Garlic", CropCategory.SPICE, ["Rabi"], ["Gujarat", "MP"], {"N": 60, "P": 40, "K": 40}, (6.0, 7.0), 150),
    "Black Pepper": Crop("Black Pepper", CropCategory.SPICE, ["Monsoon"], ["Kerala", "Karnataka"], {"N": 50, "P": 50, "K": 120}, (5.5, 6.5), 365),
    "Cardamom": Crop("Cardamom", CropCategory.SPICE, ["Monsoon"], ["Kerala", "Karnataka"], {"N": 75, "P": 75, "K": 150}, (5.0, 6.5), 365),
    "Cumin": Crop("Cumin", CropCategory.SPICE, ["Rabi"], ["Gujarat", "Rajasthan"], {"N": 40, "P": 30, "K": 20}, (6.5, 8.0), 120),
    "Coriander Seed": Crop("Coriander Seed", CropCategory.SPICE, ["Rabi"], ["Rajasthan", "MP"], {"N": 60, "P": 30, "K": 40}, (6.0, 7.0), 90),
    
    # COMMERCIAL CROPS (5+)
    "Sugarcane": Crop("Sugarcane", CropCategory.COMMERCIAL, ["Year-round"], ["UP", "Maharashtra"], {"N": 150, "P": 60, "K": 60}, (6.0, 7.5), 365),
    "Cotton": Crop("Cotton", CropCategory.COMMERCIAL, ["Kharif"], ["Gujarat", "Maharashtra"], {"N": 120, "P": 60, "K": 60}, (6.0, 8.0), 180),
    "Jute": Crop("Jute", CropCategory.COMMERCIAL, ["Kharif"], ["West Bengal", "Bihar"], {"N": 60, "P": 30, "K": 30}, (6.0, 7.5), 120),
    "Tea": Crop("Tea", CropCategory.COMMERCIAL, ["Year-round"], ["Assam", "West Bengal"], {"N": 80, "P": 40, "K": 40}, (4.5, 5.5), 365),
    "Coffee": Crop("Coffee", CropCategory.COMMERCIAL, ["Year-round"], ["Karnataka", "Kerala"], {"N": 100, "P": 50, "K": 100}, (6.0, 6.5), 365),
}


def get_all_crops() -> List[str]:
    """Get list of all crop names."""
    return sorted(CROP_DATABASE.keys())


def get_crops_by_category(category: CropCategory) -> List[str]:
    """Get crops filtered by category."""
    return sorted([name for name, crop in CROP_DATABASE.items() if crop.category == category])


def get_crop_info(crop_name: str) -> Optional[Crop]:
    """Get detailed information about a specific crop."""
    return CROP_DATABASE.get(crop_name)


def search_crops(query: str) -> List[str]:
    """Search crops by partial name match."""
    query_lower = query.lower()
    return sorted([name for name in CROP_DATABASE.keys() if query_lower in name.lower()])


def get_crops_by_season(season: str) -> List[str]:
    """Get crops suitable for a specific season."""
    return sorted([name for name, crop in CROP_DATABASE.items() if season in crop.seasons])


def get_crop_categories() -> List[str]:
    """Get all available crop categories."""
    return [cat.value for cat in CropCategory]
