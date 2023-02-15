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
import random

@Client.on_message(filters.command('video1'))
async def video1al(bot, message):
    rand = random.randint(10, 900) 
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    start_time = time.time()
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"downloads/video1.mp4",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    old_file_name = f"downloads/video1.mp4"
    await message.reply_video(old_file_name)

@Client.on_message(filters.command('video2'))
async def video2al(bot, message):
    rand = random.randint(10, 900) 
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    start_time = time.time()
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"downloads/video2.mp4",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    old_file_name = f"downloads/video2.mp4"
    await message.reply_video(old_file_name)

@Client.on_message(filters.command('birlestir'))
async def videobirlestir(bot, message):
    video1 = "downloads/video1.mp4"
    video2 = "downloads/video2.mp4" 
    text = ""
    if not video1:
        text += 'Birinci Videoyu Yolla\n'
    if not video2:
        text += 'İkinci Videoyu Yolla'
    await message.reply_text(text)

