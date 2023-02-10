import os
import pyrogram
from pyrogram import Client, filters
from config import Config

directory = f"{Config.DOWNLOAD_DIR}/"

@Client.on_message(filters.command('downloads'))
async def downloads_list(client, message):
    say = 0
    dsy = ""
    if 1 == 1:
        if not os.listdir(directory):
            await message.reply("Combo klasörünüz boş")
        else:
            for files in os.listdir(directory):
                say = say + 1
                dsy = dsy + "	" + str(say) + "-) " + files + '\n'
            await message.reply_text(
                "İndirilenler Listesi" + "\n\n" + dsy + "\n" + str(
                    say) + " Bu Kadar İndirilen Dosyan Var.")
