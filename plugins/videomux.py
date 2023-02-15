# Coded by :d
import pyrogram
from pyrogram import Client, filters
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from config import Config
import time

@Client.on_message(filters.command('video1'))
async def rename(bot, message):
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"downloads/video1.mp4",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    old_file_name =f"downloads/video1"
    await message.reply_video("downloads/video1")
