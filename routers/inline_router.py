from aiogram import F, Router
from aiogram.types import CallbackQuery
from routers.message_router import cryptopay
router = Router()

@router.callback_query(F.data.startswith("CHECK|"))
async def check_invoice(call: CallbackQuery):
    invoice_id = int(call.data.split("|")[1])
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    if invoice.status == "active":
        await call.answer("Оплата не обнаружена!", show_alert=True)
        return
    if invoice.status == "paid":
        await call.message.delete()
        await call.message.answer("Оплата обнаружена спасибо за покупку!")
    
    else:
        await call.message.delete()
        await call.message.answer("Срок инвойса истек!")

@router.callback_query(F.data.startswith("CANCEL|"))
async def cancel_invoice(call: CallbackQuery):
    invoice_id = call.data.split("|")[1]
    await cryptopay.delete_invoice(invoice_id=invoice_id)
    await call.message.delete()
    await call.message.answer("Оплата успешно отменена!")