import os
import pyrogram
from pyrogram import Client, filters
from config import Config

directory = f"{Config.DOWNLOAD_DIR}/"
directorye = f"{Config.ENCODE_DIR}/"


@Client.on_message(filters.command('downloads'))
async def downloads_list(client, message):
    say = 0
    dsy = ""
    if 1 == 1:
        if not os.listdir(directory):
            await message.reply("İndirilenler klasörünüz boş")
        else:
            for files in os.listdir(directory):
                say = say + 1
                dsy = dsy + "	" + str(say) + "-) " + files + '\n'
            await message.reply_text(
                "İndirilenler Listesi" + "\n\n" + dsy + "\n" + str(
                    say) + " Bu Kadar İndirilen Dosyan Var.")


@Client.on_message(filters.command('encodes'))
async def encodes_list(client, message):
    say = 0
    dsy = ""
    if 1 == 1:
        if not os.listdir(directory):
            await message.reply("Encode klasörünüz boş")
        else:
            for files in os.listdir(directorye):
                say = say + 1
                dsy = dsy + "	" + str(say) + "-) " + files + '\n'
            await message.reply_text(
                "İndirilenler Listesi" + "\n\n" + dsy + "\n" + str(
                    say) + " Bu Kadar Encode Dosyan Var.")
