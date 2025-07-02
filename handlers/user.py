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
    get_price_by_condition, format_price, format_distance
)
from config import ADMIN_IDS

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
    is_admin = callback.from_user.id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    await callback.message.edit_text(
        "🏪 **iBaza Tech Resale Market** ga xush kelibsiz!\n\n"
        "Biz sizga eng yaxshi texnologiya mahsulotlarini taklif qilamiz.\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "map")
async def map_handler(callback: CallbackQuery):
    """Handle map menu"""
    keyboard = get_map_keyboard()
    
    await callback.message.edit_text(
        "🗺️ **Xarita xizmatlari**\n\n"
        "Eng yaqin do'konimizni topish yoki barcha joylashuvlarni ko'rish uchun tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "nearest_location")
async def nearest_location_handler(callback: CallbackQuery):
    """Handle nearest location request"""
    keyboard = get_share_location_keyboard()
    
    await callback.message.answer(
        "📍 **Eng yaqin joylashuvni topish**\n\n"
        "Iltimos, o'z joylashuvingizni yuboring:",
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
    
    user_lat = message.location.latitude
    user_lon = message.location.longitude
    
    locations = get_locations()
    nearest = find_nearest_location(user_lat, user_lon, locations)
    
    if nearest:
        distance_text = format_distance(nearest['distance'])
        
        # Send location info
        await message.answer(
            f"📍 **Eng yaqin do'konimiz:**\n\n"
            f"🏪 **{nearest['name']}**\n"
            f"📍 **Manzil:** {nearest['address']}\n"
            f"📏 **Masofa:** {distance_text}\n\n"
            f"Joylashuvni xaritada ko'rish uchun tugmani bosing:",
            reply_markup=get_location_keyboard(nearest['id']),
            parse_mode="Markdown"
        )   
        
        # Show menu button after location processing
        await message.answer(
            "🏪 Asosiy menyuga qaytish uchun tugmani bosing:",
            reply_markup=get_menu_keyboard()
        )
    else:
        await message.answer(
            "❌ Kechirasiz, hozirda hech qanday do'kon topilmadi.",
            reply_markup=get_map_keyboard()
        )

@router.callback_query(F.data == "all_locations")
async def all_locations_handler(callback: CallbackQuery):
    """Handle all locations list"""
    locations = get_locations()
    
    if not locations:
        await callback.message.edit_text(
            "❌ Kechirasiz, hozirda hech qanday do'kon topilmadi.",
            reply_markup=get_map_keyboard()
        )
        return
    
    keyboard = get_locations_pagination_keyboard(locations, page=0)
    
    await callback.message.edit_text(
        "📋 **Barcha do'konlarimiz:**\n\n"
        "Kerakli do'konni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("locations_page_"))
async def locations_pagination_handler(callback: CallbackQuery):
    """Handle locations pagination"""
    page = int(callback.data.split("_")[-1])
    locations = get_locations()
    
    keyboard = get_locations_pagination_keyboard(locations, page=page)
    
    await callback.message.edit_text(
        "📋 **Barcha do'konlarimiz:**\n\n"
        "Kerakli do'konni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("location_"))
async def location_detail_handler(callback: CallbackQuery):
    """Handle individual location selection"""
    location_id = callback.data.split("_")[1]
    locations = get_locations()
    
    location = None
    for loc in locations:
        if loc['id'] == location_id:
            location = loc
            break
    
    if location:
        await callback.message.edit_text(
            f"🏪 **{location['name']}**\n\n"
            f"📍 **Manzil:** {location['address']}\n\n"
            f"Joylashuvni xaritada ko'rish uchun tugmani bosing:",
            reply_markup=get_location_keyboard(location_id),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("❌ Do'kon topilmadi!")

@router.callback_query(F.data.startswith("show_location_"))
async def show_location_handler(callback: CallbackQuery):
    """Handle showing location on map"""
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
        await callback.answer("📍 Joylashuv yuborildi!")
    else:
        await callback.answer("❌ Xatolik yuz berdi!")

@router.callback_query(F.data == "price_calculator")
async def price_calculator_handler(callback: CallbackQuery):
    """Handle price calculator menu"""
    models = get_models()
    
    if not models:
        await callback.message.edit_text(
            "❌ Kechirasiz, hozirda hech qanday model mavjud emas.",
            reply_markup=get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS)
        )
        return
    
    keyboard = get_models_keyboard(models)
    
    await callback.message.edit_text(
        "💰 **Narx hisoblagich**\n\n"
        "Qurilma modelini tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("model_"))
async def model_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle model selection"""
    model_id = callback.data.split("_")[1]
    model = get_model_by_id(model_id)
    
    if not model:
        await callback.answer("❌ Model topilmadi!")
        return
    
    # Store selected model
    await state.update_data(selected_model_id=model_id)
    await state.set_state(PriceCalculatorStates.selecting_memory)
    
    keyboard = get_memory_keyboard(model['memories'])
    
    await callback.message.edit_text(
        f"📱 **{model['name']}** tanlandi\n\n"
        f"Xotira hajmini tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("memory_"))
async def memory_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle memory selection"""
    memory = int(callback.data.split("_")[1])
    
    # Store selected memory
    await state.update_data(selected_memory=memory)
    await state.set_state(PriceCalculatorStates.selecting_condition)
    
    keyboard = get_condition_keyboard()
    
    await callback.message.edit_text(
        f"💾 **{memory} GB** tanlandi\n\n"
        f"Qurilma holatini tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("condition_"))
async def condition_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle condition selection and show price"""
    condition = callback.data.split("_")[1]
    
    # Get stored data
    data = await state.get_data()
    model_id = data.get('selected_model_id')
    memory = data.get('selected_memory')
    
    if not model_id or not memory:
        await callback.answer("❌ Ma'lumotlar topilmadi!")
        return
    
    model = get_model_by_id(model_id)
    if not model:
        await callback.answer("❌ Model topilmadi!")
        return
    
    price = get_price_by_condition(model, memory, condition)
    if not price:
        await callback.answer("❌ Narx topilmadi!")
        return
    
    # Condition names in Uzbek
    condition_names = {
        "new": "🆕 Yangi",
        "good": "✅ Yaxshi", 
        "fair": "🔄 O'rtacha"
    }
    
    condition_name = condition_names.get(condition, condition)
    formatted_price = format_price(price)
    
    # Create keyboard for new calculation
    from keyboards import get_main_menu_keyboard
    keyboard = get_main_menu_keyboard(callback.from_user.id in ADMIN_IDS)
    
    await callback.message.edit_text(
        f"💰 **Narx hisoblash natijasi**\n\n"
        f"📱 **Model:** {model['name']}\n"
        f"💾 **Xotira:** {memory} GB\n"
        f"📊 **Holat:** {condition_name}\n\n"
        f"💵 **Narx:** {formatted_price}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    # Clear state
    await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    """Handle cancel action"""
    await state.clear()
    is_admin = callback.from_user.id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    await callback.message.edit_text(
        "🏪 **iBaza Tech Resale Market** ga xush kelibsiz!\n\n"
        "Biz sizga eng yaxshi texnologiya mahsulotlarini taklif qilamiz.\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def register_user_handlers(dp):
    """Register all user handlers"""
    dp.include_router(router) 

@router.message(F.text == "Menu")
async def menu_handler(message: Message):
    """Handle menu button"""
    is_admin = message.from_user.id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    await message.answer(
        "🏪 **iBaza Tech Resale Market** ga xush kelibsiz!\n\n"
        "Biz sizga eng yaxshi texnologiya mahsulotlarini taklif qilamiz.\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "🏪 Menu")
async def menu_emoji_handler(message: Message):
    """Handle menu button with emoji"""
    is_admin = message.from_user.id in ADMIN_IDS
    keyboard = get_main_menu_keyboard(is_admin)
    
    await message.answer(
        "🏪 **iBaza Tech Resale Market** ga xush kelibsiz!\n\n"
        "Biz sizga eng yaxshi texnologiya mahsulotlarini taklif qilamiz.\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

