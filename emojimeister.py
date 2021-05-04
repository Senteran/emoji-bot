import sys
# prevent __pycache__ folder from being created
sys.dont_write_bytecode = True

import discord
from discord.utils import get
from os import remove
from modules.dictionaries import *
from modules.functions import *

client = discord.Client()

file = open('data/prefix.txt', 'r')
prefix = file.read()
file.close()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Stworzenie temp_content które zmienia content wiadomości na same małe znaki
    content = message.content
    content = content.lower()
    content = to_en_str(content)

    # emoji reactions
    # default emoji
    for element in emoji_library:
        if element in content:
            await message.add_reaction(emoji_library[element])
            reaction()
    # customowe emoji
    for element in custom_emoji_library:
        if element in content:
            emoji = get(client.emojis, name=custom_emoji_library[element])
            await message.add_reaction(emoji)
            reaction()
    # Granie muzyki
    for element in music_library:
        if element in content:
            channel = message.author.voice.channel
            try:
                await channel.connect()
            except AttributeError:
                pass
            filename = 'src/' + music_library[element]
            server = message.guild
            voice_client = server.voice_client
            voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
            await message.channel.send('Currently playing: ' + music_library[element])

    # Zmienienie prefiksu
    if message.content.startswith('nowy prefix ') or message.content.startswith('nowy prefiks '):
        if message.content.startswith('nowy prefix '):
            new_prefix = message.content.removeprefix('nowy prefix')
        else:
            new_prefix = message.content.removeprefix('nowy prefiks ')
        encoded_prefix = new_prefix.encode('utf-8')
        file = open('data/prefix.txt', 'wb')
        file.write(encoded_prefix)
        file.close()
        global prefix
        prefix = new_prefix
        if len(prefix) >= 24:
            await message.guild.me.edit(nick=prefix[0 : 23]+'meitser')
        else:
            await message.guild.me.edit(nick=prefix+'meister')
    # Wyświetlenie prefiksu
    if 'jaki prefix' in content or 'jaki prefiks' in content:
        await message.channel.send('Aktualny prefiks to: ' + prefix)
    # Granie muzyki los santos
    if prefix + ' zagraj ' in message.content:
        server = message.guild
        voice_client = server.voice_client

        text = message.content
        url = text.removeprefix('emoji zagraj')
        filename = await yt_download(url, 'songs/')
        try:
            voice_client.stop()
        except:
            pass
        voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
        await message.channel.send('**Now playing:** {}'.format(filename.removeprefix('songs/')))
        

        # remove_song jest dopiero tu, ponieważ musi się stać po voice_client.stop() aby nie próbować usunąć pliku w użyciu oraz ponieważ jak było tuż po nim to czasami nie działało
        # sensowną opcją jest więc danie go tu ponieważ jest po await send czyli minie chwila i plik powinien mieć wystarczająco czasu aby przestać być zablokowanym
        remove_song()
        write_song_filename(filename)
        

    # send messages
    for element in send_library:
        if element in content:
            await message.channel.send(send_library[element])
    
    if message.content.startswith("trójkąt "):
        string = word_triangle(message.content.removeprefix("trójkąt "))
        try:
            await message.channel.send(string)
        except discord.errors.HTTPException:
            await message.channel.send("Ta wiadomość byłaby za długa")

    # Wyświetlenie liczby reakcji
    if 'ile reakcji' in content:
        file = open('data/reactions.txt', 'r')
        reactions = file.read()
        await message.reply('Już zareagowałem: ' + reactions + ' razy!')
    
    # Wchodzenie na kanał
    if message.content.startswith(prefix) and ' wejdz' in content:
        channel = message.author.voice.channel
        await channel.connect()

    # Wychodzenie z kanału
    if (message.content.startswith(prefix) and ' wyjdz' in content) or 'https://tenor.com/view/robert-kubica-orlen-wypierdalaj-autograph-signing-gif-14480393' in message.content:
        await message.add_reaction('👋')
        await message.guild.voice_client.disconnect()
    
    # Stop muzyki
    if message.content.startswith(prefix) and ' stop' in content:
        await message.add_reaction('🛑')
        message.guild.voice_client.stop()
    
    # Pauza muzyki
    if message.content.startswith(prefix) and ' pauza' in content:
        await message.add_reaction('⏸')
        message.guild.voice_client.pause()
    
    # Wstrzymanie muzyki
    if message.content.startswith(prefix) and ' wznow' in content:
        await message.add_reaction('⏯')
        message.guild.voice_client.resume()
    
    # Ręczna odpowiedź
    if 'czesc' in content and ' ' + prefix in message.content and 'meister' in content:
        response = input('Input the response to ' + message.content + ': ')
        await message.reply(response)

    # los santos customs (ultra customowe rzeczy)
    # Witczak combinations for ending the call
    if 'witczak' in content or ('spotkanie' in content and ('zakonczyl' in content or 'zamknal' in content)):
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)

    # Two reactions for 'tomek'
    if 'tomek' in content:
        emoji = get(client.emojis, name='tomek')
        await message.add_reaction(emoji)
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)

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

# Dodaje ścieżkę danej piosenki do pliko data/song.txt
def write_song_filename(filename):
    file = open('data/song.txt', 'w')
    file.write(filename)
    file.close()

# Dodaje 1 do pliku data/reactions.txt
def reaction():
    file = open('data/reactions.txt', 'r')
    reactions = int(file.read())
    reactions = reactions + 1
    file.close()
    file = open('data/reactions.txt', 'w')
    file.write(str(reactions))
    file.close()


client.run('ODMyMjIzNDczOTk2MTM2NDU5.YHgqgg.KDDH0Nlre0nunCwPdu-TlinpPPw')
