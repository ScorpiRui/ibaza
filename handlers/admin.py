from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import (
    get_admin_panel_keyboard, get_admin_map_keyboard, get_admin_price_keyboard,
    get_cancel_keyboard, get_admin_cancel_keyboard,
    get_admin_map_cancel_keyboard, get_admin_price_cancel_keyboard,
    get_models_edit_keyboard, get_models_delete_keyboard, get_model_edit_options_keyboard,
    get_confirm_delete_keyboard
)
from utils import save_location, save_model, get_locations, get_models, update_model, delete_model, get_model_by_id
from config import ADMIN_IDS
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = Router()
#cdalsfa;lsfj;asjfsa
# Admin states for adding location
class AddLocationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_location = State()

# Admin states for adding model
class AddModelStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_memory_selection = State()
    waiting_for_prices = State()

# Admin states for editing model
class EditModelStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_memory_selection = State()
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
    await state.set_state(AddModelStates.waiting_for_memory_selection)
    
    # Create memory selection keyboard
    builder = InlineKeyboardBuilder()
    
    # Memory options with proper labels
    memory_options = [
        ("64 GB", "64"),
        ("128 GB", "128"), 
        ("256 GB", "256"),
        ("512 GB", "512"),
        ("1 TB", "1024")
    ]
    
    # Add memory selection buttons
    for label, value in memory_options:
        builder.add(InlineKeyboardButton(
            text=f"⬜ {label}", 
            callback_data=f"select_memory_{value}"
        ))
    
    # Add Done and Cancel buttons
    builder.add(InlineKeyboardButton(text="✅ Tugatish", callback_data="done_memory_selection"))
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    
    # Arrange buttons in a grid
    builder.adjust(2, 2, 1, 1)  # 2 columns for memory options, then Done and Cancel
    
    await message.answer(
        f"✅ **Model:** {message.text}\n\n"
        f"Xotira hajmlarini tanlang (bir nechtasini tanlash mumkin):",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("select_memory_"))
