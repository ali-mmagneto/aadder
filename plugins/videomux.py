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
from config import Config
import time
import re
import asyncio


progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    if not items:
        return None
    return items

async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))

async def read_stderr(start, mes, process):
    async for line in readlines(process.stderr):
            line = line.decode('utf-8')
            progress = parse_progress(line)
            if progress:
                #Progress bar logic
                now = time.time()
                diff = start-now
                text = 'İLERLEME\n'
                text += 'Boyut : {}\n'.format(progress['size'])
                text += 'Süre : {}\n'.format(progress['time'])
                text += 'Hız : {}\n'.format(progress['speed'])

                if round(diff % 5)==0:
                    try:
                        await mes.edit(text=text)
                    except Exception as e:
                        print(e)

async def videobirlestirici(mes, video1, video2):
    start = time.time()
    output = "birlestirilmisVideo.mp4"
    out_location = f"downloads/{output}"
    command = [
            'ffmpeg','-hide_banner',
            '-i',video1,
            '-i',video2,
            '-c:a','copy',
            '-y',out_location
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    await asyncio.wait([
            read_stderr(start,mes, process),
            process.wait(),
        ])
    
    if process.returncode == 0:
        await mes.edit('Ses Ekleme Başarı İle Tamamlandı!\n\nGeçen Süre : {} saniye'.format(round(start-time.time())))
    else:
        await mes.edit('Ses Eklenirken Bir Hata Oluştu!')
        return False
    time.sleep(2)
    return output

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
    directory = "downloads/" 
    chat_id = message.chat.id
    video1 = "downloads/video1.mp4"
    video2 = "downloads/video2.mp4" 
    video1temp = "video1.mp4" 
    video2temp = "video2.mp4" 
    text = ""
    if not video1temp in os.listdir(directory):
        text += 'Birinci Videoyu Yolla\n'
        await message.reply_text(text)
        return
    if not video2temp in os.listdir(directory):
        text += 'İkinci Videoyu Yolla'
        await message.reply_text(text)
        return
    mes = await bot.send_message(message.chat.id, "`Videolar Birleştiriliyor..`")
    birlesiktemp = await videobirlestirici(mes, video1, video2)
    video = os.path.join(Config.DOWNLOAD_DIR, birlesiktemp)
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
    if file_size > 2093796556:
        get_chat = await bot.get_chat(chat_id=Config.PRE_LOG)
        print(get_chat)
        await bot.send_message(Config.PRE_LOG, "2 gb üstüVideo Geliyor.")
        copy = await Config.userbot.send_video(
                chat_id = Config.PRE_LOG, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ),
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                video = video,
                caption = final_filename
                )
        text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
        await bot.copy_message(
            chat_id=chat_id, 
            from_chat_id=Config.PRE_LOG, 
            message_id=copy.id)
    else:
        copy = await bot.send_video(
                chat_id = chat_id, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ),
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                video = video,
                caption = final_filename + '.@disneyplustur' + '.mp4'
                )
        text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
