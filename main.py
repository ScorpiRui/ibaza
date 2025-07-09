from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F

import asyncio
import logging
from config import BOT_TOKEN
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from keyboards import get_language_selection_keyboard, get_main_menu_keyboard
from languages import get_text, get_language_name
from utils import get_user_language, set_user_language, initialize_default_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Language selection states
class LanguageStates(StatesGroup):
    selecting_language = State()

# Create router for language selection
language_router = Router()

@language_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Handle /start command with language selection"""
    user_id = message.from_user.id
    
    # Check if user already has a language set
    current_language = get_user_language(user_id)
    
    if current_language == 'uz':  # Default, show language selection
        await state.set_state(LanguageStates.selecting_language)
        await message.answer(
            get_text('select_language', 'uz'),
            reply_markup=get_language_selection_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # User already has language, show welcome message
        await show_welcome_message(message, current_language)

@language_router.callback_query(F.data.startswith("lang_"))
async def language_selection_handler(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    user_id = callback.from_user.id
    selected_language = callback.data.split("_")[1]  # Get language code
    
    # Save user language preference
    if set_user_language(user_id, selected_language):
        await callback.answer(get_text('language_selected', selected_language, language=get_language_name(selected_language)))
        
        # Clear state and show welcome message
        await state.clear()
        await show_welcome_message(callback.message, selected_language)
    else:
        await callback.answer("❌ Error saving language preference!")

async def show_welcome_message(message_or_callback, language: str):
    """Show welcome message in selected language"""
    welcome_text = get_text('welcome_title', language) + "\n\n"
    welcome_text += get_text('welcome_description', language) + "\n\n"
    
    # Add services list
    services = get_text('welcome_services', language)
    if isinstance(services, list):
        for service in services:
            welcome_text += f"• {service}\n"
    welcome_text += "\n"
    welcome_text += get_text('welcome_footer', language)
    
    # Check if user is admin
    from config import ADMIN_IDS
    is_admin = message_or_callback.from_user.id in ADMIN_IDS
    
    keyboard = get_main_menu_keyboard(is_admin)
    
    if hasattr(message_or_callback, 'edit_text'):
        await message_or_callback.edit_text(
            welcome_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        await message_or_callback.answer(
            welcome_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

# Register handlers
def register_handlers():
    """Register all handlers"""
    # Register language selection handlers first
    dp.include_router(language_router)
    
    # Register other handlers
    register_user_handlers(dp)
    register_admin_handlers(dp)

async def main():
    """Main function"""
    logger.info("Starting iBaza bot...")
    
    # Initialize default data
    initialize_default_data()
    
    # Register handlers
    register_handlers()
    
    # Start polling
    logger.info("Bot started successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 