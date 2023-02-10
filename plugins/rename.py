import pyrogram
from pyrogram import Client, filters
import os
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from config import Config
import time

@Client.on_message(filters.command('rename'))
async def rename(bot, message):
    text = message.text.split(" ", 1)
    file_name = text[1]
    caption = f"`{file_name}`"
    video = f"downloads/{file_name}"
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı`")
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"{file_name}")
    splitpath = media.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, video)
    start_time = time.time()
    duration = get_duration(video)
    thumb_image_path = os.path.join(
        Config.DOWNLOAD_DIR,
        chat_id,
        chat_id + ".jpg"
    )
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    else:
        thumb = get_thumbnail(file_path, './' + Config.DOWNLOAD_DIR, duration / 4)
    width, height = get_width_height(video)
    file_size = os.stat(video).st_size
    await bot.send_video(
        chat_id = message.chat.id,
        progress = progress_bar, 
        progress_args = (
            'Dosyan Yükleniyor!',
            msg,
            start_time
            ),
        video = video,
        caption = caption,
        duration = duration,
        thumb = thumb,
        width = width,
        height = height,
        supports_streaming=True)
