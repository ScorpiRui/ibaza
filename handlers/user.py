from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location, reply_keyboard_markup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import (
    get_main_menu_keyboard, get_map_keyboard, get_locations_pagination_keyboard,
    get_models_keyboard, get_memory_keyboard, get_condition_keyboard,
    get_location_keyboard, get_share_location_keyboard, get_menu_keyboard
)
from utils import (
    get_locations, find_nearest_location, get_models, get_model_by_id,
    get_model_by_name, get_price_by_condition, format_price, format_distance,
    get_user_language
)
from languages import get_text
from config import ADMIN_IDS
import logging

logger = logging.getLogger(__name__)

router = Router()

# User states for price calculator
class PriceCalculatorStates(StatesGroup):
    selecting_model = State()
    selecting_memory = State()
    selecting_condition = State()

# User session data storage
user_sessions = {}

@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    """Handle main menu navigation"""
    user_id = callback.from_user.id
    is_admin = user_id in ADMIN_IDS
    language = get_user_language(user_id)
    
    keyboard = get_main_menu_keyboard(is_admin)
    
    welcome_text = get_text('welcome_title', language) + "\n\n"
    welcome_text += get_text('welcome_description', language) + "\n\n"
    
    # Add services list
    services = get_text('welcome_services', language)
    if isinstance(services, list):
        for service in services:
            welcome_text += f"• {service}\n"
    welcome_text += "\n"
    welcome_text += get_text('welcome_footer', language)
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "map")
async def map_handler(callback: CallbackQuery):
    """Handle map menu"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    keyboard = get_map_keyboard()
    
    await callback.message.edit_text(
        get_text('map_title', language) + "\n\n" + get_text('map_description', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "nearest_location")
async def nearest_location_handler(callback: CallbackQuery):
    """Handle nearest location request"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    keyboard = get_share_location_keyboard()
    
    await callback.message.answer(
        get_text('share_location_prompt', language),
        reply_markup=keyboard,
        parse_mode="Markdown",
        one_time_keyboard=True
    )
    await callback.answer()

@router.message(F.location)
async def handle_location_shared(message: Message, state: FSMContext):
    """Handle when user shares their location"""
    # Check if user is in admin state (adding location)
    current_state = await state.get_state()
    print(f"DEBUG: Current state when location shared: {current_state}")
    
    if current_state and "AddLocationStates" in current_state:
        print(f"DEBUG: Admin state detected, returning early")
        # This is an admin adding a location, let admin handler deal with it
        return
    
    # Check if user is in installment state
    if current_state and "InstallmentStates" in current_state:
        print(f"DEBUG: Installment state detected, returning early")
        # This is for installment calculator, let installment handler deal with it
        return
    
    print(f"DEBUG: Processing location in user handler")
    
    user_id = message.from_user.id
    language = get_user_language(user_id)
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    
    locations = get_locations()
    nearest = find_nearest_location(user_lat, user_lon, locations)
    
    if nearest:
        distance_text = format_distance(nearest['distance'])
        
        # Create location info text
        location_text = get_text('nearest_store_title', language) + "\n\n"
        location_text += get_text('store_name', language, name=nearest['name']) + "\n"
        location_text += get_text('store_address', language, address=nearest['address']) + "\n"
        location_text += get_text('store_distance', language, distance=distance_text) + "\n"
        
        if nearest.get('image'):
            location_text += get_text('store_image_available', language) + "\n\n"
        else:
            location_text += get_text('store_image_not_available', language) + "\n\n"
        
        location_text += get_text('view_on_map', language)
        
        # Send location info
        await message.answer(
            location_text,
            reply_markup=get_location_keyboard(nearest['id']),
            parse_mode="Markdown"
        )
        
        # Send image if available
        if nearest.get('image'):
            try:
                await message.answer_photo(
                    photo=nearest['image'],
                    caption=get_text('store_name', language, name=nearest['name']) + f" - {distance_text} uzoqlikda"
                )
            except Exception as e:
                logger.error(f"Failed to send nearest location image: {e}")
                await message.answer(get_text('image_load_error', language))
        
        # Show menu button after location processing
        await message.answer(
            get_text('return_to_menu', language),
            reply_markup=get_menu_keyboard()
        )
    else:
        await message.answer(
            get_text('no_stores_found', language),
            reply_markup=get_map_keyboard()
        )

