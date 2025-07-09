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
USER_LANGUAGES_FILE = "storage/user_languages.json"

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

def format_distance(distance: float) -> str:
    """Format distance for display"""
    if distance < 1:
        return f"{int(distance * 1000)} m"
    else:
        return f"{distance:.1f} km"

def find_nearest_location(user_lat: float, user_lon: float, locations: List[Dict]) -> Optional[Dict]:
    """Find the nearest location to user coordinates"""
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
            nearest = location.copy()
            nearest['distance'] = distance
    
    return nearest

def load_json_data(file_path: str) -> Any:
    """Load data from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading data from {file_path}: {e}")
    return {} if 'user_languages' in file_path else []

def save_json_data(file_path: str, data: Any) -> bool:
    """Save data to JSON file"""
    try:
        logger.info(f"Saving data to {file_path}: {len(data) if isinstance(data, (list, dict)) else 'unknown'} items")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved data to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {e}")
        return False

# Location functions (using local JSON storage)
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
    
    # Set default image if not provided
    if 'image' not in location:
        location['image'] = None
    
    logger.info(f"Generated ID for new location: {location['id']}")
    
    locations.append(location)
    logger.info(f"Added location to list. New count: {len(locations)}")
    
    result = save_json_data(LOCATIONS_FILE, locations)
    logger.info(f"Save result: {result}")
    return result

def get_locations() -> List[Dict]:
    """Get all locations from storage"""
    return load_json_data(LOCATIONS_FILE)

def get_location_by_id(location_id: str) -> Optional[Dict]:
    """Get location by ID"""
    locations = get_locations()
    for location in locations:
        if location.get('id') == location_id:
            return location
    return None

# Model functions (using Google Sheets)
def get_models() -> List[Dict]:
    """Get all models from Google Sheets"""
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        return service.get_all_models()
    except Exception as e:
        logger.error(f"Failed to get models from Google Sheets: {e}")
        return []

def get_model_by_id(model_id: str) -> Optional[Dict]:
    """Get model by ID (for backward compatibility)"""
    models = get_models()
    try:
        index = int(model_id) - 1
        if 0 <= index < len(models):
            return models[index]
    except (ValueError, IndexError):
        pass
    return None

def get_model_by_name(model_name: str) -> Optional[Dict]:
    """Get model by name"""
    models = get_models()
    for model in models:
        if model.get('name') == model_name:
            return model
    return None

def get_price_by_condition(model: Dict, memory: int, condition: str) -> Optional[int]:
    """Get price for specific model, memory, and condition"""
    if not model or 'prices' not in model:
        return None
    
    memory_str = str(memory)
    if memory_str not in model['prices']:
        return None
    
    prices = model['prices'][memory_str]
    return prices.get(condition)

def format_price(price: int) -> str:
    """Format price for display in USD"""
    return f"${price:,}"

# Legacy functions for backward compatibility (now using Google Sheets)
def save_model(model_data: Dict) -> bool:
    """Save model to Google Sheets (legacy function)"""
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        
        model_name = model_data.get('name')
        if not model_name:
            logger.error("Model name is required")
            return False
            
        memories = model_data.get('memories', [])
        prices = model_data.get('prices', {})
        
        success = True
        for memory in memories:
            memory_prices = prices.get(str(memory), {})
            if service.add_model(
                model_name, memory,
                memory_prices.get('new', 0),
                memory_prices.get('good', 0),
                memory_prices.get('fair', 0)
            ):
                logger.info(f"Added model {model_name} {memory}GB to Google Sheets")
            else:
                success = False
                logger.error(f"Failed to add model {model_name} {memory}GB to Google Sheets")
        
        return success
    except Exception as e:
        logger.error(f"Failed to save model to Google Sheets: {e}")
        return False

def update_model(model_id: str, updated_model: Dict) -> bool:
    """Update model in Google Sheets (legacy function)"""
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        
        model_name = updated_model.get('name')
        if not model_name:
            logger.error("Model name is required")
            return False
            
        memories = updated_model.get('memories', [])
        prices = updated_model.get('prices', {})
        
        success = True
        for memory in memories:
            memory_prices = prices.get(str(memory), {})
            if service.update_model_price(
                model_name, memory,
                memory_prices.get('new', 0),
                memory_prices.get('good', 0),
                memory_prices.get('fair', 0)
            ):
                logger.info(f"Updated model {model_name} {memory}GB in Google Sheets")
            else:
                success = False
                logger.error(f"Failed to update model {model_name} {memory}GB in Google Sheets")
        
        return success
    except Exception as e:
        logger.error(f"Failed to update model in Google Sheets: {e}")
        return False

def delete_model(model_id: str) -> bool:
    """Delete model from Google Sheets (legacy function)"""
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        
        # Get the model to delete
        model = get_model_by_id(model_id)
        if not model:
            logger.error(f"Model with ID {model_id} not found")
            return False
        
        model_name = model.get('name')
        if not model_name:
            logger.error("Model name is required")
            return False
            
        memories = model.get('memories', [])
        
        success = True
        for memory in memories:
            if service.delete_model(model_name, memory):
                logger.info(f"Deleted model {model_name} {memory}GB from Google Sheets")
            else:
                success = False
                logger.error(f"Failed to delete model {model_name} {memory}GB from Google Sheets")
        
        return success
    except Exception as e:
        logger.error(f"Failed to delete model from Google Sheets: {e}")
        return False

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
                "longitude": 69.2401,
                "image": None
            },
            {
                "id": "2", 
                "name": "iBaza Samarqand filiali",
                "address": "Samarqand shahri, Registon ko'chasi, 15-uy",
                "latitude": 39.6270,
                "longitude": 66.9749,
                "image": None
            }
        ]
        save_json_data(LOCATIONS_FILE, default_locations)
    
    # Initialize Google Sheets template if needed
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        service.create_template()
        logger.info("Google Sheets template initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets template: {e}") 

# Language management functions
def get_user_language(user_id: int) -> str:
    """Get user's preferred language"""
    try:
        user_languages = load_json_data(USER_LANGUAGES_FILE)
        if isinstance(user_languages, dict):
            return user_languages.get(str(user_id), 'uz')  # Default to Uzbek
        return 'uz'
    except Exception as e:
        logger.error(f"Error getting user language: {e}")
        return 'uz'

def set_user_language(user_id: int, language: str) -> bool:
    """Set user's preferred language"""
    try:
        user_languages = load_json_data(USER_LANGUAGES_FILE)
        if not isinstance(user_languages, dict):
            user_languages = {}
        user_languages[str(user_id)] = language
        return save_json_data(USER_LANGUAGES_FILE, user_languages)
    except Exception as e:
        logger.error(f"Error setting user language: {e}")
        return False 