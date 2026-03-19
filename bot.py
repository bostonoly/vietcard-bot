import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus
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
        "подпишись на наш канал — там все актуальные условия и новости. Далее с тобой свяжется менеджер",
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
            username = f"@{user.use
