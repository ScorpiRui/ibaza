from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import get_main_menu_keyboard, get_cancel_keyboard
from config import ADMIN_IDS

router = Router()

# Installment calculator states
class InstallmentStates(StatesGroup):
    waiting_for_total = State()
    waiting_for_initial = State()

def calculate_installments_with_interest(total_sum: float, initial_payment: float) -> dict:
    """Calculate installment payments with interest rates"""
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

@router.callback_query(F.data == "installment")
async def installment_handler(callback: CallbackQuery, state: FSMContext):
    """Handle installment calculator menu"""
    if not callback.message:
        return
    
    is_admin = callback.from_user.id in ADMIN_IDS
    
    if is_admin:
        # Admin flow - ask for total price
        await state.set_state(InstallmentStates.waiting_for_total)
        await callback.message.edit_text(
            "📅 **Nasiya hisoblagich (Admin)**\n\n"
            "Telefonning umumiy narxini USD da kiriting (masalan: 1000):",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # User flow - ask for total price
        await state.set_state(InstallmentStates.waiting_for_total)
        await callback.message.edit_text(
            "📅 **Nasiya hisoblagich**\n\n"
            "Telefonning narxini USD da kiriting (masalan: 500):",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
    
    await callback.answer()

@router.message(InstallmentStates.waiting_for_total)
async def handle_total_sum(message: Message, state: FSMContext):
    """Handle total sum input"""
    if not message.text:
        await message.answer(
            "❌ Iltimos, to'g'ri raqam kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    try:
        total_sum = float(message.text)
        if total_sum <= 0:
            raise ValueError("Negative or zero price")
    except ValueError:
        await message.answer(
            "❌ Iltimos, to'g'ri raqam kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    is_admin = message.from_user.id in ADMIN_IDS
    
    if is_admin:
        # Admin flow - ask for initial payment
        await state.update_data(total_sum=total_sum)
        await state.set_state(InstallmentStates.waiting_for_initial)
        
        await message.answer(
            f"✅ **Umumiy summa:** ${total_sum}\n\n"
            f"Dastlabki to'lov miqdorini USD da kiriting:",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # User flow - calculate with 40% initial payment
        initial_payment = round(total_sum * 0.4, 2)
        
        if initial_payment >= total_sum:
            await message.answer(
                "❌ Dastlabki to'lov umumiy summadan katta yoki teng bo'lishi mumkin emas!",
                reply_markup=get_cancel_keyboard()
            )
            return
        
        installment_plan = calculate_installments_with_interest(total_sum, initial_payment)
        
        response = f"📱 **Telefon narxi:** ${total_sum}\n"
        response += f"💵 **Dastlabki to'lov (40%):** ${initial_payment}\n\n"
        response += "📅 **Oylik to'lovlar:**\n\n"
        
        for months, payment in installment_plan.items():
            response += f"{months.replace('_month', '  oyga')}: ${payment}\n"
        
        keyboard = get_main_menu_keyboard(is_admin)
        await message.answer(
            response,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        await state.clear()

@router.message(InstallmentStates.waiting_for_initial)
async def handle_initial_payment(message: Message, state: FSMContext):
    """Handle initial payment input (admin only)"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    if not message.text:
        await message.answer(
            "❌ Iltimos, to'g'ri raqam kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    try:
        initial_payment = float(message.text)
        if initial_payment <= 0:
            raise ValueError("Negative or zero payment")
    except ValueError:
        await message.answer(
            "❌ Iltimos, to'g'ri raqam kiriting!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    data = await state.get_data()
    total_sum = data.get('total_sum')
    
    if total_sum is None:
        await message.answer(
            "❌ Xatolik yuz berdi! Qaytadan boshlang.",
            reply_markup=get_main_menu_keyboard(True)
        )
        await state.clear()
        return
    
    if initial_payment >= total_sum:
        await message.answer(
            "❌ Dastlabki to'lov umumiy summadan katta yoki teng bo'lishi mumkin emas!",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    installment_plan = calculate_installments_with_interest(total_sum, initial_payment)
    
    response = f"📱 **Telefon narxi:** ${total_sum}\n"
    response += f"💵 **Dastlabki to'lov:** ${initial_payment}\n\n"
    response += "📅 **Oylik to'lovlar:**\n\n"
    
    for months, payment in installment_plan.items():
        response += f"{months.replace('_month', '  oyga')}: ${payment}\n"
    
    keyboard = get_main_menu_keyboard(True)  # Admin keyboard
    await message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    await state.clear()

def register_installment_handlers(dp):
    """Register all installment handlers"""
    dp.include_router(router) 