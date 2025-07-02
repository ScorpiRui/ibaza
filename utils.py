import json
import math
import os
import logging
from typing import List, Dict, Any, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File paths for data storage
LOCATIONS_FILE = "storage/locations.json"
MODELS_FILE = "storage/models.json"

# Ensure storage directory exists
os.makedirs("storage", exist_ok=True)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def find_nearest_location(user_lat: float, user_lon: float, locations: List[Dict]) -> Optional[Dict]:
    """Find the nearest location to user's coordinates"""
    if not locations:
        return None
    
    nearest = None
    min_distance = float('inf')
    
    for location in locations:
        distance = calculate_distance(
            user_lat, user_lon,
            location['latitude'], location['longitude']
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest = location
    
    if nearest:
        nearest['distance'] = round(min_distance, 2)
    
    return nearest

def load_json_data(file_path: str) -> List[Dict]:
    """Load data from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading data from {file_path}: {e}")
    return []

def save_json_data(file_path: str, data: List[Dict]) -> bool:
    """Save data to JSON file"""
    try:
        logger.info(f"Saving data to {file_path}: {len(data)} items")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved data to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        return False

def get_locations() -> List[Dict]:
    """Get all locations from storage"""
    return load_json_data(LOCATIONS_FILE)

def save_location(location: Dict) -> bool:
    """Save a new location to storage"""
    logger.info(f"Attempting to save location: {location}")
    
    locations = get_locations()
    logger.info(f"Current locations count: {len(locations)}")
    
    # Generate unique ID
    if locations:
        max_id = max(int(loc['id']) for loc in locations)
        location['id'] = str(max_id + 1)
    else:
        location['id'] = '1'
    
    logger.info(f"Generated ID for new location: {location['id']}")
    
    locations.append(location)
    logger.info(f"Added location to list. New count: {len(locations)}")
    
    result = save_json_data(LOCATIONS_FILE, locations)
    logger.info(f"Save result: {result}")
    return result

def get_models() -> List[Dict]:
    """Get all models from storage"""
    return load_json_data(MODELS_FILE)

def save_model(model: Dict) -> bool:
    """Save a new model to storage"""
    models = get_models()
    
    # Generate unique ID
    if models:
        max_id = max(int(m['id']) for m in models)
        model['id'] = str(max_id + 1)
    else:
        model['id'] = '1'
    
    models.append(model)
    return save_json_data(MODELS_FILE, models)

def get_model_by_id(model_id: str) -> Optional[Dict]:
    """Get model by ID"""
    models = get_models()
    for model in models:
        if model['id'] == model_id:
            return model
    return None

def get_price_by_condition(model: Dict, memory: int, condition: str) -> Optional[float]:
    """Get price for specific model, memory and condition"""
    if 'prices' not in model:
        return None
    
    memory_str = str(memory)
    if memory_str not in model['prices']:
        return None
    
    if condition not in model['prices'][memory_str]:
        return None
    
    return model['prices'][memory_str][condition]

def format_price(price: float) -> str:
    """Format price for display"""
    return f"{price:,.0f} so'm"

def format_distance(distance: float) -> str:
    """Format distance for display"""
    if distance < 1:
        return f"{distance * 1000:.0f} m"
    else:
        return f"{distance:.1f} km"

# Initialize default data if files don't exist
def initialize_default_data():
    """Initialize default data for the bot"""
    # Initialize locations if empty
    if not get_locations():
        default_locations = [
            {
                "id": "1",
                "name": "iBaza Toshkent markazi",
                "address": "Toshkent shahri, Chilonzor tumani, 1-mavze",
                "latitude": 41.2995,
                "longitude": 69.2401
            },
            {
                "id": "2", 
                "name": "iBaza Samarqand filiali",
                "address": "Samarqand shahri, Registon ko'chasi, 15-uy",
                "latitude": 39.6270,
                "longitude": 66.9749
            }
        ]
        save_json_data(LOCATIONS_FILE, default_locations)
    
    # Initialize models if empty
    if not get_models():
        default_models = [
            {
                "id": "1",
                "name": "iPhone 14 Pro",
                "memories": [128, 256, 512, 1024],
                "prices": {
                    "128": {"new": 15000000, "good": 12000000, "fair": 9000000},
                    "256": {"new": 17000000, "good": 14000000, "fair": 11000000},
                    "512": {"new": 20000000, "good": 17000000, "fair": 14000000},
                    "1024": {"new": 25000000, "good": 22000000, "fair": 19000000}
                }
            },
            {
                "id": "2",
                "name": "Samsung Galaxy S23",
                "memories": [128, 256, 512],
                "prices": {
                    "128": {"new": 12000000, "good": 10000000, "fair": 8000000},
                    "256": {"new": 14000000, "good": 12000000, "fair": 10000000},
                    "512": {"new": 17000000, "good": 15000000, "fair": 13000000}
                }
            }
        ]
        save_json_data(MODELS_FILE, default_models)

# Run initialization
initialize_default_data() 