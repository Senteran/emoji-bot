import sys

from discord import channel
from discord.activity import Game
# prevent __pycache__ folder from being created
sys.dont_write_bytecode = True

import time
import discord
import random
from discord.utils import get
from os import remove
from modules.dictionaries import *
from modules.functions import *
from google_images_search import GoogleImagesSearch
import asyncio
import youtube_dl
import shutil
import io


def to_en_str(pl_str):
    # Przechowuje polskie znaki oraz ich odpowiedniki aby móc je zamienić (Nie jestem pewny co do 'ó' może by to zmienić na 'o' zamiast?)
    polish_symbols = {
        'ą': 'a',
        'ć': 'c',
        'ę': 'e',
        'ó': 'o',
        'ż': 'z',
        'ź': 'z',
        'ł': 'l',
        'ś': 's',
        'ń': 'n'
    }
    
    # Stworzenie pustego en_str który bęzdie przechowywał string bez polskich znaków
    en_str = ""
    # Przechowuje czy znak został dodany jako przemieniony
    char_added = False

    # Celem tego całego bloku jest przejście przez każdy znak w message.content i zamienienie polskich znaków takich jak 'ą' i 'ć' na ich odpowiedniki, czyli w tym przypadku 'a' i 'c'
    # Jest to przydatne inaczej trzeba sprawdzać dwie opcje wiadomości na przykład 'zły' i 'zly', po zamianie natomiast trzeba sprawdzać tylko 'zly'
    # Iteruje przez każdy znak z pl_str
    for char in pl_str:
        # Iteruje przez każdy znak w dzienniku polskie_znaki
        for symbol in polish_symbols:
            # Jeżeli aktualny znak z dzienniku jest równy char z contentu wiadomości to go zamieniamy
            if symbol == char:
                en_str = en_str + polish_symbols[symbol]
                # Skoro został dodany znak to znak_dodany = True, aby na przykład nie zmienić 'ą' na 'a' i potem też dodać 'ą'
                char_added = True
        # Jeżeli char z contentu nie został znaleziony w dzienniku to normalny znak zostaje dodany do content
        if not char_added:
            en_str = en_str + char
        # Na końcu trzeba powrócić znak_dodany do False aby w następnej iteracji głównego for wszystko działało poprawnie
        char_added = False
    
    return en_str


