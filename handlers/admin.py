from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import (
    get_admin_panel_keyboard, get_admin_map_keyboard, get_admin_price_keyboard,
    get_cancel_keyboard, get_admin_cancel_keyboard,
    get_admin_map_cancel_keyboard, get_admin_price_cancel_keyboard
)
from utils import save_location, get_locations, get_user_language
from languages import get_text
from config import ADMIN_IDS
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = Router()

# Admin states for adding location
class AddLocationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_location = State()
    waiting_for_image = State()

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

@router.callback_query(F.data == "admin_panel")
async def admin_panel_handler(callback: CallbackQuery):
    """Handle admin panel"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('no_permission', get_user_language(callback.from_user.id)))
        return
    
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    keyboard = get_admin_panel_keyboard()
    
    await callback.message.edit_text(
        get_text('admin_panel_title', language) + "\n\n" + get_text('admin_panel_description', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "admin_map")
async def admin_map_handler(callback: CallbackQuery):
    """Handle admin map management"""
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('no_permission', get_user_language(callback.from_user.id)))
        return
    
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    keyboard = get_admin_map_keyboard()
    
    await callback.message.edit_text(
        get_text('admin_map_title', language) + "\n\n" + get_text('admin_map_description', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "add_location")
async def add_location_handler(callback: CallbackQuery, state: FSMContext):
    """Handle add location request"""
    logger.info(f"Admin {callback.from_user.id} requested to add location")
    
    if not is_admin(callback.from_user.id):
        await callback.answer(get_text('no_permission', get_user_language(callback.from_user.id)))
        return
    
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    await state.set_state(AddLocationStates.waiting_for_name)
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        get_text('add_location_title', language) + "\n\n" + get_text('enter_store_name', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_name)
async def handle_location_name(message: Message, state: FSMContext):
    """Handle location name input"""
    logger.info(f"Admin {message.from_user.id} entered location name: {message.text}")
    
    if not is_admin(message.from_user.id):
        return
    
    user_id = message.from_user.id
    language = get_user_language(user_id)
    
    if not message.text:
        await message.answer(
            get_text('please_enter_name', language),
            reply_markup=get_admin_map_cancel_keyboard()
        )
        return
    
    await state.update_data(name=message.text)
    await state.set_state(AddLocationStates.waiting_for_address)
    
    keyboard = get_admin_map_cancel_keyboard()
    
    await message.answer(
        get_text('name_entered', language, name=message.text) + "\n\n" + get_text('enter_store_address', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_address)
async def handle_location_address(message: Message, state: FSMContext):
    """Handle location address input"""
    logger.info(f"Admin {message.from_user.id} entered location address: {message.text}")
    
    if not is_admin(message.from_user.id):
        return
    
    user_id = message.from_user.id
    language = get_user_language(user_id)
    
    if not message.text:
        await message.answer(
            get_text('please_enter_address', language),
            reply_markup=get_admin_map_cancel_keyboard()
        )
        return
    
    await state.update_data(address=message.text)
    await state.set_state(AddLocationStates.waiting_for_location)
    
    from keyboards import get_share_location_keyboard
    keyboard = get_share_location_keyboard()
    
    await message.answer(
        get_text('address_entered', language, address=message.text) + "\n\n" + get_text('share_store_location', language),
        reply_markup=keyboard,
        parse_mode="Markdown",
        one_time_keyboard=False
    )

@router.message(AddLocationStates.waiting_for_location)
async def handle_location_coordinates(message: Message, state: FSMContext):
    """Handle location coordinates"""
    print(f"DEBUG: Admin location handler called for user {message.from_user.id}")
    logger.info(f"Admin {message.from_user.id} shared location: {message.location}")
    
    if not is_admin(message.from_user.id):
        print(f"DEBUG: User {message.from_user.id} is not admin")
        return
    
    user_id = message.from_user.id
    language = get_user_language(user_id)
    
    if not message.location:
        print(f"DEBUG: No location in message")
        await message.answer(
            get_text('please_share_location', language),
            reply_markup=get_admin_map_cancel_keyboard()
        )
        return
    
    print(f"DEBUG: Processing location for admin {message.from_user.id}")
    
    data = await state.get_data()
    name = data.get('name')
    address = data.get('address')
    
    print(f"DEBUG: Location data from state: name={name}, address={address}")
    logger.info(f"Location data from state: name={name}, address={address}")
    
    if not name or not address:
        print(f"DEBUG: Missing name or address")
        await message.answer(
            get_text('error_restart_admin', language),
            reply_markup=get_admin_map_keyboard()
        )
        await state.clear()
        return
    
    # Store coordinates and move to image state
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude
    )
    await state.set_state(AddLocationStates.waiting_for_image)
    
    keyboard = get_admin_map_cancel_keyboard()
    
    await message.answer(
        get_text('coordinates_received', language, lat=message.location.latitude, lon=message.location.longitude) + "\n\n" + get_text('upload_store_image', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_image)
async def handle_location_image(message: Message, state: FSMContext):
    """Handle location image upload"""
    logger.info(f"Admin {message.from_user.id} uploaded image for location")
    
    if not is_admin(message.from_user.id):
        return
    
    user_id = message.from_user.id
    language = get_user_language(user_id)
    
    # Get all stored data
    data = await state.get_data()
    name = data.get('name')
    address = data.get('address')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not all([name, address, latitude, longitude]):
        await message.answer(
            get_text('error_restart_admin', language),
            reply_markup=get_admin_map_keyboard()
        )
        await state.clear()
        return
    
    # Handle image if provided
    image_file_id = None
    if message.photo:
        # Get the largest photo size
        photo = message.photo[-1]
        image_file_id = photo.file_id
        logger.info(f"Image uploaded: {image_file_id}")
    
    # Create location data
    location_data = {
        'name': name,
        'address': address,
        'latitude': latitude,
        'longitude': longitude,
        'image': image_file_id
    }
    
    print(f"DEBUG: Attempting to save location data: {location_data}")
    logger.info(f"Attempting to save location data: {location_data}")
    
    if save_location(location_data):
        print(f"DEBUG: Location saved successfully")
        
        # Send success message
        success_text = get_text('location_saved_title', language) + "\n\n"
        success_text += get_text('location_name', language, name=name) + "\n"
        success_text += get_text('store_address', language, address=address) + "\n"
        success_text += get_text('location_coordinates', language, lat=latitude, lon=longitude) + "\n"
        
        if image_file_id:
            success_text += get_text('image_added', language) + "\n"
        else:
            success_text += get_text('image_not_added', language) + "\n"
        
        await message.answer(
            success_text,
            reply_markup=get_admin_map_keyboard(),
            parse_mode="Markdown"
        )
        logger.info(f"Location saved successfully for admin {message.from_user.id}")
    else:
        print(f"DEBUG: Failed to save location")
        await message.answer(
            get_text('location_save_error', language),
            reply_markup=get_admin_map_keyboard()
        )
        logger.error(f"Failed to save location for admin {message.from_user.id}")
    
    await state.clear()

@router.callback_query(F.data == "admin_price")
async def admin_price_handler(callback: CallbackQuery):
    """Handle admin price management - now shows Google Sheets link"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    # Create keyboard with Google Sheets link
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('manage_prices_sheets', language),
        url="https://docs.google.com/spreadsheets/d/1Rw3MW613RW6_4zKgtBWWkPg9bEoyvG68OLTCFbkgTAg/edit?gid=0#gid=0"
    ))
    builder.add(InlineKeyboardButton(text=get_text('refresh_prices', language), callback_data="refresh_prices"))
    builder.add(InlineKeyboardButton(text=get_text('back_to_admin', language), callback_data="admin_panel"))
    builder.adjust(1)
    
    # Create message text
    message_text = get_text('price_management_title', language) + "\n\n"
    message_text += get_text('price_management_description', language) + "\n"
    
    # Add features list
    features = get_text('price_management_features', language)
    if isinstance(features, list):
        for feature in features:
            message_text += f"• {feature}\n"
    message_text += "\n"
    message_text += get_text('refresh_prices_description', language)
    
    await callback.message.edit_text(
        message_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "refresh_prices")
