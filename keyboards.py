from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Main menu keyboard with different options for users and admins"""
    builder = InlineKeyboardBuilder()
    
    # Common buttons for all users
    builder.add(InlineKeyboardButton(text="🗺️ Xarita", callback_data="map"))
    builder.add(InlineKeyboardButton(text="💰 Narx hisoblagich", callback_data="price_calculator"))
    builder.add(InlineKeyboardButton(text="📅 Nasiya hisoblagich", callback_data="installment"))
    
    # Admin-only buttons
    if is_admin:
        builder.add(InlineKeyboardButton(text="⚙️ Admin panel", callback_data="admin_panel"))
    
    builder.adjust(1)  # One button per row
    return builder.as_markup()

def get_map_keyboard() -> InlineKeyboardMarkup:
    """Map options keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📍 Eng yaqin joylashuv", callback_data="nearest_location"))
    builder.add(InlineKeyboardButton(text="📋 Barcha joylashuvlar", callback_data="all_locations"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_map_keyboard() -> InlineKeyboardMarkup:
    """Admin map options keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="➕ Joylashuv qo'shish", callback_data="add_location"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_panel"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Admin panel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🗺️ Xarita boshqaruvi", callback_data="admin_map"))
    builder.add(InlineKeyboardButton(text="💰 Narx boshqaruvi", callback_data="admin_price"))
    builder.add(InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def get_location_keyboard(location_id: str) -> InlineKeyboardMarkup:
    """Keyboard for individual location with location button"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📍 Joylashuvni ko'rsatish", callback_data=f"show_location_{location_id}"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="all_locations"))
    builder.adjust(1)
    return builder.as_markup()

def get_locations_pagination_keyboard(locations: list, page: int = 0, per_page: int = 5) -> InlineKeyboardMarkup:
    """Pagination keyboard for locations list"""
    builder = InlineKeyboardBuilder()
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_locations = locations[start_idx:end_idx]
    
    for location in page_locations:
        builder.add(InlineKeyboardButton(
            text=location['name'], 
            callback_data=f"location_{location['id']}"
        ))
    
    # Pagination buttons
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text="⬅️", callback_data=f"locations_page_{page-1}"))
    if end_idx < len(locations):
        row.append(InlineKeyboardButton(text="➡️", callback_data=f"locations_page_{page+1}"))
    
    if row:
        builder.row(*row)
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="map"))
    builder.adjust(1)
    return builder.as_markup()

def get_models_keyboard(models: list) -> InlineKeyboardMarkup:
    """Keyboard for selecting device models"""
    builder = InlineKeyboardBuilder()
    
    for model in models:
        builder.add(InlineKeyboardButton(
            text=model['name'], 
            callback_data=f"model_{model['id']}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="price_calculator"))
    builder.adjust(1)
    return builder.as_markup()

def get_memory_keyboard(memories: list) -> InlineKeyboardMarkup:
    """Keyboard for selecting memory options"""
    builder = InlineKeyboardBuilder()
    
    for memory in memories:
        builder.add(InlineKeyboardButton(
            text=f"{memory} GB", 
            callback_data=f"memory_{memory}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="select_model"))
    builder.adjust(2)  # Two buttons per row
    return builder.as_markup()

def get_condition_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting device condition"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🆕 Yangi", callback_data="condition_new"))
    builder.add(InlineKeyboardButton(text="✅ Yaxshi", callback_data="condition_good"))
    builder.add(InlineKeyboardButton(text="🔄 O'rtacha", callback_data="condition_fair"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="select_memory"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_price_keyboard() -> InlineKeyboardMarkup:
    """Admin price management keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="➕ Model qo'shish", callback_data="add_model"))
    builder.add(InlineKeyboardButton(text="✏️ Modellarni tahrirlash", callback_data="edit_models"))
    builder.add(InlineKeyboardButton(text="🗑️ Modellarni o'chirish", callback_data="delete_models"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_panel"))
    builder.adjust(1)
    return builder.as_markup()

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Simple cancel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    return builder.as_markup()

def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    """Admin cancel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_cancel"))
    return builder.as_markup()

def get_admin_map_cancel_keyboard() -> InlineKeyboardMarkup:
    """Admin map cancel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_map_cancel"))
    return builder.as_markup()

def get_admin_price_cancel_keyboard() -> InlineKeyboardMarkup:
    """Admin price cancel keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_price_cancel"))
    return builder.as_markup()

def get_share_location_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard for sharing location"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard with menu button"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏪 Menu")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_models_edit_keyboard(models: list) -> InlineKeyboardMarkup:
    """Keyboard for editing models"""
    builder = InlineKeyboardBuilder()
    
    for model in models:
        builder.add(InlineKeyboardButton(
            text=f"✏️ {model['name']}", 
            callback_data=f"edit_model_{model['id']}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_price"))
    builder.adjust(1)
    return builder.as_markup()

def get_models_delete_keyboard(models: list) -> InlineKeyboardMarkup:
    """Keyboard for deleting models"""
    builder = InlineKeyboardBuilder()
    
    for model in models:
        builder.add(InlineKeyboardButton(
            text=f"🗑️ {model['name']}", 
            callback_data=f"delete_model_{model['id']}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_price"))
    builder.adjust(1)
    return builder.as_markup()

def get_model_edit_options_keyboard(model_id: str) -> InlineKeyboardMarkup:
    """Keyboard for model edit options"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✏️ Nomi", callback_data=f"edit_model_name_{model_id}"))
    builder.add(InlineKeyboardButton(text="💾 Xotira hajmlari", callback_data=f"edit_model_memories_{model_id}"))
    builder.add(InlineKeyboardButton(text="💰 Narxlari", callback_data=f"edit_model_prices_{model_id}"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="edit_models"))
    builder.adjust(1)
    return builder.as_markup()

def get_confirm_delete_keyboard(model_id: str) -> InlineKeyboardMarkup:
    """Keyboard for confirming model deletion"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"confirm_delete_{model_id}"))
    builder.add(InlineKeyboardButton(text="❌ Yo'q, bekor qilish", callback_data="delete_models"))
    builder.adjust(1)
    return builder.as_markup()