async def yt_download(url, destination):
    global youtube_dl
    youtube_dl.utils.bug_reports_message = lambda: ''

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' 
    }
    ffmpeg_options = {
        'options': '-vn'
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                data = data['entries'][0]
            filename = data['title'] if stream else ytdl.prepare_filename(data)
            shutil.move(filename, 'songs')
            filename = destination + filename
            return filename
    
    ret = await YTDLSource.from_url(url, loop=True)
    return ret

async def word_triangle(message):
    string = ""
    prev = ""

    for char in message:
        prev += char
        if not char == ' ':
            string = string + "\n" + prev
    for char in message[:0:-1]:
        prev = prev.removesuffix(char)
        if not char == ' ':
            string = string + "\n" + prev
    return seperate_into_2000_words(string)

async def seperate_into_2000_words(message):
    count = 0
    ret = []
    last_enter = 0
    last_append = 0
    string = ""
    for i in range(0, len(message)):
        if count == 1999:
            string = string.removesuffix(message[i:last_enter-2:-1])
            ret.append(string)
            string = ""
            last_append = i
            i = last_enter
            count = 0
        else:
            if message[i] == '\n':
                last_enter = i+1
            string += message[i]
            count += 1
    ret.append(message[last_append:len(message)])
    return ret

def Initilise_Variables():
    global banned_ids
    global beast_banned_ids
    global prefix
    global suffix

    file = open('data/prefix.txt', 'r')
    prefix = file.read()
    file.close()
    file = open('data/suffix.txt', 'r')
    suffix = file.read()
    file.close()
    file = open('data/banned_ids.txt', 'r')
    with open('data/banned_ids.txt') as f:
        banned_ids = [line.rstrip() for line in f]
    with open('data/beast_banned_ids.txt') as f:
        beast_banned_ids = [line.rstrip() for line in f]

async def delete_message(message):
    await message.delete()

async def send_message(message, content):
    await message.channel.send(content)

def process_content(content):
    string = content.lower()
    return to_en_str(string)

async def default_reactions(message, content):
    for element in emoji_library:
        if element in content:
            try:
                await message.add_reaction(emoji_library[element])
                reaction()
            except discord.errors.Forbidden:
                pass

async def custom_reactions(message, client, content):
    for element in custom_emoji_library:
        if element in content:
            try:
                emoji = get(client.emojis, name=custom_emoji_library[element])
                await message.add_reaction(emoji)
                reaction()
            except discord.errors.Forbidden:
                pass

def reaction():
    file = open('data/reactions.txt', 'r')
    reactions = int(file.read())
    reactions = reactions + 1
    file.close()
    file = open('data/reactions.txt', 'w')
    file.write(str(reactions))
    file.close()

async def play_default_music(message, content):
    for element in music_library:
        if element in content:
            channel = message.author.voice.channel
            try:
                channel.connect()
            except AttributeError:
                message.channel.send("Musisz być połączony do kanału!")
            filename = 'src/' + music_library[element]
            server = message.guild
            voice_client = server.voice_client
            voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
            await message.channel.send('Currently playing: ' + music_library[element])

async def change_prefix(message):
    if message.content.startswith('nowy prefix '):
            new_prefix = message.content.removeprefix('nowy prefix')
    else:
        new_prefix = message.content.removeprefix('nowy prefiks ')
    encoded_prefix = new_prefix.encode('utf-8')
    file = open('data/prefix.txt', 'wb')
    file.write(encoded_prefix)
    file.close()
    global prefix
    file = open('data/suffix.txt', 'r')
    suf = file.read()
    file.close()
    prefix = new_prefix
    if len(prefix + suf) >= 30:
        await message.guild.me.edit(nick=prefix[0 : min(len(prefix), 30)]+suf[0 : 30 - len(prefix)])
    else:
        await message.guild.me.edit(nick=prefix+suf)
    
async def display_prefix(message):
    await message.channel.send('Aktualny prefiks to: ' + prefix)

# Dodaje ścieżkę danej piosenki do pliko data/song.txt
def write_song_filename(filename):
    file = open('data/song.txt', 'w')
    file.write(filename)
    file.close()

# Usuwa piosenke aktualnie zapisaną w pliku data/song.txt
def remove_song():
    file = open('data/song.txt', 'r')
    filename = file.read()
    file.close()
    if not (filename == ''):
        remove(filename)
        file = open('data/song.txt', 'w')
        file.write('')
        file.close()

async def change_suffix(message):
        if message.content.startswith('nowy sufiks '):
            new_suffix = message.content.removeprefix('nowy sufiks ')
        else:
            new_suffix = message.content.removeprefix('nowy suffix ')
        encoded_suffix = new_suffix.encode('utf-8')
        file = open('data/suffix.txt', 'wb')
        file.write(encoded_suffix)
        file.close()
        global suffix
        suffix = new_suffix
        if len(prefix + suffix) >= 30:
            await message.guild.me.edit(nick=prefix + suffix[0 : 29 - len(prefix)])
        else:
            await message.guild.me.edit(nick=prefix+suffix)

async def display_suffix(message):
    message.channel.send('Aktualny sufiks to: ' + suffix)

async def play_music(message):
    server = message.guild
    voice_client = server.voice_client

    text = message.content
    url = text.removeprefix('emoji zagraj')
    filename = await yt_download(url, 'songs/')
    try:
        voice_client.stop()
    except AttributeError:
        channel = message.author.voice.channel
        await channel.connect()
        voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
    await message.channel.send('**Now playing:** {}'.format(filename.removeprefix('songs/')))
        
    # remove_song jest dopiero tu, ponieważ musi się stać po voice_client.stop() aby nie próbować usunąć pliku w użyciu oraz ponieważ jak było tuż po nim to czasami nie działało
    # sensowną opcją jest więc danie go tu ponieważ jest po await send czyli minie chwila i plik powinien mieć wystarczająco czasu aby przestać być zablokowanym
    remove_song()
    write_song_filename(filename)

async def send_messages(content, message):
    for element in send_library:
        if element in content:
            await message.channel.send(send_library[element])

async def send_word_triangle(message, content):
    string = word_triangle(message.content.removeprefix("trójkąt "))
    try:
        for element in string:
            await message.author.send(element)
    except discord.errors.HTTPException:
        await message.channel.send("Ta wiadomość byłaby za długa :(")

async def search_for_image(message, client, gis):
    print('zdjęcie...')
    query = message.content.removeprefix('emoji zdjęcie ')
    image_search_params['q'] = query
    gis.search(search_params=image_search_params, custom_image_name='img')
    for image in gis.results():
        image.download('pictures/')
    try:
        file = open('pictures/img.jpg', 'rb')
        path = 'pictures/img.jpg'
    except FileNotFoundError:
        try:
            file = open('pictures/img.png', 'rb')
            path = 'pictures/img.png'
        except FileNotFoundError:
            try:
                file = open('pictures/img.gif', 'rb')
                path = 'pictures/img.gif'
            except FileNotFoundError:
                await message.channel.send('Image not found')
                return
    avatar = file.read()
    file.close()
    await client.user.edit(avatar=avatar)
    time.sleep(1)
    remove(path)

async def change_to_attached_image(message, client):
    return
    for file in message.attachments:
        fp = io.BytesIO()
        await file.save(fp)
        pfp = discord.File(fp, filename=file.filename)
        # f = open('/pictures/' + file.filename, 'w+')
        # f.write(pfp)
        # f.close()
        await client.user.edit(avatar=pfp)


async def display_reactions(message):
    file = open('data/reactions.txt', 'r')
    reactions = file.read()
    await message.reply('Już zareagowałem: ' + reactions + ' razy!')

async def join_voice_channel(message):
    channel = message.author.voice.channel
    await channel.connect()

async def leave_voice_channel(message):
    await message.add_reaction('👋')
    await message.guild.voice_client.disconnect()

async def pause_music(message):
    await message.add_reaction('⏸')
    message.guild.voice_client.pause()

async def stop_music(message):
    await message.add_reaction('🛑')
    message.guild.voice_client.stop()

async def resume_music(message):
    await message.add_reaction('⏯')
    message.guild.voice_client.resume()

async def manual_response(message):
    response = input('Input the response to ' + message.content + ': ')
    await message.reply(response)

async def i_am_the_cum_beast(message, client):
    file = open('pictures/cum_beast.jpg', 'rb')
    pfp = file.read()
    file.close()
    await client.user.edit(avatar=pfp)
    await message.guild.me.edit(nick='The cum beast')
    await message.channel.send('I am the cum beast')

async def emojimeister_return(message, client):
    file = open('pictures/emoji_fp.png', 'rb')
    pfp = file.read()
    file.close()
    await client.user.edit(avatar=pfp)
    await message.guild.me.edit(nick=prefix[0 : min(len(prefix), 29)] + suffix[0 : 29 - len(prefix)])

async def custom_reaction(message, client, emoji_name):
    emoji = get(client.emojis, name=emoji_name)
    await message.add_reaction(emoji)

async def beast_mode_on(client):
    global beast_mode
    beast_mode = True
    await client.change_presence(activity=discord.Game('Cum Beast Mode'))

async def beast_mode_off(client):
    global beast_mode
    beast_mode = False
    client.change_presence(status=None)

async def reply_to_message(message, content):
    await message.reply(content)
    return
