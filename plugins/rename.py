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
    start_time = time.time()
    video = f"downloads/{file_name}"
    chat_id = str(message.from_user.id)
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"{file_name}",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    splitpath = media.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, video)
    if message.reply_to_message.video:
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
            thumb = get_thumbnail(video, './' + Config.DOWNLOAD_DIR, duration / 4)
        width, height = get_width_height(video)
        file_size = os.stat(video).st_size
        await msg.edit("`Yükleniyor..`") 
        file_size = os.stat(video).st_size
        if file_size > 2093796556:
            await Config.userbot.send_video(
                chat_id = Config.PRE_LOG,
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
            await msg.edit("`Başarı ile Tamamlandı...`")
        else:
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
            await msg.edit("`Başarı ile Tamamlandı...`")
    elif message.reply_to_message.photo:
        start_time = time.time()
        await msg.edit("`Yükleniyor..`") 
        await bot.send_photo(
            chat_id = message.chat.id,
            progress = progress_bar, 
            progress_args = (
                'Dosyan Yükleniyor!',
                msg,
                start_time
                ),
            photo = video,
            caption = caption) 
        await msg.edit("`Başarıyla Tamamlandı`")
        
