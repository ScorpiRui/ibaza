from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token - replace with your actual token
BOT_TOKEN = "7951892270:AAEaFw3h2Q_hOL5TH4d2JsD-KuZ4K9fxRR4"

# Admin list
ADMIN_IDS = [
    6709695039,
]

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# User states
user_states = {}

def calculate_installments_with_interest(total_sum, initial_payment):
    rates = {
        1: 0.13,
        2: 0.22,
        3: 0.35,
        4: 0.44,
        5: 0.53,
        6: 0.60,
        7: 0.68,
        8: 0.77
    }

    remaining = total_sum - initial_payment
    installments = {}

    for months, rate in rates.items():
        total_with_interest = remaining * (1 + rate)
        monthly_payment = total_with_interest / months
        installments[f"{months}_month"] = round(monthly_payment, 1)

    return installments

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "Admin panel:\n"
            "Telefonning umumiy narxini USD da kiriting (masalan: 1000):"
        )
        user_states[message.from_user.id] = {"state": "admin_total"}
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Tovarni hisoblash", callback_data="calculate")],
                [InlineKeyboardButton(text="Shartnoma", callback_data="contract")]
            ]
        )
        await message.answer(
            "Assalomu alaykum! iCompfort rasmiy nasiya savdo bo'limiga xush kelibsiz!",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "calculate")
async def process_calculate_callback(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in ADMIN_IDS:
        return
    await callback_query.message.answer(
        "Telefonning narxini USD da kiriting (masalan: 500):"
    )
    user_states[callback_query.from_user.id] = {"state": "waiting_total_sum"}
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "contract")
async def process_contract_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer_document(
        document="BQACAgIAAxkBAAMmaDwinaGFK7qbOdOCkRTjpCr8ITgAAvRwAAJ05eBJHUKqquKRIhE2BA"
    )
    await callback_query.answer()

@dp.message()
async def handle_messages(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_states:
        if user_id in ADMIN_IDS:
            await message.answer(
                "Telefonning umumiy narxini USD da kiriting (masalan: 1000):"
            )
            user_states[user_id] = {"state": "admin_total"}
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Tovarni hisoblash", callback_data="calculate")],
                    [InlineKeyboardButton(text="Shartnoma", callback_data="contract")]
                ]
            )
            await message.answer(
                "Iltimos, hisoblashni boshlash uchun tugmani bosing:",
                reply_markup=keyboard
            )
        return

    state = user_states[user_id]["state"]
    
    try:
        if state == "admin_total":
            if user_id not in ADMIN_IDS:
                return
            total_sum = float(message.text)
            user_states[user_id] = {
                "state": "admin_initial",
                "total_sum": total_sum
            }
            await message.answer(
                f"Umumiy summa: ${total_sum}\n"
                "Dastlabki to'lov miqdorini USD da kiriting:"
            )
            
        elif state == "admin_initial":
            if user_id not in ADMIN_IDS:
                return
            initial_payment = float(message.text)
            total_sum = user_states[user_id]["total_sum"]
            
            if initial_payment >= total_sum:
                await message.answer("Dastlabki to'lov umumiy summadan katta yoki teng bo'lishi mumkin emas!")
                return
                
            installment_plan = calculate_installments_with_interest(total_sum, initial_payment)
            
            response = f"📱 Telefon narxi: ${total_sum}\n"
            response += f"💵 Dastlabki to'lov: ${initial_payment}\n\n"
            response += "📅 Oylik to'lovlar:\n\n"
            
            for months, payment in installment_plan.items():
                response += f"{months.replace('_month', '  oyga')}: ${payment}\n"
            
            await message.answer(response)
            del user_states[user_id]
            
        elif state == "waiting_total_sum":
            if user_id in ADMIN_IDS:
                return
            total_sum = float(message.text)
            initial_payment = round(total_sum * 0.4, 2)  # 40% of total price
            
            installment_plan = calculate_installments_with_interest(total_sum, initial_payment)
            
            response = f"📱 Telefon narxi: ${total_sum}\n"
            response += f"💵 Dastlabki to'lov (40%): ${initial_payment}\n\n"
            response += "📅 Oylik to'lovlar:\n\n"
            
            for months, payment in installment_plan.items():
                response += f"{months.replace('_month', '  oyga')}: ${payment}\n"
            
            await message.answer(response)
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Yangi hisoblash", callback_data="calculate")]
                ]
            )
            await message.answer("Yangi hisoblash uchun tugmani bosing:", reply_markup=keyboard)
            del user_states[user_id]
            
    except ValueError:
        await message.answer("Iltimos, to'g'ri raqam kiriting!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())