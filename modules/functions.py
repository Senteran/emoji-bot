"""This module houses most of the functions of the bot"""
import sys
import time
import random
from os import remove
import shutil
import datetime
import asyncio
from io import BytesIO
from PIL import Image

import discord
from discord.utils import get
import youtube_dl as YOUTUBE_DL

from dictionaries import sending_hours, emoji_library, custom_emoji_library, send_library,\
    music_library, krupier_users, inverse_krupier_users, krupier_ids, krupier_users_list,\
    NAMES_J, NAMES_M, NAMES_P, NAMES_S, NAMES_K, NAMES_A, NAMES_KZ, NAMES_AZ, NAZWISKA_B,\
    NAZWISKA_K, NAZWISKA_P, NAZWISKA_R, NAZWISKA_T, NAZWISKA_W, NAZWISKA_Z,\
    nick_to_name_beginning_dictionary, nick_to_surname_dictionary, names_today,\
    names_to_nick, image_search_params, names_to_custom_nick
from file_handler import get_value, store_value

# prevent __pycache__ folder from being created
sys.dont_write_bytecode = True

USE_NEW_NAME_FILES = True
ASSIGNED_NICKNAMES = False
SHOULD_EMOJI_BOT_CHANGE_NICKNAMES = False
SEND_NICKNAMES_TO_USER = False

BEAST_MODE = False

def to_en_str(pl_str):
    """Usuwa polskie znaki z tekstu

    Args:
        pl_str (string): tekst z polskimi znakami

    Returns:
        string: tekst z zamienionymi polskimi znakami
    """
    # Przechowuje polskie znaki oraz ich odpowiedniki aby móc je zamienić
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

    en_str = ""
    char_added = False

    for char in pl_str:
        for symbol in polish_symbols:
            if symbol == char:
                en_str = en_str + polish_symbols[symbol]
                char_added = True
        if not char_added:
            en_str = en_str + char
        char_added = False

    return en_str


