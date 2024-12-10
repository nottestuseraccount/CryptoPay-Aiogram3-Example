from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from aiocryptopay import AioCryptoPay
from config import cryptopay_token, network
from aiogram.utils.keyboard import InlineKeyboardBuilder

cryptopay = AioCryptoPay(token=cryptopay_token, network=network)
router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer("Используй команду /pay <сумма>")
    

@router.message(Command("pay"))
async def command_pay(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Ты не указал сумму!")
        return
    
    args = command.args.split(" ")
    if len(args) != 1:
        await message.answer("Используй команду /pay <сумма>")
        return
    try:
        amount = int(command.args)
    except ValueError:
        await message.answer("Используй команду /pay <сумма>")
        return
    
    invoice = await cryptopay.create_invoice(amount=amount, fiat='RUB', currency_type='fiat')
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Ссылка на оплату", url=invoice.bot_invoice_url))
    builder.add(InlineKeyboardButton(text="Проверить оплату", callback_data=f"CHECK|{invoice.invoice_id}"))
    builder.add(InlineKeyboardButton(text="Отменить оплату", callback_data=f"CANCEL|{invoice.invoice_id}"))
    builder.adjust(1)
    text = f"""Покупка на сумму:{amount} RUB
Используй кнопки ниже 👇"""
    await message.answer(text=text, reply_markup=builder.as_markup())