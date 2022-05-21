import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .commands import start, BATCH
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """Hello! , 👋

❓ Help Menu

★ Just send me the files, I will store file and give you share able link. Your files will totally safe here.

👨‍💻 Commands

• /start : for start the bot.
• /mode : You Can Enable or Disable Uploader Details in Caption.
  /mode channel_id : for channels.
• /batch : You Can Store Multiple files in one link.
• /me : Your Info.


💠 Features ❕

1. Support Channels : just make me admin with edit permission, I'll add url & share button In media posts.

2. You can delete your file while saving files in private. 🗑

📍Check Complete Details Here 👇🏻"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Details📝', url=f"http://telegra.ph/TG-File-Store-Bot-07-10")
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""Hi! Ashu, 👋

🤖 I'm a Telegram File Store Bot v2 written in python with Pyrogram Framework. 
    
🧑‍💻 This Bot Is Made By [Srujan](https://t.me/Sruja_12) & Thanks to [Anoymous_Ns](https://t.me/Anonymous_Ns) for their code. ❤

📍Note : Please don't send adults files, don't block the bot & don't spam.

👥 Contact My Boss : [Here](https://t.me/Sruja_12) for any help etc. 

📖 My Details : [Click Here](http://telegra.ph/TG-File-Store-Bot-07-10)

|> Thank You :)

-
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Help 💡', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("Deleted files successfully 👨‍✈️")