async def yt_download(url, destination):
    """Pobiera film z YouTube

    Args:
        url (string): adres filmiku na YouTube
        destination (string): folder do którego filmik zostanie pobrany
    """
    global YOUTUBE_DL
    YOUTUBE_DL.utils.bug_reports_message = lambda: ''

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

    ytdl = YOUTUBE_DL.YoutubeDL(ytdl_format_options)

    class YTDLSource(discord.PCMVolumeTransformer):
        """Wewnętrzna klasa dla obiektu do pobierania z YouTube"""
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            """Pobiera z url. DO WEWNĘTRZNEGO UŻYTKU

            Args:
                url (string): adres
                loop (bool, optional): Ustala czy będzie pętla. Defaults to None.
                stream (bool, optional): Ustawia czy będzie pobierany czy streamowany film.\
                     Defaults to False.
            """
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor\
                (None, lambda: ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                data = data['entries'][0]
            filename = data['title'] if stream else ytdl.prepare_filename(data)
            try:
                shutil.move(filename, 'songs')
            except shutil.Error:
                remove_song()
                shutil.move(filename, 'songs')
            filename = destination + filename
            return filename

    ret = await YTDLSource.from_url(url, loop=True)
    return ret

def word_triangle(message):
    """Zamienia długi string na pomniejsze stringi do trójkątu

    Args:
        message (message): Otrzymana wiadomość

    Returns:
        array[string]: zawiera części trójkątu
    """
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

def seperate_into_2000_words(message):
    """Zamienia długi string na pojedyncze o długości 2000 liter

    Args:
        message (message): Discord.message

    Returns:
        array[string]: zawiera pojedyncze człony wiadomości
    """
    count = 0
    ret = []
    last_enter = 0
    last_append = 0
    string = ""
    for i, value in enumerate(message):
        if count == 1999:
            string = string.removesuffix(message[i:last_enter-2:-1])
            ret.append(string)
            string = ""
            last_append = i
            i = last_enter
            count = 0
        else:
            if value == '\n':
                last_enter = i+1
            string += value
            count += 1

    ret.append(message[last_append:len(message)])
    return ret

async def delete_message(message):
    """Usuwa wiadomość

    Args:
        message (message): Wiadomość
    """
    await message.delete()

async def send_message(message, content):
    """Wysyła wiadomość po otrzymaniu jakiejś

    Args:
        message (message): Wiadomość otrzymana
        content (string): Treść wiadomości do wysłania
    """
    await message.channel.send(content)

def process_content(content):
    """Processes a string for use

    Args:
        content (string): A string with uppercase and polish characters

    Returns:
        string: text in lower case without polish characters
    """
    string = content.lower()
    return to_en_str(string)

async def default_reactions(message, content):
    """Adds reactions with normal emojis

    Args:
        message (message): The message to react to
        content (string): The message's content
    """
    for element in emoji_library:
        if element in content:
            try:
                await message.add_reaction(emoji_library[element])
                reaction()
            except discord.errors.Forbidden:
                pass

async def custom_reactions(message, client, content):
    """Adds reactions with custom emojis

    Args:
        message (message): The message to react to
        client (discord.client): The bot's login session
        content (string): The message's content
    """
    for element in custom_emoji_library:
        if element in content:
            try:
                emoji = get(client.emojis, name=custom_emoji_library[element])
                await message.add_reaction(emoji)
                reaction()
            except discord.errors.Forbidden:
                pass

def reaction():
    """Adds 1 to the reaction counter in data/reactions.txt
    """
    reactions = int(get_value('reactions'))
    reactions = reactions + 1
    store_value('reactions', str(reactions))

async def play_default_music(message, content):
    """Plays music from the built-in library

    Args:
        message (message): The received message
        content (string): The message's content
    """
    for element in music_library:
        if element in content:
            filename = 'src/' + music_library[element]
            server = message.guild
            voice_client = server.voice_client
            voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
            await message.channel.send('Currently playing: ' + music_library[element])

def write_song_filename(filename):
    """Pisze ścieżke aktualnie granej piosenki do data/song.txt

    Args:
        filename (string): Ścieżka do piosenki
    """
    store_value('song', filename)

def remove_song():
    """Usuwa ostatnio pobraną piosenkę. Bierze ścieżke z data/song.txt
    """
    filename = get_value('song')
    if not filename == '':
        try:
            remove(filename)
        except FileNotFoundError:
            print("The file was not found")
        store_value('song', '')


async def change_nick(message, client):
    nickname = message.content.removeprefix('emoji nick ')
    await client.get_guild(message.guild.id).me.edit(nick=nickname)

async def play_music(message):
    """Gra muzykę pobierając ją z YouTube

    Args:
        message (message): Otrzymana wiadomość
    """
    server = message.guild

    text = message.content
    url = text.removeprefix('emoji zagraj')
    filename = await yt_download(url, 'songs/')
    chan = message.author.voice.channel
    try:
        await chan.connect()
    except discord.errors.ClientException:
        pass
    voice_client = server.voice_client
    voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
    await message.channel.send('**Now playing:** {}'.format(filename.removeprefix('songs/')))

    remove_song()
    write_song_filename(filename)

async def send_messages(content, message):
    """Wysyła odpowiedzi na wiadomości z wbudowanej biblioteki

    Args:
        content (string): Treść wiadomości
        message (message): Otrzymana wiadomość
    """
    for element in send_library:
        if element in content:
            await message.channel.send(send_library[element])

async def send_word_triangle(message):
    """Wysyła trójkąt autorowi wiadomości

    Args:
        message (message): Otrzymana wiadomość
    """
    string = word_triangle(message.content.removeprefix("trójkąt "))
    try:
        for element in string:
            await message.author.send(element)
    except discord.errors.HTTPException:
        await message.channel.send("Ta wiadomość byłaby za długa :(")

async def search_for_image(message, client, gis):
    """Wyszukuje zdjęcie na Google Images i ustawia je jako zdjęcie profilowe bota

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja discorda bota
        gis (???): Nie wiem co to jest
    """
    print('zdjęcie...')
    query = message.content.removeprefix('emoji zdjęcie ')
    image_search_params['q'] = query
    gis.search(search_params=image_search_params)

    my_bytes_io = BytesIO()

    for image in gis.results():
        # here we tell the BytesIO object to go back to address 0
        my_bytes_io.seek(0)

        # take raw image data
        raw_image_data = image.get_raw_data()

        # this function writes the raw image data to the object
        image.copy_to(my_bytes_io, raw_image_data)

        # we go back to address 0 again so PIL can read it from start to finish
        my_bytes_io.seek(0)

        # create a temporary image object
        temp_img = Image.open(my_bytes_io)

        converted_img = temp_img.convert("RGB")
        converted_img.save('src/temp.jpg')
        file = open('src/temp.jpg', 'rb')
        pfp = file.read()

        await client.user.edit(avatar=pfp)
        file.close()
        await asyncio.sleep(1)
        remove('src/temp.jpg')
        
    
    # for image in gis.results():
    #     image.download('src/')
    # try:
    #     file = open('src/img.jpg', 'rb')
    #     path = 'src/img.jpg'
    # except FileNotFoundError:
    #     try:
    #         file = open('src/img.png', 'rb')
    #         path = 'src/img.png'
    #     except FileNotFoundError:
    #         try:
    #             file = open('src/img.gif', 'rb')
    #             path = 'src/img.gif'
    #         except FileNotFoundError:
    #             await message.channel.send('Image not found')
    #             return
    # avatar = file.read()
    # file.close()
    # await client.user.edit(avatar=avatar)
    # time.sleep(1)
    # remove(path)

async def attachment_profile_picture(message, client):
    atts = message.attachments
    if len(atts) == 0:
        message.reply('No attachments')
        return
    
    att = atts[0]
    bytes = await att.read()
    my_bytes_io = BytesIO(bytes)
    my_bytes_io.seek(0)

    temp_img = Image.open(my_bytes_io)

    converted_img = temp_img.convert("RGB")
    converted_img.save('src/temp.jpg')
    file = open('src/temp.jpg', 'rb')
    pfp = file.read()

    await client.user.edit(avatar=pfp)
    file.close()
    await asyncio.sleep(1)
    remove('src/temp.jpg')


async def display_reactions(message):
    """Pisze ile reakcji zostało już wykonanych

    Args:
        message (message): Otrzymana wiadomość
    """
    await message.reply('Już zareagowałem: ' + get_value('reactions') + ' razy!')

async def join_voice_channel(message, client):
    """Dołącza do kanału głosowego, w którym jest autor wiadomości

    Args:
        message (message): Otrzymana wiadomość
    """
    chan = message.author.voice.channel
    chan = client.get_channel(chan.id)
    try:
        await chan.connect()
    except discord.errors.ClientException:
        await message.guild.voice_client.disconnect()
        try:
            await chan.connect()
        except:
            await message.reply("Niestety nie udało mi się dołączyć 😢")

async def leave_voice_channel(message, current):
    """Opuszcza kanał głosowy

    Args:
        message (message): Otrzymana wiadomość
    """
    chan = current.get_channel(message.channel.id)
    mess = await chan.fetch_message(message.id)
    await mess.add_recation('👋')
    await current.get_guild(message.guild.id).voice_client.disconnect()

async def pause_music(message):
    """Pauzuje muzyke

    Args:
        message (message): Otrzymana wiadomość
    """
    await message.add_reaction('⏸')
    message.guild.voice_client.pause()

async def stop_music(message):
    """Zatrzymuje muzyke

    Args:
        message (message): Otrzymana wiadomość
    """
    await message.add_reaction('🛑')
    message.guild.voice_client.stop()

async def resume_music(message):
    """Wstrzymuje muzykę

    Args:
        message (message): Otrzymana wiadomość
    """
    await message.add_reaction('⏯')
    message.guild.voice_client.resume()

async def manual_response(message):
    """Manualna odpowiedź na pytanie

    Args:
        message (message): Otrzymana wiadomość
    """
    response = input('Input the response to ' + message.content + ': ')
    await message.reply(response)

async def emojimeister_return(message, client):
    """Przywraca domyślne zdjęcie i nick bota

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja discorda bota
    """
    file = open('src/emoji_fp.png', 'rb')
    pfp = file.read()
    file.close()
    await client.user.edit(avatar=pfp)
    await message.guild.me.edit(nick='emojimeister')

async def custom_reaction(message, client, emoji_name):
    """Reaguje reakcją krupierową

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja discorda bota
        emoji_name (string): Nazwa emoji do zareagowania
    """
    emoji = get(client.emojis, name=emoji_name)
    await message.add_reaction(emoji)

async def reply_to_message(message, content):
    """Odpowiada na wiadomość

    Args:
        message (message): Otrzymana wiadomość
        content (string): Treść odpowiedzi
    """
    await message.reply(content)

async def help_other_helps(message):
    """Wysyła listę innych komend pomocy

    Args:
        message (message): Otrzymana wiadomość
    """
    await send_message(message, '''
    - emoji commands - wyświetla komendy\n
    - emoji replies - wyświetla zapytania i odpowiedzi\n
    - emoji songs - wyświetle wbudowane piosenki do zagrania\n
    - emoji emoji - wyświetla zestaw domyślnych emoji\n
    - emoji emoji_krupier - wyświetla customowe reakcje emoji''')

async def help_commands(message):
    """Wysyła listę komend bota

    Args:
        message (message): Otrzymana wiadomość
    """
    await send_message(message, '''
    - emoji wejdz - wchodzi do kanału\n
    - emoji wyjdz - wychodzi z kanału\n
    - emoji zagraj {nazwa piosenki} - gra piosenkę z YouTube\n
    - emoji zdjęcie {nazwa zdjęcia} - szuka zdjęcia na Google Image i ustawia je jako profilowe\n
    - emoji nick {nick} - zmienia nick bota\n
    - ile reakcji? - wyświetla ilość reakcji wykonanych''')

async def help_replies(message):
    """Wysyła listę wbudowanych odpowiedzi

    Args:
        message (message): Otrzymana wiadomość
    """
    cont = ""
    for element in send_library:
        cont = cont + element + ' - ' + send_library[element] + '\n'
    await send_message(message, cont)

async def help_songs(message):
    """Wysyła listę wbudowanych piosenek

    Args:
        message (message): Otrzymana wiadomość
    """
    cont = ""
    for element in music_library:
        cont = cont + element + ' - ' + music_library[element] + '\n'
    await send_message(message, cont)

async def help_emoji(message):
    """Wysyła wiadomość z listą domyślnych reakcji

    Args:
        message (message): Otrzymana wiadomość
    """
    cont = ""
    for element in emoji_library:
        cont = cont + element + ' - ' + emoji_library[element] + '\n'
    await send_message(message, cont)

async def help_custom_emoji(message, client):
    """Wysyła wiadomość z piekła rodem  (!!!UWAGA NIE UŻYWAĆ BO KRUPIER SIĘ ZDENERWUJE)

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja discorda bota
    """
    for element in custom_emoji_library:
        emoji = get(client.emojis, name=custom_emoji_library[element])
        try:
            await send_message(message, element)
            await send_message(message, emoji)
        except discord.errors.HTTPException:
            try:
                print('Empty message caught in help_custom_emoji. Element: ' + element +
                 ' . Emoji: ' + emoji)
            except TypeError:
                print('The emoji could not be appended')

async def new_day(client):
    """Ustawia listę nicków, wysyła indywidualne i kanałowe wiadomości o nickach

    Args:
        client (client): Sesja discorda bota
    """
    i = 0
    names = []
    surnames = []
    for element in krupier_users:
        names.append(random.choice(nick_to_name_beginning_dictionary[element]))
        surnames.append(random.choice(nick_to_surname_dictionary[element]))
        names_today[element] = names[i] + ' ' + surnames[i]
        if SEND_NICKNAMES_TO_USER:
            user = await client.fetch_user(krupier_users[element])
            message = "Cześć " + element + "! Twoje dzisiejsze imię to: " + names[i]
            try:
                await user.send(message)
            except discord.errors.HTTPException:
                print("User " + element + " failed to receive message")
        i = i + 1
    message = "Dziejsza lista imion:"
    for j in range(len(krupier_users)):
        message = message + '\n' + krupier_users_list[j] + " - " + names[j] + ' ' + surnames[j]
    chan = client.get_channel(768865472552108115)
    await chan.send(message)

    file = open('data/today_names.txt', 'w', encoding='utf-8')
    for i, value in enumerate(names):
        file.write(value + ' ' + surnames[i])
        if not i == len(names) - 1:
            file.write('\n')
    file.close()

def create_lists():
    """Tworzy listy imion i nazwisk zaczynających się na jakieś litery
    z plików data/imiona_polskie.txt i data/surnames.txt
    """
    global NAMES_J
    global NAMES_A
    global NAMES_S
    global NAMES_M
    global NAMES_P
    global NAMES_K
    global NAMES_KZ
    global NAMES_AZ
    if USE_NEW_NAME_FILES:
        with open('data/imiona_polskie.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            content_list = content.split('\n')
            for row in content_list:
                if row.endswith('a'):
                    if row.startswith('K'):
                        NAMES_KZ.append(row)
                    elif row.startswith('A'):
                        NAMES_AZ.append(row)
                elif row.startswith('J'):
                    NAMES_J.append(row)
                elif row.startswith('M'):
                    NAMES_M.append(row)
                elif row.startswith('P'):
                    NAMES_P.append(row)
                elif row.startswith('K'):
                    NAMES_K.append(row)
                elif row.startswith('S'):
                    NAMES_S.append(row)
                elif row.startswith('A'):
                    NAMES_A.append(row)
    else:
        with open('data/male_names.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            content_list = content.split('\n')
            for row in content_list:
                if '-' in row:
                    pass
                elif row.startswith('J'):
                    NAMES_J.append(row)
                elif row.startswith('M'):
                    NAMES_M.append(row)
                elif row.startswith('P'):
                    NAMES_P.append(row)
                elif row.startswith('K'):
                    NAMES_K.append(row)
                elif row.startswith('S'):
                    NAMES_S.append(row)
                elif row.startswith('A'):
                    NAMES_A.append(row)
        with open('data/female_names.txt', 'r', encoding='utf-8') as file:
            for row in file.read().split('\n'):
                if '-' in row:
                    pass
                elif row.startswith('K'):
                    NAMES_KZ.append(row)
                elif row.startswith('A'):
                    NAMES_AZ.append(row)
    with open('data/surnames.txt', 'r', encoding='utf-8') as file:
        global NAZWISKA_K
        global NAZWISKA_P
        global NAZWISKA_Z
        global NAZWISKA_T
        global NAZWISKA_R
        global NAZWISKA_B
        global NAZWISKA_W
        for row in file.read().split('\n'):
            if row.startswith('K'):
                NAZWISKA_K.append(row)
            elif row.startswith('P'):
                NAZWISKA_P.append(row)
            elif row.startswith('Z'):
                NAZWISKA_Z.append(row)
            elif row.startswith('T'):
                NAZWISKA_T.append(row)
            elif row.startswith('R'):
                NAZWISKA_R.append(row)
            elif row.startswith('B'):
                NAZWISKA_B.append(row)
            elif row.startswith('W'):
                NAZWISKA_W.append(row)

async def check_for_new_day(client):
    """Sprawdza czy jest nowy dzień i wykonuje wymagane operacje jeżeli jest

    Args:
        client (client): Sesja discorda bota
    """
    date = get_value('date')
    cur_date = datetime.today().strftime('%Y-%m-%d')
    global ASSIGNED_NICKNAMES
    global SHOULD_EMOJI_BOT_CHANGE_NICKNAMES

    print('Date from file is ' + cur_date)
    print('Date from current time is ' + date)

    if not date == cur_date:
        print('It is a new day! Welcome to ' + date)
        reset_sents()
        create_lists()
        if SHOULD_EMOJI_BOT_CHANGE_NICKNAMES:
            await new_day(client)
            await change_nicknames(client)
        store_value('date', cur_date)
    elif not ASSIGNED_NICKNAMES:
        ASSIGNED_NICKNAMES = True
        file = open('data/today_names.txt', 'r', encoding='utf-8')
        names = file.read().split('\n')
        i = 0
        for element in names_today:
            names_today[element] = names[i]
            i = i + 1

async def change_nicknames(client):
    """Zmienia nicki osób z Krupiera na dzisiejsze

    Args:
        client (client): Sesja discorda bota
    """
    guild = await client.fetch_guild(768865472552108112)
    members = await guild.fetch_members(limit=100).flatten()

    for member in members:
        if member.id in krupier_ids:
            try:
                await member.edit(nick=names_today[inverse_krupier_users[member.id]])
            except discord.errors.Forbidden:
                print('Failed to change nick of id: ' + str(member.id) +
                 '. This is user: ' + inverse_krupier_users[member.id])

async def return_nicknames(client):
    """Przywraca nicki wszystkich osób z Krupiera do domyślnych

    Args:
        client (client): Sesja discorda bota
    """
    guild = await client.fetch_guild(768865472552108112)
    members = await guild.fetch_members(limit=100).flatten()

    for member in members:
        if member.id in krupier_ids:
            try:
                await member.edit(nick=names_to_nick[inverse_krupier_users[member.id]])
            except discord.errors.Forbidden:
                print('Failed to change nick of id: ' + str(member.id) +
                 '. This is user: ' + inverse_krupier_users[member.id])

async def change_nicknames_to_custom(client):
    """Zmienia nicki wszystkich na customowe

    Args:
        client (client): Sesja discorda bota
    """
    guild = await client.fetch_guild(768865472552108112)
    members = await guild.fetch_members(limit=100).flatten()

    for member in members:
        if member.id in krupier_ids:
            try:
                await member.edit(nick=names_to_custom_nick[inverse_krupier_users[member.id]])
            except discord.errors.Forbidden:
                print('Failed to change nick of id: ' + str(member.id) +
                 '. This is user: ' + inverse_krupier_users[member.id])

async def write_to_channel(message, client):
    """Pisze do określonego kanału

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja zalogowania bota
    """
    trunc = message.content.removeprefix('emoji napisz do ')

    for i, value in enumerate(trunc):
        if value == 'e':
            end_of_numbers = i
            break

    nums = trunc[0:end_of_numbers]
    cont = trunc[end_of_numbers+2:len(trunc)]
    chan = await client.fetch_channel(int(nums))
    await chan.send(cont)

async def dm_user(message, client):
    """Pisze prywatną wiadomość do osoby

    Args:
        message (message): Otrzymana wiadomość
        client (client): Sesja discorda bota
    """
    trunc = message.content.removeprefix('emoji dm ')

    for i, value in enumerate(trunc):
        if value == 'e':
            end_of_numbers = i
            break

    nums = trunc[0:end_of_numbers]
    cont = trunc[end_of_numbers+2:len(trunc)]
    user = await client.fetch_user(int(nums))
    await user.send(cont)

async def good_blank(client):
    """Wysyła dobrą wiadomość

    Args:
        client (client): Sesja discorda bota
    """
    hour = datetime.now().hour
    print('The current hour is ' + str(hour))
    path = 'a'


    if sending_hours[0][0] <= hour <= sending_hours[0][1]:
        if not check_if_good_sent(1):
            path = 'data/good_morning.png'
            key = '/sent_good_morning'
    elif sending_hours[1][0] <= hour <= sending_hours[1][1]:
        if not check_if_good_sent(2):
            path = 'data/good_afternoon.png'
            key = 'sent_good_afternoon'
    elif sending_hours[2][0] <= hour <= sending_hours[2][1]:
        if not check_if_good_sent(3):
            path = 'data/good_evening.png'
            key = 'sent_good_evening'
    if not path == 'a':
        chan = client.get_channel(768865472552108115)
        await chan.send(file=discord.File(path))
        store_value(key, 1)

def check_if_good_sent(which):
    """Sprawdza czy dana dobra wiadomość była już wysłana

    Args:
        which (int): Która wiadomość (1, 2, 3)

    Returns:
        bool: Czy dobra wiadomość była już wysłana
    """
    if which == 1:
        path = 'sent_good_morning.txt'
    elif which == 2:
        path = 'sent_good_afternoon.txt'
    elif which == 3:
        path = 'sent_good_evening.txt'
    file = open('data/' + path, 'r')
    sent = int(file.read())
    if sent == 1:
        return True
    else:
        return False

def reset_sents():
    """Resetuje pliki z wysłanymi dobrymi wiadomościami
    """
    print('Resetting sent good messages...')
    store_value('sent_good_morning', '0')
    store_value('sent_good_afternoon', '0')
    store_value('sent_good_evening', '0')

async def delete_message_by_id(message, client):
    """Usuwa wiadomość o podanym id

    Args:
        message ([message]): Objekt wiadomości o stylu 'emoji usun 21743890'
        client (client): sesja discorda bota
    """
    trunc = message.content.removeprefix('emoji usun ')

    for i, value in enumerate(trunc):
        if value == 'e':
            end_of_channel_id = i
            break

    channel_id = int(trunc[0:end_of_channel_id])
    message_id = int(trunc[end_of_channel_id+2:len(trunc)])
    channel = await client.fetch_channel(channel_id)
    mess = await channel.fetch_message(message_id)
    await mess.delete()

async def paper_janka(message):
    await message.channel.send(file=discord.File('src/paper_janka_1.jpg'))
    await message.channel.send(file=discord.File('src/paper_janka_2.jpg'))
    await message.channel.send(file=discord.File('src/paper_janka_3.jpg'))
    await message.channel.send(file=discord.File('src/paper_janka_4.jpg'))

async def policjant(client, message):
    await message.guild.me.edit(nick='Policjant')
    file = open('src/policjant.jpg', 'rb')
    pfp = file.read()
    file.close()
    await client.user.edit(avatar=pfp)

async def deszcz(message):
    for i in range(7):
        m = "🕷️"
        for j in range(25):
            if random.randint(0,7) == 1:
                m += "💧"
            else:
                m += "     "
        await message.channel.send(m)

async def delft_results(message):
    now = datetime.datetime.now()
    res = datetime.datetime(2022, 4, 14, 22)
    sub = res - now
    s = sub.seconds
    m = s//60
    h = m//60
    s = s % 60
    m = m % 60

    mm = str(m)
    ss = str(s)
    hh = str(h)

    if len(str(s)) == 1:
        ss = f'0{s}'
    if len(str(m)) == 1:
        mm = f'0{m}'
    if len(str(h)) == 1:
        hh = f'0{h}'

    m = await message.channel.send(f'{hh}:{mm}:{ss}')
    store_value('delft_message_id', str(m.id))
    store_value('delft_message_channel_id', str(m.channel.id))

def delft_string():
    now = datetime.datetime.now()
    res = datetime.datetime(2022, 4, 14, 22)
    sub = res - now
    s = sub.seconds
    m = s//60
    h = m//60
    s = s % 60
    m = m % 60

    mm = str(m)
    ss = str(s)
    hh = str(h)
    if len(str(s)) == 1:
        ss = f'0{s}'
    if len(str(m)) == 1:
        mm = f'0{m}'
    if len(str(h)) == 1:
        hh = f'0{h}'

    return f'{hh}:{mm}:{ss}'

async def delft_message(client):
    mess_id = get_value('delft_message_id')
    chan_id = get_value('delft_message_channel_id')
    channel = await client.fetch_channel(int(chan_id))
    message = await channel.fetch_message(int(mess_id))
    await message.edit(content=f'**{delft_string()}**')

def bot_selection(msg):
    bots = []
    if msg == '':
        return [1]
    
    separated_bots = msg.split(',')

    for bot in separated_bots:
        if '-' in bot:
            rg = bot.split('-')
            for i in range(int(rg[0]),int(rg[1])+1):
                bots.append(i)
        else:
            bots.append(int(bot))
    
    bots_final = []
    for i in range(1,11):
        if i in bots:
            bots_final.append(i)
    
    return bots_final
            