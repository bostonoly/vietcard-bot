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
        [InlineKeyboardButton(text="\u041f\u043e\u0434\u043f\u0438\u0441\u0430\u0442\u044c\u0441\u044f \u0438 \u0443\u0437\u043d\u0430\u0442\u044c \u043f\u0440\u043e \u043a\u0430\u0440\u0442\u0443", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="\u042f \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043b\u0441\u044f", callback_data="check_sub")]
    ])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c! "
        "\u0427\u0442\u043e\u0431\u044b \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043a\u043e\u043d\u0441\u0443\u043b\u044c\u0442\u0430\u0446\u0438\u044e "
        "\u043f\u043e \u043a\u0430\u0440\u0442\u0435 Visa \u0432\u043e \u0412\u044c\u0435\u0442\u043d\u0430\u043c\u0435, "
        "\u043f\u043e\u0434\u043f\u0438\u0448\u0438\u0441\u044c \u043d\u0430 \u043d\u0430\u0448 \u043a\u0430\u043d\u0430\u043b."
    )
    await message.answer(text, reply_markup=subscribe_keyboard())

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            ok_text = "\u041e\u0442\u043b\u0438\u0447\u043d\u043e! \u041e\u0436\u0438\u0434\u0430\u0439\u0442\u0435 \u2014 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u0441\u0432\u044f\u0436\u0435\u0442\u0441\u044f \u0441 \u0432\u0430\u043c\u0438 \u0432 \u0431\u043b\u0438\u0436\u0430\u0439\u0448\u0435\u0435 \u0432\u0440\u0435\u043c\u044f."
            await callback.message.edit_text(ok_text)
            user = callback.from_user
            name = user.full_name
            if user.username:
                uname = "@" + user.username
            else:
                uname = "\u0431\u0435\u0437 username"
            link = "tg://user?id=" + str(user_id)
            line1 = "\U0001f514 \u041d\u043e\u0432\u044b\u0439 \u043a\u043b\u0438\u0435\u043d\u0442 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043b\u0441\u044f!\n\n"
            line2 = "\U0001f464 \u0418\u043c\u044f: " + name + "\n"
            line3 = "\U0001f4ce Username: " + uname + "\n"
            line4 = "\U0001f517 \u041f\u0440\u043e\u0444\u0438\u043b\u044c: " + link
            await bot.send_message(chat_id=MANAGER_ID, text=line1 + line2 + line3 + line4)
        else:
            err_text = "\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430. \u041f\u043e\u0434\u043f\u0438\u0448\u0438\u0441\u044c \u043d\u0430 \u043a\u0430\u043d\u0430\u043b \u0438 \u043f\u043e\u043f\u0440\u043e\u0431\u0443\u0439 \u0441\u043d\u043e\u0432\u0430."
            await callback.answer(err_text, show_alert=True)
    except Exception as e:
        logging.error(str(e))
        err2 = "\u041f\u0440\u043e\u0438\u0437\u043e\u0448\u043b\u0430 \u043e\u0448\u0438\u0431\u043a\u0430. \u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439 \u043f\u043e\u0437\u0436\u0435."
        await callback.answer(err2, show_alert=True)

async def main():
    print("Started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
