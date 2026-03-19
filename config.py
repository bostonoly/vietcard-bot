import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberStatus
from aiogram.filters import CommandStart
from config import BOT_TOKEN, CHANNEL_ID, MANAGER_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CHANNEL_LINK = "https://t.me/amazingviet"

def subscribe_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Чтобы получить консультацию по карте Visa во Вьетнаме, "
        "подпишись на наш канал — там все актуальные условия и новости.",
        reply_markup=subscribe_keyboard()
    )

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            await callback.message.edit_text(
                "✅ Отлично! Ожидайте — менеджер свяжется с вами в ближайшее время."
            )
            user = callback.from_user
            name = user.full_name
            username = f"@{user.username}" if user.username else "без username"
            profile_link = f"tg://user?id={user_id}"
            await bot.send_message(
                chat_id=MANAGER_ID,
                text=(
                    f"🔔 Новый клиент подписался!\n\n"
                    f"👤 Имя: {name}\n"
                    f"📎 Username: {username}\n"
                    f"🔗 Профиль: {profile_link}"
                )
            )
        else:
            await callback.answer(
                "❌ Подписка не найдена. Подпишись на канал и попробуй снова.",
                show_alert=True
            )
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        await callback.answer("Произошла ошибка. Попробуй позже.", show_alert=True)

async def main():
    print("Started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