async def refresh_prices_handler(callback: CallbackQuery):
    """Handle refresh prices from Google Sheets"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    await callback.answer(get_text('prices_refreshing', language))
    
    try:
        from sheets_service import get_sheets_service
        service = get_sheets_service()
        models = service.get_all_models()
        
        if models:
            message_text = get_text('prices_refreshed', language) + "\n\n"
            message_text += get_text('total_models', language, count=len(models)) + "\n\n"
            message_text += get_text('prices_refresh_description', language)
            
            await callback.message.edit_text(
                message_text,
                reply_markup=get_admin_price_keyboard(),
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                get_text('sheets_error', language),
                reply_markup=get_admin_price_keyboard(),
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Failed to refresh prices: {e}")
        await callback.message.edit_text(
            get_text('refresh_error', language),
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )

@router.callback_query(F.data == "cancel")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """Handle cancel button"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    current_state = await state.get_state()
    
    if current_state and "AddLocationStates" in current_state:
        # Return to admin map panel
        await state.clear()
        keyboard = get_admin_map_keyboard()
        
        await callback.message.edit_text(
            "🗺️ **Xarita boshqaruvi**\n\n"
            "Do'kon joylashuvlarini boshqarish:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # For other states, just clear and show admin panel
        await state.clear()
        keyboard = get_admin_panel_keyboard()
        
        await callback.message.edit_text(
            "⚙️ **Admin panel**\n\n"
            "Do'konlar va narxlarni boshqarish uchun tanlang:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

def register_admin_handlers(dp):
    """Register all admin handlers"""
    dp.include_router(router) 