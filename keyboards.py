from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Main menu keyboard with different options for users and admins"""
    builder = InlineKeyboardBuilder()
    
    # Common buttons for all users
    builder.add(InlineKeyboardButton(text="🗺️ Do'konlar xaritasi", callback_data="map"))
    builder.add(InlineKeyboardButton(text="💰 Telefonimni narxla", callback_data="price_calculator"))
    builder.add(InlineKeyboardButton(text="📅 Nasiya hisoblash", callback_data="installment"))
    builder.add(InlineKeyboardButton(text="📞 Call center", callback_data="call_center"))
    builder.add(InlineKeyboardButton(text="👨‍💼 Admin", callback_data="admin_contact"))
    
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

def get_models_pagination_keyboard(models: list, page: int = 0, per_page: int = 8) -> InlineKeyboardMarkup:
    """Pagination keyboard for models list"""
    builder = InlineKeyboardBuilder()
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_models = models[start_idx:end_idx]
    
    for model in page_models:
        builder.add(InlineKeyboardButton(
            text=model['name'], 
            callback_data=f"model_{model['name']}"
        ))
    
    # Pagination buttons
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text="⬅️", callback_data=f"models_page_{page-1}"))
    if end_idx < len(models):
        row.append(InlineKeyboardButton(text="➡️", callback_data=f"models_page_{page+1}"))
    
    if row:
        builder.row(*row)
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def get_models_keyboard(models: list) -> InlineKeyboardMarkup:
    """Keyboard for selecting device models"""
    builder = InlineKeyboardBuilder()
    
    for model in models:
        builder.add(InlineKeyboardButton(
            text=model['name'], 
            callback_data=f"model_{model['name']}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="price_calculator"))
    builder.adjust(1)
    return builder.as_markup()

def get_memory_keyboard(memories: list) -> InlineKeyboardMarkup:
    """Keyboard for selecting memory options"""
    builder = InlineKeyboardBuilder()
    
    for memory in memories:
        if memory == 1024:
            display_text = "1 TB"
        else:
            display_text = f"{memory} GB"
        
        builder.add(InlineKeyboardButton(
            text=display_text, 
            callback_data=f"memory_{memory}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="select_model"))
    builder.adjust(2)  # Two buttons per row
    return builder.as_markup()

def get_condition_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting device condition"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🆕 Ideal", callback_data="condition_new"))
    builder.add(InlineKeyboardButton(text="✅ Yaxshi", callback_data="condition_good"))
    builder.add(InlineKeyboardButton(text="🔄 Ortacha", callback_data="condition_fair"))
    builder.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_memory"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_price_keyboard() -> InlineKeyboardMarkup:
    """Admin price management keyboard - now shows Google Sheets link"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📊 Google Sheets da narxlarni boshqarish", callback_data="admin_price"))
    builder.add(InlineKeyboardButton(text="🔄 Narxlarni yangilash", callback_data="refresh_prices"))
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

def get_language_selection_keyboard():
    """Get language selection keyboard"""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"))
    builder.add(InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"))
    builder.add(InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_eng"))
    builder.adjust(1)
    
    return builder.as_markup()