async def handle_memory_selection(callback: CallbackQuery, state: FSMContext):
    """Handle memory selection"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    memory_value = callback.data.split("_")[2]
    data = await state.get_data()
    
    # Initialize selected memories if not exists
    if 'selected_memories' not in data:
        data['selected_memories'] = []
    
    # Toggle memory selection
    if memory_value in data['selected_memories']:
        data['selected_memories'].remove(memory_value)
    else:
        data['selected_memories'].append(memory_value)
    
    await state.update_data(selected_memories=data['selected_memories'])
    
    # Update the keyboard to show selected items
    builder = InlineKeyboardBuilder()
    
    # Memory options with proper labels
    memory_options = [
        ("64 GB", "64"),
        ("128 GB", "128"), 
        ("256 GB", "256"),
        ("512 GB", "512"),
        ("1 TB", "1024")
    ]
    
    # Add memory selection buttons with checkmarks
    for label, value in memory_options:
        checkbox = "✅" if value in data['selected_memories'] else "⬜"
        builder.add(InlineKeyboardButton(
            text=f"{checkbox} {label}", 
            callback_data=f"select_memory_{value}"
        ))
    
    # Add Done and Cancel buttons
    builder.add(InlineKeyboardButton(text="✅ Tugatish", callback_data="done_memory_selection"))
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    
    # Arrange buttons in a grid
    builder.adjust(2, 2, 1, 1)
    
    # Show selected memories count
    selected_count = len(data['selected_memories'])
    selected_text = f"Tanlangan: {selected_count} ta" if selected_count > 0 else "Hech qanday tanlanmagan"
    
    await callback.message.edit_text(
        f"✅ **Model:** {data.get('name', '')}\n\n"
        f"Xotira hajmlarini tanlang (bir nechtasini tanlash mumkin):\n"
        f"📊 {selected_text}",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "done_memory_selection")
async def handle_done_memory_selection(callback: CallbackQuery, state: FSMContext):
    """Handle done button for memory selection"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    data = await state.get_data()
    selected_memories = data.get('selected_memories', [])
    
    if not selected_memories:
        await callback.answer("❌ Kamida bitta xotira hajmini tanlang!")
        return
    
    # Convert string values to integers and sort them
    memories = sorted([int(m) for m in selected_memories])
    await state.update_data(memories=memories)
    await state.set_state(AddModelStates.waiting_for_prices)
    
    # Create memory selection keyboard for prices
    builder = InlineKeyboardBuilder()
    
    # Convert memory values to display labels
    memory_labels = []
    for memory in memories:
        if memory == 1024:
            label = "1 TB"
        else:
            label = f"{memory} GB"
        memory_labels.append(label)
        builder.add(InlineKeyboardButton(
            text=f"{label} narxini kiriting", 
            callback_data=f"set_price_{memory}"
        ))
    
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    builder.adjust(1)
    
    # Format memory display
    memory_display = []
    for memory in memories:
        if memory == 1024:
            memory_display.append("1 TB")
        else:
            memory_display.append(f"{memory} GB")
    
    await callback.message.edit_text(
        f"✅ **Xotira hajmlari:** {', '.join(memory_display)}\n\n"
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
    
    # Format memory label
    if memory == 1024:
        memory_label = "1 TB"
    else:
        memory_label = f"{memory} GB"
    
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        f"💰 **{memory_label} uchun narxlarni kiriting**\n\n"
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
            # Format memory display for success message
            memory_display = []
            for memory in memories:
                if memory == 1024:
                    memory_display.append("1 TB")
                else:
                    memory_display.append(f"{memory} GB")
            
            await message.answer(
                f"✅ **Model muvaffaqiyatli qo'shildi!**\n\n"
                f"📱 **Model:** {name}\n"
                f"💾 **Xotira hajmlari:** {', '.join(memory_display)}",
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
        
        builder = InlineKeyboardBuilder()
        
        # Format memory label for next memory
        if next_memory == 1024:
            next_memory_label = "1 TB"
        else:
            next_memory_label = f"{next_memory} GB"
        
        # Format current memory label for display
        if current_memory == 1024:
            current_memory_label = "1 TB"
        else:
            current_memory_label = f"{current_memory} GB"
        
        builder.add(InlineKeyboardButton(
            text=f"{next_memory_label} narxini kiriting", 
            callback_data=f"set_price_{next_memory}"
        ))
        builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
        builder.adjust(1)
        
        await message.answer(
            f"✅ **{current_memory_label} narxlari saqlandi**\n\n"
            f"Keyingi xotira hajmi uchun narxlarni kiriting:",
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )

@router.callback_query(F.data == "cancel")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    """Handle cancel button"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    current_state = await state.get_state()
    
    if current_state == AddModelStates.waiting_for_memory_selection:
        # Return to admin price panel
        await state.clear()
        keyboard = get_admin_price_keyboard()
        
        await callback.message.edit_text(
            "💰 **Narx boshqaruvi**\n\n"
            "Qurilma modellarini boshqarish:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif current_state == AddModelStates.waiting_for_prices:
        # Return to admin price panel
        await state.clear()
        keyboard = get_admin_price_keyboard()
        
        await callback.message.edit_text(
            "💰 **Narx boshqaruvi**\n\n"
            "Qurilma modellarini boshqarish:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif current_state == EditModelStates.waiting_for_name:
        # Return to admin price panel
        await state.clear()
        keyboard = get_admin_price_keyboard()
        
        await callback.message.edit_text(
            "💰 **Narx boshqaruvi**\n\n"
            "Qurilma modellarini boshqarish:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif current_state == EditModelStates.waiting_for_memory_selection:
        # Return to admin price panel
        await state.clear()
        keyboard = get_admin_price_keyboard()
        
        await callback.message.edit_text(
            "💰 **Narx boshqaruvi**\n\n"
            "Qurilma modellarini boshqarish:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    elif current_state == EditModelStates.waiting_for_prices:
        # Return to admin price panel
        await state.clear()
        keyboard = get_admin_price_keyboard()
        
        await callback.message.edit_text(
            "💰 **Narx boshqaruvi**\n\n"
            "Qurilma modellarini boshqarish:",
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

@router.callback_query(F.data == "edit_models")
async def edit_models_handler(callback: CallbackQuery):
    """Handle edit models request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    models = get_models()
    if not models:
        await callback.message.edit_text(
            "❌ Hech qanday model mavjud emas!",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    keyboard = get_models_edit_keyboard(models)
    
    await callback.message.edit_text(
        "✏️ **Modellarni tahrirlash**\n\n"
        "Tahrirlash uchun modelni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "delete_models")
async def delete_models_handler(callback: CallbackQuery):
    """Handle delete models request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    models = get_models()
    if not models:
        await callback.message.edit_text(
            "❌ Hech qanday model mavjud emas!",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    keyboard = get_models_delete_keyboard(models)
    
    await callback.message.edit_text(
        "🗑️ **Modellarni o'chirish**\n\n"
        "O'chirish uchun modelni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("edit_model_") & ~F.data.startswith("edit_model_name_") & ~F.data.startswith("edit_model_memories_") & ~F.data.startswith("edit_model_prices_"))
async def edit_model_handler(callback: CallbackQuery):
    """Handle edit specific model request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[2]
    model = get_model_by_id(model_id)
    
    if not model:
        await callback.answer("❌ Model topilmadi!")
        return
    
    keyboard = get_model_edit_options_keyboard(model_id)
    
    # Format memory display
    memory_display = []
    for memory in model.get('memories', []):
        if memory == 1024:
            memory_display.append("1 TB")
        else:
            memory_display.append(f"{memory} GB")
    
    await callback.message.edit_text(
        f"✏️ **Model tahrirlash**\n\n"
        f"📱 **Model:** {model['name']}\n"
        f"💾 **Xotira hajmlari:** {', '.join(memory_display)}\n\n"
        f"Nima tahrirlashni xohlaysiz?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("delete_model_"))
async def delete_model_handler(callback: CallbackQuery):
    """Handle delete specific model request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[2]
    model = get_model_by_id(model_id)
    
    if not model:
        await callback.answer("❌ Model topilmadi!")
        return
    
    keyboard = get_confirm_delete_keyboard(model_id)
    
    await callback.message.edit_text(
        f"🗑️ **Model o'chirish**\n\n"
        f"📱 **Model:** {model['name']}\n\n"
        f"Bu modelni o'chirishni xohlaysizmi?\n"
        f"⚠️ Bu amalni qaytarib bo'lmaydi!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete_model_handler(callback: CallbackQuery):
    """Handle confirm delete model"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[2]
    model = get_model_by_id(model_id)
    
    if not model:
        await callback.answer("❌ Model topilmadi!")
        return
    
    if delete_model(model_id):
        await callback.message.edit_text(
            f"✅ **Model muvaffaqiyatli o'chirildi!**\n\n"
            f"📱 **Model:** {model['name']}",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ Xatolik yuz berdi! Model o'chirilmadi.",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )

@router.callback_query(F.data.startswith("edit_model_name_"))
async def edit_model_name_handler(callback: CallbackQuery, state: FSMContext):
    """Handle edit model name request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[3]
    logger.info(f"Edit model name handler called for model_id: {model_id}")
    model = get_model_by_id(model_id)
    
    if not model:
        logger.error(f"Model not found for ID: {model_id}")
        await callback.answer("❌ Model topilmadi!")
        return
    
    logger.info(f"Found model: {model['name']}")
    await state.set_state(EditModelStates.waiting_for_name)
    await state.update_data(model_id=model_id, current_model=model)
    
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        f"✏️ **Model nomini tahrirlash**\n\n"
        f"Joriy nom: **{model['name']}**\n\n"
        f"Yangi nomni kiriting:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("edit_model_memories_"))
async def edit_model_memories_handler(callback: CallbackQuery, state: FSMContext):
    """Handle edit model memories request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[3]
    logger.info(f"Edit model memories handler called for model_id: {model_id}")
    model = get_model_by_id(model_id)
    
    if not model:
        logger.error(f"Model not found for ID: {model_id}")
        await callback.answer("❌ Model topilmadi!")
        return
    
    logger.info(f"Found model: {model['name']}")
    await state.set_state(EditModelStates.waiting_for_memory_selection)
    await state.update_data(model_id=model_id, current_model=model)
    
    # Create memory selection keyboard with current selections
    builder = InlineKeyboardBuilder()
    
    # Memory options with proper labels
    memory_options = [
        ("64 GB", "64"),
        ("128 GB", "128"), 
        ("256 GB", "256"),
        ("512 GB", "512"),
        ("1 TB", "1024")
    ]
    
    current_memories = set(str(m) for m in model.get('memories', []))
    
    # Add memory selection buttons with checkmarks
    for label, value in memory_options:
        checkbox = "✅" if value in current_memories else "⬜"
        builder.add(InlineKeyboardButton(
            text=f"{checkbox} {label}", 
            callback_data=f"edit_select_memory_{value}"
        ))
    
    # Add Done and Cancel buttons
    builder.add(InlineKeyboardButton(text="✅ Tugatish", callback_data="edit_done_memory_selection"))
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    
    # Arrange buttons in a grid
    builder.adjust(2, 2, 1, 1)
    
    await callback.message.edit_text(
        f"✏️ **Xotira hajmlarini tahrirlash**\n\n"
        f"Model: **{model['name']}**\n\n"
        f"Xotira hajmlarini tanlang (bir nechtasini tanlash mumkin):",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("edit_model_prices_"))
async def edit_model_prices_handler(callback: CallbackQuery, state: FSMContext):
    """Handle edit model prices request"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    model_id = callback.data.split("_")[3]
    logger.info(f"Edit model prices handler called for model_id: {model_id}")
    model = get_model_by_id(model_id)
    
    if not model:
        logger.error(f"Model not found for ID: {model_id}")
        await callback.answer("❌ Model topilmadi!")
        return
    
    logger.info(f"Found model: {model['name']}")
    await state.set_state(EditModelStates.waiting_for_prices)
    await state.update_data(model_id=model_id, current_model=model)
    
    # Create memory selection keyboard for prices
    builder = InlineKeyboardBuilder()
    
    # Convert memory values to display labels
    for memory in model.get('memories', []):
        if memory == 1024:
            label = "1 TB"
        else:
            label = f"{memory} GB"
        builder.add(InlineKeyboardButton(
            text=f"{label} narxini tahrirlash", 
            callback_data=f"edit_set_price_{memory}"
        ))
    
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"✏️ **Narxlarni tahrirlash**\n\n"
        f"Model: **{model['name']}**\n\n"
        f"Qaysi xotira hajmi uchun narxlarni tahrirlashni xohlaysiz?",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.message(EditModelStates.waiting_for_name)
async def handle_edit_model_name(message: Message, state: FSMContext):
    """Handle edit model name input"""
    if not is_admin(message.from_user.id):
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, model nomini kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    data = await state.get_data()
    model_id = data.get('model_id')
    current_model = data.get('current_model')
    
    if not model_id or not current_model:
        await message.answer(
            "❌ Xatolik yuz berdi! Qaytadan boshlang.",
            reply_markup=get_admin_price_keyboard()
        )
        await state.clear()
        return
    
    # Update the model
    updated_model = current_model.copy()
    updated_model['name'] = message.text
    
    if update_model(model_id, updated_model):
        await message.answer(
            f"✅ **Model nomi muvaffaqiyatli yangilandi!**\n\n"
            f"📱 **Yangi nom:** {message.text}",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Xatolik yuz berdi! Model yangilanmadi.",
            reply_markup=get_admin_price_keyboard()
        )
    
    await state.clear()

@router.callback_query(F.data.startswith("edit_select_memory_"))
async def handle_edit_memory_selection(callback: CallbackQuery, state: FSMContext):
    """Handle edit memory selection"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    memory_value = callback.data.split("_")[3]
    data = await state.get_data()
    
    # Initialize selected memories if not exists
    if 'selected_memories' not in data:
        current_model = data.get('current_model', {})
        data['selected_memories'] = [str(m) for m in current_model.get('memories', [])]
    
    # Toggle memory selection
    if memory_value in data['selected_memories']:
        data['selected_memories'].remove(memory_value)
    else:
        data['selected_memories'].append(memory_value)
    
    await state.update_data(selected_memories=data['selected_memories'])
    
    # Update the keyboard to show selected items
    builder = InlineKeyboardBuilder()
    
    # Memory options with proper labels
    memory_options = [
        ("64 GB", "64"),
        ("128 GB", "128"), 
        ("256 GB", "256"),
        ("512 GB", "512"),
        ("1 TB", "1024")
    ]
    
    # Add memory selection buttons with checkmarks
    for label, value in memory_options:
        checkbox = "✅" if value in data['selected_memories'] else "⬜"
        builder.add(InlineKeyboardButton(
            text=f"{checkbox} {label}", 
            callback_data=f"edit_select_memory_{value}"
        ))
    
    # Add Done and Cancel buttons
    builder.add(InlineKeyboardButton(text="✅ Tugatish", callback_data="edit_done_memory_selection"))
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    
    # Arrange buttons in a grid
    builder.adjust(2, 2, 1, 1)
    
    # Show selected memories count
    selected_count = len(data['selected_memories'])
    selected_text = f"Tanlangan: {selected_count} ta" if selected_count > 0 else "Hech qanday tanlanmagan"
    
    current_model = data.get('current_model', {})
    
    await callback.message.edit_text(
        f"✏️ **Xotira hajmlarini tahrirlash**\n\n"
        f"Model: **{current_model.get('name', '')}**\n\n"
        f"Xotira hajmlarini tanlang (bir nechtasini tanlash mumkin):\n"
        f"📊 {selected_text}",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "edit_done_memory_selection")
async def handle_edit_done_memory_selection(callback: CallbackQuery, state: FSMContext):
    """Handle done button for edit memory selection"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    data = await state.get_data()
    selected_memories = data.get('selected_memories', [])
    model_id = data.get('model_id')
    current_model = data.get('current_model')
    
    if not selected_memories:
        await callback.answer("❌ Kamida bitta xotira hajmini tanlang!")
        return
    
    if not model_id or not current_model:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    # Convert string values to integers and sort them
    memories = sorted([int(m) for m in selected_memories])
    
    # Update the model
    updated_model = current_model.copy()
    updated_model['memories'] = memories
    
    # Remove prices for memories that are no longer available
    if 'prices' in updated_model:
        updated_prices = {}
        for memory_str in updated_model['prices']:
            if int(memory_str) in memories:
                updated_prices[memory_str] = updated_model['prices'][memory_str]
        updated_model['prices'] = updated_prices
    
    if update_model(model_id, updated_model):
        # Format memory display
        memory_display = []
        for memory in memories:
            if memory == 1024:
                memory_display.append("1 TB")
            else:
                memory_display.append(f"{memory} GB")
        
        await callback.message.edit_text(
            f"✅ **Xotira hajmlari muvaffaqiyatli yangilandi!**\n\n"
            f"📱 **Model:** {current_model.get('name', '')}\n"
            f"💾 **Yangi xotira hajmlari:** {', '.join(memory_display)}",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ Xatolik yuz berdi! Xotira hajmlari yangilanmadi.",
            reply_markup=get_admin_price_keyboard()
        )
    
    await state.clear()

@router.callback_query(F.data.startswith("edit_set_price_"))
async def edit_set_price_handler(callback: CallbackQuery, state: FSMContext):
    """Handle edit price setting for specific memory"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Ruxsat yo'q!")
        return
    
    if not callback.data:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    memory = int(callback.data.split("_")[3])
    data = await state.get_data()
    current_model = data.get('current_model')
    
    if not current_model:
        await callback.answer("❌ Xatolik yuz berdi!")
        return
    
    await state.update_data(current_memory=memory)
    
    # Format memory label
    if memory == 1024:
        memory_label = "1 TB"
    else:
        memory_label = f"{memory} GB"
    
    # Get current prices if they exist
    current_prices = current_model.get('prices', {}).get(str(memory), {})
    current_prices_text = ""
    if current_prices:
        current_prices_text = f"\nJoriy narxlar:\n🆕 Yangi: {current_prices.get('new', 'N/A'):,} so'm\n✅ Yaxshi: {current_prices.get('good', 'N/A'):,} so'm\n🔄 O'rtacha: {current_prices.get('fair', 'N/A'):,} so'm\n\n"
    
    keyboard = get_cancel_keyboard()
    
    await callback.message.edit_text(
        f"💰 **{memory_label} uchun narxlarni tahrirlash**\n\n"
        f"Model: **{current_model.get('name', '')}**{current_prices_text}"
        f"Yangi narxlarni kiriting:\n"
        f"Format: yangi,yaxshi,o'rtacha\n"
        f"Masalan: 15000000,12000000,9000000",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(EditModelStates.waiting_for_prices)
async def handle_edit_model_prices(message: Message, state: FSMContext):
    """Handle edit model prices input"""
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
    model_id = data.get('model_id')
    current_model = data.get('current_model')
    
    if not current_model or not model_id:
        await message.answer(
            "❌ Xatolik yuz berdi! Qaytadan boshlang.",
            reply_markup=get_admin_price_keyboard()
        )
        await state.clear()
        return
    
    # Update the model with new prices
    updated_model = current_model.copy()
    if 'prices' not in updated_model:
        updated_model['prices'] = {}
    
    updated_model['prices'][str(current_memory)] = {
        'new': prices[0],
        'good': prices[1], 
        'fair': prices[2]
    }
    
    if update_model(model_id, updated_model):
        # Format memory label
        if current_memory == 1024:
            memory_label = "1 TB"
        else:
            memory_label = f"{current_memory} GB"
        
        await message.answer(
            f"✅ **{memory_label} narxlari muvaffaqiyatli yangilandi!**\n\n"
            f"📱 **Model:** {current_model.get('name', '')}\n"
            f"💰 **Yangi narxlar:**\n"
            f"🆕 Yangi: {prices[0]:,} so'm\n"
            f"✅ Yaxshi: {prices[1]:,} so'm\n"
            f"🔄 O'rtacha: {prices[2]:,} so'm",
            reply_markup=get_admin_price_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ Xatolik yuz berdi! Narxlar yangilanmadi.",
            reply_markup=get_admin_price_keyboard()
        )
    
    await state.clear()

def register_admin_handlers(dp):
    """Register all admin handlers"""
    dp.include_router(router) 