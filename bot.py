import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, ADMIN_IDS
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from handlers.installment import register_installment_handlers
from utils import initialize_default_data

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
        "🏪 **iBaza** telefon va gadgetlar olamiga xush kelibsiz\n\n"
        "Biz sizga eng yaxshi texnologik mahsulotlarni xarid qilishda quyidagi xizmatlarni taklif qilamiz:\n\n"
        "• Qayerdan va qanday qilib eng yaxshi narxlarda xarid qilish\n"
        "• Nasiya (muddatli to'lov) asosida xarid qilish imkoniyati\n"
        "• Telefon va boshqa qurilmalar narxini aniqlab berish\n\n"
        "Sifatli, qulay va ishonchli xizmatlar biz bilan!"
    )
    
    from keyboards import get_main_menu_keyboard
    keyboard = get_main_menu_keyboard(is_admin)
    
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

async def main():
    """Main function to start the bot"""
    logger.info("Starting iBaza Tech Resale Market Bot...")
    
    # Initialize default data (locations and Google Sheets template)
    logger.info("Initializing default data...")
    initialize_default_data()
    
    # Start the bot
    logger.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 