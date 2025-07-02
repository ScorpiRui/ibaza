from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import (
    get_admin_panel_keyboard, get_admin_map_keyboard, get_admin_price_keyboard,
    get_cancel_keyboard, get_admin_cancel_keyboard,
    get_admin_map_cancel_keyboard, get_admin_price_cancel_keyboard
)
from utils import save_location, save_model, get_locations, get_models
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

# Admin states for adding model
class AddModelStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_memories = State()
    waiting_for_prices = State()

# Admin session data storage
admin_sessions = {}

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

@router.callback_query(F.data == "admin_panel")
async def admin_panel_handler(callback: CallbackQuery):
    """Handle admin panel"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    keyboard = get_admin_panel_keyboard()
    
    await callback.message.edit_text(
        "⚙️ **Admin panel**\n\n"
        "Do'konlar va narxlarni boshqarish uchun tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "admin_map")
async def admin_map_handler(callback: CallbackQuery):
    """Handle admin map management"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    keyboard = get_admin_map_keyboard()
    
    await callback.message.edit_text(
        "🗺️ **Xarita boshqaruvi**\n\n"
        "Do'kon joylashuvlarini boshqarish:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "add_location")
async def add_location_handler(callback: CallbackQuery, state: FSMContext):
    """Handle add location request"""
    logger.info(f"Admin {callback.from_user.id} requested to add location")
    
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    await state.set_state(AddLocationStates.waiting_for_name)
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        "➕ **Yangi joylashuv qo'shish**\n\n"
        "Do'kon nomini kiriting:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_name)
async def handle_location_name(message: Message, state: FSMContext):
    """Handle location name input"""
    logger.info(f"Admin {message.from_user.id} entered location name: {message.text}")
    
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, do'kon nomini kiriting!",
            reply_markup=get_admin_map_cancel_keyboard()
        )
        return
    
    await state.update_data(name=message.text)
    await state.set_state(AddLocationStates.waiting_for_address)
    
    keyboard = get_admin_map_cancel_keyboard()
    
    await message.answer(
        f"✅ **Nom:** {message.text}\n\n"
        f"Endi do'kon manzilini kiriting:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_address)
async def handle_location_address(message: Message, state: FSMContext):
    """Handle location address input"""
    logger.info(f"Admin {message.from_user.id} entered location address: {message.text}")
    
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, do'kon manzilini kiriting!",
            reply_markup=get_admin_map_cancel_keyboard()
        )
        return
    
    await state.update_data(address=message.text)
    await state.set_state(AddLocationStates.waiting_for_location)
    
    from keyboards import get_share_location_keyboard
    keyboard = get_share_location_keyboard()
    
    await message.answer(
        f"✅ **Manzil:** {message.text}\n\n"
        f"Endi do'kon joylashuvini yuboring:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddLocationStates.waiting_for_location)
async def handle_location_coordinates(message: Message, state: FSMContext):
    """Handle location coordinates"""
    print(f"DEBUG: Admin location handler called for user {message.from_user.id}")
    logger.info(f"Admin {message.from_user.id} shared location: {message.location}")
    
    if not is_admin(message.from_user.id):
        print(f"DEBUG: User {message.from_user.id} is not admin")
        return
    
    if not message.location:
        print(f"DEBUG: No location in message")
        await message.answer(
            "❌ Iltimos, joylashuvni yuboring!",
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
            "❌ Xatolik yuz berdi! Qaytadan boshlang.",
            reply_markup=get_admin_map_keyboard()
        )
        await state.clear()
        return
    
    location_data = {
        'name': name,
        'address': address,
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    }
    
    print(f"DEBUG: Attempting to save location data: {location_data}")
    logger.info(f"Attempting to save location data: {location_data}")
    
    if save_location(location_data):
        print(f"DEBUG: Location saved successfully")
        await message.answer(
            f"✅ **Joylashuv muvaffaqiyatli qo'shildi!**\n\n"
            f"🏪 **Nomi:** {name}\n"
            f"📍 **Manzil:** {address}\n"
            f"📍 **Koordinatalar:** {message.location.latitude}, {message.location.longitude}",
            reply_markup=get_admin_map_keyboard(),
            parse_mode="Markdown"
        )
        logger.info(f"Location saved successfully for admin {message.from_user.id}")
    else:
        print(f"DEBUG: Failed to save location")
        await message.answer(
            "❌ Xatolik yuz berdi! Joylashuv saqlanmadi.",
            reply_markup=get_admin_map_keyboard()
        )
        logger.error(f"Failed to save location for admin {message.from_user.id}")
    
    await state.clear()

@router.callback_query(F.data == "admin_price")
async def admin_price_handler(callback: CallbackQuery):
    """Handle admin price management"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    keyboard = get_admin_price_keyboard()
    
    await callback.message.edit_text(
        "💰 **Narx boshqaruvi**\n\n"
        "Qurilma modellarini boshqarish:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "add_model")
async def add_model_handler(callback: CallbackQuery, state: FSMContext):
    """Handle add model request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    await state.set_state(AddModelStates.waiting_for_name)
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        "➕ **Yangi model qo'shish**\n\n"
        "Qurilma modelini kiriting (masalan: iPhone 15 Pro):",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddModelStates.waiting_for_name)
