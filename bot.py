import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, ADMIN_IDS
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from handlers.installment import register_installment_handlers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Register handlers
register_admin_handlers(dp)
register_user_handlers(dp)
register_installment_handlers(dp)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Main start command with welcome message and main menu"""
    user_id = message.from_user.id
    is_admin = user_id in ADMIN_IDS
    
    welcome_text = (
        "🏪 **iBaza Tech Resale Market** ga xush kelibsiz!\n\n"
        "Biz sizga eng yaxshi texnologiya mahsulotlarini taklif qilamiz.\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:"
    )
    
    from keyboards import get_main_menu_keyboard
    keyboard = get_main_menu_keyboard(is_admin)
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

async def main():
    """Main function to start the bot"""
    logger.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 