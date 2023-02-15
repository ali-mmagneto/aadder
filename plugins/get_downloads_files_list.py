import os
import pyrogram
from pyrogram import Client, filters
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from helper_func.mux import sesekle_vid
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
import time
import logging 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

directory = f"{Config.DOWNLOAD_DIR}/"
directorye = f"{Config.ENCODE_DIR}/"


@Client.on_message(filters.command('downloads'))
async def downloads_list(bot, message):
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
            await message.reply("İstediğin Dosyayı Seç: ", reply_markup=ForceReply(True))

@Client.on_message(filters.reply)
async def api_connect(bot, message):
    if message.reply_to_message.reply_markup and isinstance(message.reply_to_message.reply_markup, ForceReply):
        sent_msg = await message.reply_text("**✓ İşlem Başlatılıyor..**", reply_to_message_id=message.id)
        try:
            choose = int(message.text)
            say = 0
            for files in os.listdir(directory):
                say = say + 1
                if choose == say:
                    video = (directory + files)
            start_time = time.time()
            chat_id = str(message.chat.id)
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
                        caption = final_filename  + '.@disneyplustur' + '.mp4'
                        )
                text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
                await sent_msg.edit(text)
                await bot.copy_message(
                    chat_id=message.chat.id, 
                    from_chat_id=Config.PRE_LOG, 
                    message_id=copy.id)
            else:
                copy = await bot.send_video(
                        chat_id = message.chat.id, 
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
        except Exception as f:
            LOGGER.info(f)
            await message.reply_text(f"**Error :** {f}", reply_to_message_id=message.id)

@Client.on_message(filters.command('encodes'))
async def encodes_list(bot, message):
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
            await message.reply("İstediğin Dosyayı Seç: ", reply_markup=ForceReply(True))


@Client.on_message(filters.reply)
async def api_connect(bot, message):
    if message.reply_to_message.reply_markup and isinstance(message.reply_to_message.reply_markup, ForceReply):
        sent_msg = await message.reply_text("**✓ İşlem Başlatılıyor..**", reply_to_message_id=message.id)
        try:
            choose = int(message.text)
            say = 0
            for files in os.listdir(directorye):
                say = say + 1
                if choose == say:
                    video = (directorye + files)
            start_time = time.time()
            chat_id = str(message.chat.id)
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
                        caption = final_filename  + '.@disneyplustur' + '.mp4'
                        )
                text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
                await sent_msg.edit(text)
                await bot.copy_message(
                    chat_id=message.chat.id, 
                    from_chat_id=Config.PRE_LOG, 
                    message_id=copy.id)
            else:
                copy = await bot.send_video(
                        chat_id = message.chat.id, 
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
        except Exception as f:
            LOGGER.info(f)
            await message.reply_text(f"**Error :** {f}", reply_to_message_id=message.id)