async def handle_model_name(message: Message, state: FSMContext):
    """Handle model name input"""
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, model nomini kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    await state.update_data(name=message.text)
    await state.set_state(AddModelStates.waiting_for_memories)
    
    keyboard = get_cancel_keyboard()
    
    await message.answer(
        f"✅ **Model:** {message.text}\n\n"
        f"Endi xotira hajmlarini kiriting (vergul bilan ajrating):\n"
        f"Masalan: 64, 128, 256, 512",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddModelStates.waiting_for_memories)
async def handle_model_memories(message: Message, state: FSMContext):
    """Handle model memories input"""
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, xotira hajmlarini kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    try:
        memories = [int(x.strip()) for x in message.text.split(',')]
        if not memories:
            raise ValueError("Empty list")
    except ValueError:
        await message.answer(
            "❌ Noto'g'ri format! Iltimos, raqamlarni vergul bilan ajrating.\n"
            "Masalan: 64, 128, 256",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    await state.update_data(memories=memories)
    await state.set_state(AddModelStates.waiting_for_prices)
    
    # Create memory selection keyboard for prices
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    for memory in memories:
        builder.add(InlineKeyboardButton(
            text=f"{memory} GB narxini kiriting", 
            callback_data=f"set_price_{memory}"
        ))
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    builder.adjust(1)
    
    await message.answer(
        f"✅ **Xotira hajmlari:** {', '.join(map(str, memories))} GB\n\n"
        f"Endi har bir xotira hajmi uchun narxlarni kiriting:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# Price setting handlers for each memory
@router.callback_query(F.data.startswith("set_price_"))
async def set_price_handler(callback: CallbackQuery, state: FSMContext):
    """Handle price setting for specific memory"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    memory = int(callback.data.split("_")[2])
    await state.update_data(current_memory=memory)
    
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        f"💰 **{memory} GB uchun narxlarni kiriting**\n\n"
        f"Format: yangi,yaxshi,o'rtacha\n"
        f"Masalan: 15000000,12000000,9000000",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(AddModelStates.waiting_for_prices)
async def handle_model_prices(message: Message, state: FSMContext):
    """Handle model prices input"""
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, narxlarni kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    try:
        prices = [int(x.strip()) for x in message.text.split(',')]
        if len(prices) != 3:
            raise ValueError("Wrong number of prices")
    except ValueError:
        await message.answer(
            "❌ Noto'g'ri format! Iltimos, 3 ta narxni vergul bilan ajrating.\n"
            "Masalan: 15000000,12000000,9000000",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    data = await state.get_data()
    current_memory = data.get('current_memory')
    memories = data.get('memories')
    name = data.get('name')
    
    if not memories or not name:
        await message.answer(
            "❌ Xatolik yuz berdi! Qaytadan boshlang.",
            reply_markup=get_admin_price_keyboard()
        )
        await state.clear()
        return
    
    # Initialize prices dict if not exists
    if 'prices' not in data:
        data['prices'] = {}
    
    # Store prices for current memory
    data['prices'][str(current_memory)] = {
        'new': prices[0],
        'good': prices[1], 
        'fair': prices[2]
    }
    
    await state.update_data(prices=data['prices'])
    
    # Check if all memories have prices
    if len(data['prices']) == len(memories):
        # Save the complete model
        model_data = {
            'name': name,
            'memories': memories,
            'prices': data['prices']
        }
        
        if save_model(model_data):
            await message.answer(
                f"✅ **Model muvaffaqiyatli qo'shildi!**\n\n"
                f"📱 **Model:** {name}\n"
                f"💾 **Xotira hajmlari:** {', '.join(map(str, memories))} GB",
                reply_markup=get_admin_price_keyboard(),
                parse_mode="Markdown"
            )
        else:
            await message.answer(
                "❌ Xatolik yuz berdi! Model saqlanmadi.",
                reply_markup=get_admin_price_keyboard()
            )
        
        await state.clear()
    else:
        # Continue with next memory
        remaining_memories = [m for m in memories if str(m) not in data['prices']]
        next_memory = remaining_memories[0]
        
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        from aiogram.types import InlineKeyboardButton
        
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text=f"{next_memory} GB narxini kiriting", 
            callback_data=f"set_price_{next_memory}"
        ))
        builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
        builder.adjust(1)
        
        await message.answer(
            f"✅ **{current_memory} GB narxlari saqlandi**\n\n"
            f"Keyingi xotira hajmi uchun narxlarni kiriting:",
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )

def register_admin_handlers(dp):
    """Register all admin handlers"""
    dp.include_router(router) 