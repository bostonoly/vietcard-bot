import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, CHANNEL_ID, MANAGER_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def check_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Я подписался",
            callback_data="check_sub"
        )]
    ])

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Мы поможем тебе оформить карту Visa во Вьетнаме 🇻🇳\n\n"
        "Чтобы связаться с менеджером — подпишись на наш канал:\n"
        "👉 https://t.me/amazingviet\n\n"
        "После подписки нажми кнопку ниже 👇",
        reply_markup=check_button()
    )

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )
        status = member.status
    except Exception:
        status = "left"

    if status in ("member", "administrator", "creator"):
        # Сообщение пользователю
        await callback.message.edit_text(
            "✅ Отлично, подписка подтверждена!\n\n"
            "Ожидайте — менеджер свяжется с вами в ближайшее время 🙌"
        )
        # Уведомление менеджеру
        name = callback.from_user.first_name or "Без имени"
        username = f"@{callback.from_user.username}" if callback.from_user.username else "нет username"
        uid = callback.from_user.id
        await bot.send_message(
            chat_id=MANAGER_ID,
            text=(
                f"🔔 Новый клиент!\n\n"
                f"Имя: {name}\n"
                f"Username: {username}\n\n"
                f"Написать: tg://user?id={uid}"
            )
        )
    else:
        await callback.answer(
            "❌ Подписка не найдена.\n"
            "Подпишись на канал и нажми кнопку снова.",
            show_alert=True
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

**requirements.txt**
```
aiogram==3.7.0