@router.callback_query(F.data == "all_locations")
async def all_locations_handler(callback: CallbackQuery):
    """Handle all locations list"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    locations = get_locations()
    
    if not locations:
        await callback.message.edit_text(
            get_text('no_stores_found', language),
            reply_markup=get_map_keyboard()
        )
        return
    
    keyboard = get_locations_pagination_keyboard(locations, page=0)
    
    await callback.message.edit_text(
        get_text('all_stores_title', language) + "\n\n" + get_text('select_store', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("locations_page_"))
async def locations_pagination_handler(callback: CallbackQuery):
    """Handle locations pagination"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    page = int(callback.data.split("_")[-1])
    locations = get_locations()
    
    keyboard = get_locations_pagination_keyboard(locations, page=page)
    
    await callback.message.edit_text(
        get_text('all_stores_title', language) + "\n\n" + get_text('select_store', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("location_"))
async def location_detail_handler(callback: CallbackQuery):
    """Handle individual location selection"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    location_id = callback.data.split("_")[1]
    locations = get_locations()
    
    location = None
    for loc in locations:
        if loc['id'] == location_id:
            location = loc
            break
    
    if location:
        # Create location info text
        location_text = get_text('store_name', language, name=location['name']) + "\n\n"
        location_text += get_text('store_address', language, address=location['address']) + "\n"
        
        if location.get('image'):
            location_text += get_text('store_image_available', language) + "\n\n"
        else:
            location_text += get_text('store_image_not_available', language) + "\n\n"
        
        location_text += get_text('view_on_map', language)
        
        # Send location info
        await callback.message.edit_text(
            location_text,
            reply_markup=get_location_keyboard(location_id),
            parse_mode="Markdown"
        )
        
        # Send image if available
        if location.get('image'):
            try:
                await callback.message.answer_photo(
                    photo=location['image'],
                    caption=get_text('store_name', language, name=location['name'])
                )
            except Exception as e:
                logger.error(f"Failed to send location image: {e}")
                await callback.answer(get_text('image_load_error', language))
    else:
        await callback.answer(get_text('store_not_found', language))

@router.callback_query(F.data.startswith("show_location_"))
async def show_location_handler(callback: CallbackQuery):
    """Handle showing location on map"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    location_id = callback.data.split("_")[2]
    locations = get_locations()
    
    location = None
    for loc in locations:
        if loc['id'] == location_id:
            location = loc
            break
    
    if location:
        await callback.message.answer_location(
            latitude=location['latitude'],
            longitude=location['longitude']
        )
        await callback.answer(get_text('location_sent', language))
    else:
        await callback.answer(get_text('error_occurred', language))

@router.callback_query(F.data == "price_calculator")
async def price_calculator_handler(callback: CallbackQuery):
    """Handle price calculator menu"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    models = get_models()
    
    if not models:
        await callback.message.edit_text(
            get_text('no_models_available', language),
            reply_markup=get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS)
        )
        return
    
    keyboard = get_models_keyboard(models)
    
    await callback.message.edit_text(
        get_text('price_calculator_title', language) + "\n\n" + get_text('select_model', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("model_"))
async def model_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle model selection"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    model_name = callback.data.split("_", 1)[1]  # Get everything after "model_"
    model = get_model_by_name(model_name)
    
    if not model:
        await callback.answer(get_text('model_not_found', language))
        return
    
    # Store selected model
    await state.update_data(selected_model_name=model_name)
    await state.set_state(PriceCalculatorStates.selecting_memory)
    
    keyboard = get_memory_keyboard(model['memories'])
    
    await callback.message.edit_text(
        get_text('model_selected', language, name=model['name']) + "\n\n" + get_text('select_memory', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("memory_"))
async def memory_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle memory selection"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    memory = int(callback.data.split("_")[1])
    
    # Store selected memory
    await state.update_data(selected_memory=memory)
    await state.set_state(PriceCalculatorStates.selecting_condition)
    
    # Format memory display
    if memory == 1024:
        memory_display = "1 TB"
    else:
        memory_display = f"{memory} GB"
    
    # Create condition description text
    condition_text = get_text('memory_selected', language, memory=memory_display) + "\n\n"
    condition_text += get_text('condition_info_title', language) + "\n\n"
    condition_text += get_text('condition_new', language) + "\n\n"
    condition_text += get_text('condition_good', language) + "\n\n"
    condition_text += get_text('condition_fair', language)
    
    # Create keyboard with "tanishib chiqdim" button
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=get_text('got_it', language), callback_data="show_conditions"))
    builder.add(InlineKeyboardButton(text=get_text('back', language), callback_data="select_memory"))
    builder.adjust(1)
    
    await callback.message.edit_text(
        condition_text,
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "show_conditions")
async def show_conditions_handler(callback: CallbackQuery, state: FSMContext):
    """Handle show conditions button"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    # Get stored data
    data = await state.get_data()
    model_name = data.get('selected_model_name')
    memory = data.get('selected_memory')
    
    if not model_name or not memory:
        await callback.answer(get_text('error_restart', language))
        await state.clear()
        return
    
    # Get model data
    model = get_model_by_name(model_name)
    if not model:
        await callback.answer(get_text('model_not_found', language))
        await state.clear()
        return
    
    # Format memory display
    if memory == 1024:
        memory_display = "1 TB"
    else:
        memory_display = f"{memory} GB"
    
    keyboard = get_condition_keyboard()
    
    await callback.message.edit_text(
        get_text('model_selected', language, name=model['name']) + f" {memory_display}\n\n" + get_text('select_condition', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("condition_"))
async def condition_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle condition selection and show price"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    condition = callback.data.split("_")[1]
    
    # Get stored data
    data = await state.get_data()
    model_name = data.get('selected_model_name')
    memory = data.get('selected_memory')
    
    if not model_name or not memory:
        await callback.answer(get_text('error_restart', language))
        await state.clear()
        return
    
    # Get model data
    model = get_model_by_name(model_name)
    if not model:
        await callback.answer(get_text('model_not_found', language))
        await state.clear()
        return
    
    # Get price for selected condition
    price = get_price_by_condition(model, memory, condition)
    
    if not price:
        await callback.answer(get_text('condition_not_found', language))
        return
    
    # Format condition display
    condition_display = {
        'new': '🆕 Ideal',
        'good': '✅ Yaxshi', 
        'fair': '🔄 Ortacha'
    }.get(condition, condition)
    
    # Format memory display
    if memory == 1024:
        memory_display = "1 TB"
    else:
        memory_display = f"{memory} GB"
    
    # Format price
    formatted_price = format_price(price)
    
    # Create response message with additional information
    response = get_text('price_result_title', language) + "\n\n"
    response += get_text('price_model', language, model=model['name']) + "\n"
    response += get_text('price_memory', language, memory=memory_display) + "\n"
    response += get_text('price_condition', language, condition=condition_display) + "\n"
    response += get_text('price_amount', language, price=formatted_price) + "\n\n"
    response += get_text('additional_info_title', language) + "\n"
    
    # Add additional info list
    additional_info = get_text('additional_info', language)
    if isinstance(additional_info, list):
        for info in additional_info:
            response += f"• {info}\n"
    response += "\n"
    response += get_text('contact_for_details', language)
    
    # Create keyboard for new calculation
    from keyboards import get_main_menu_keyboard
    keyboard = get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS)
    
    await callback.message.edit_text(
        response,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    # Clear state
    await state.clear()

@router.callback_query(F.data == "back_to_memory")
async def back_to_memory_handler(callback: CallbackQuery, state: FSMContext):
    """Handle back to memory selection"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    # Get stored data
    data = await state.get_data()
    model_name = data.get('selected_model_name')
    
    if not model_name:
        await callback.answer(get_text('error_restart', language))
        await state.clear()
        return
    
    # Get model data
    model = get_model_by_name(model_name)
    if not model:
        await callback.answer(get_text('model_not_found', language))
        await state.clear()
        return
    
    # Clear memory selection from state
    await state.update_data(selected_memory=None)
    await state.set_state(PriceCalculatorStates.selecting_memory)
    
    keyboard = get_memory_keyboard(model['memories'])
    
    await callback.message.edit_text(
        get_text('model_selected', language, name=model['name']) + "\n\n" + get_text('select_memory', language),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "call_center")
async def call_center_handler(callback: CallbackQuery):
    """Handle call center contact"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    await callback.answer(get_text('phone_copied', language))
    
    call_center_text = get_text('call_center_title', language) + "\n\n"
    call_center_text += get_text('call_center_description', language) + "\n\n"
    
    # Add services list
    services = get_text('call_center_services', language)
    if isinstance(services, list):
        for service in services:
            call_center_text += f"• {service}\n"
    call_center_text += "\n"
    call_center_text += get_text('call_center_phone', language) + "\n"
    call_center_text += get_text('call_center_hours', language) + "\n"
    call_center_text += get_text('call_center_days', language) + "\n\n"
    call_center_text += get_text('call_center_footer', language)
    
    await callback.message.edit_text(
        call_center_text,
        reply_markup=get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "admin_contact")
async def admin_contact_handler(callback: CallbackQuery):
    """Handle admin contact"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    
    await callback.answer(get_text('admin_info_shown', language))
    
    admin_text = get_text('admin_contact_title', language) + "\n\n"
    admin_text += get_text('admin_contact_description', language) + "\n\n"
    admin_text += get_text('admin_telegram', language) + "\n"
    admin_text += get_text('admin_phone', language) + "\n\n"
    admin_text += get_text('admin_footer', language)
    
    await callback.message.edit_text(
        admin_text,
        reply_markup=get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    """Handle cancel action"""
    user_id = callback.from_user.id
    language = get_user_language(user_id)
    is_admin = user_id in ADMIN_IDS
    
    await state.clear()
    keyboard = get_main_menu_keyboard(is_admin)
    
    welcome_text = get_text('welcome_title', language) + "\n\n"
    welcome_text += get_text('welcome_description', language) + "\n\n"
    
    # Add services list
    services = get_text('welcome_services', language)
    if isinstance(services, list):
        for service in services:
            welcome_text += f"• {service}\n"
    welcome_text += "\n"
    welcome_text += get_text('welcome_footer', language)
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def register_user_handlers(dp):
    """Register all user handlers"""
    dp.include_router(router) 

@router.message(F.text == "Menu")
async def menu_handler(message: Message):
    """Handle menu button"""
    user_id = message.from_user.id
    language = get_user_language(user_id)
    is_admin = user_id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    welcome_text = get_text('welcome_title', language) + "\n\n"
    welcome_text += get_text('welcome_description', language) + "\n\n"
    
    # Add services list
    services = get_text('welcome_services', language)
    if isinstance(services, list):
        for service in services:
            welcome_text += f"• {service}\n"
    welcome_text += "\n"
    welcome_text += get_text('welcome_footer', language)
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

@router.message(F.text == "🏪 Menu")
async def menu_emoji_handler(message: Message):
    """Handle menu button with emoji"""
    user_id = message.from_user.id
    language = get_user_language(user_id)
    is_admin = user_id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    welcome_text = get_text('welcome_title', language) + "\n\n"
    welcome_text += get_text('welcome_description', language) + "\n\n"
    
    # Add services list
    services = get_text('welcome_services', language)
    if isinstance(services, list):
        for service in services:
            welcome_text += f"• {service}\n"
    welcome_text += "\n"
    welcome_text += get_text('welcome_footer', language)
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

