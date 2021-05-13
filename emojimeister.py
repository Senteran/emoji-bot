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

#
# WAŻNE! Do działanie trzeba zainstalować dodatkowo moduł: windows-curses
#

client = discord.Client()
gis = GoogleImagesSearch('AIzaSyBgsrLkQ5F12eUmhM1V0x5jEkh65cdhp-c', '6a39c51a75423e301')


beast_mode = False
banned_ids = []
beast_banned_ids = []
prefix = ''
suffix = ''
Initilise_Variables()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global beast_mode
    global prefix
    global suffix

    if message.author == client.user:
        return
    
    # Normal bans
    if str(message.author.id) in banned_ids and not isinstance(message.channel, discord.channel.DMChannel):
        await delete_message(message)
        await send_message(message, random.choice(deletion_responses))
        return
    
    # Beast mode bans
    if beast_mode == True and str(message.author.id) in beast_banned_ids and not isinstance(message.channel, discord.channel.DMChannel):
        await delete_message(message)
        await send_message(message, random.choice(deletion_responses))
        return

    # Stworzenie temp_content które zmienia content wiadomości na same małe znaki
    content = process_content(message.content)

    # emoji reactions
    # default emoji
    await default_reactions(message, content)

    # customowe emoji
    await custom_reactions(message, client, content)

    # Granie muzyki
    await play_default_music(message, content)

    # Zmienienie prefiksu
    if message.content.startswith('nowy prefix ') or message.content.startswith('nowy prefiks '):
        change_prefix(message)

    # Wyświetlenie prefiksu
    if 'jaki prefix' in content or 'jaki prefiks' in content:
        display_prefix(message)
    
    # Zmienienie sufiksu
    if message.content.startswith('nowy sufiks ') or message.content.startswith('nowy suffix'):
        change_suffix(message)

    # Wyświetlenie sufiksu
    if 'jaki sufix' in content or 'jaki suffix' in content:
        await display_suffix(message)
    
    # Granie muzyki los santos
    if prefix + ' zagraj ' in message.content:
        await play_music(message)
        

    # send messages
    await send_messages(content, message)

    if message.content.startswith("trójkąt "):
        await send_word_triangle(message, content)

    # Zdjęcie profilowe z Google Image Search
    if message.content.startswith('emoji zdjęcie '):
        await search_for_image(message, client, gis)

    # Wyświetlenie liczby reakcji
    if 'ile reakcji' in content:
        """ function
        file = open('data/reactions.txt', 'r')
        reactions = file.read()
        await message.reply('Już zareagowałem: ' + reactions + ' razy!')
        """
    
    # Wchodzenie na kanał
    if message.content.startswith(prefix) and ' wejdz' in content:
        """ function
        channel = message.author.voice.channel
        await channel.connect()
        """

    # Wychodzenie z kanału
    if (message.content.startswith(prefix) and ' wyjdz' in content) or 'https://tenor.com/view/robert-kubica-orlen-wypierdalaj-autograph-signing-gif-14480393' in message.content:
        """ function
        await message.add_reaction('👋')
        await message.guild.voice_client.disconnect()
        """
    
    # Stop muzyki
    if message.content.startswith(prefix) and ' stop' in content:
        """ function
        await message.add_reaction('🛑')
        message.guild.voice_client.stop()
        """
    
    # Pauza muzyki
    if message.content.startswith(prefix) and ' pauza' in content:
        """ function
        await message.add_reaction('⏸')
        message.guild.voice_client.pause()
        """
    
    # Wstrzymanie muzyki
    if message.content.startswith(prefix) and ' wznow' in content:
        """ function
        await message.add_reaction('⏯')
        message.guild.voice_client.resume()
        """
    
    # Ręczna odpowiedź
    if 'czesc' in content and ' ' + prefix in message.content and 'meister' in content:
        """ function
        response = input('Input the response to ' + message.content + ': ')
        await message.reply(response)
        """
    
    # I am the cum beast
    if 'co wy macie z tym kamem?' == content:
        """ function
        file = open('pictures/cum_beast.jpg', 'rb')
        pfp = file.read()
        file.close()
        await client.user.edit(avatar=pfp)
        await message.guild.me.edit(nick='The cum beast')
        await message.channel.send('I am the cum beast')
        """
    
    # The return of emojimeister
    if 'emojimeister wroc' == content:
        """ function
        file = open('pictures/emoji_fp.png', 'rb')
        pfp = file.read()
        file.close()
        await client.user.edit(avatar=pfp)
        await message.guild.me.edit(nick=prefix[0 : min(len(prefix), 29)] + suffix[0 : 29 - len(prefix)])
        """

    # los santos customs (ultra customowe rzeczy)
    # Witczak combinations for ending the call
    if 'witczak' in content or ('spotkanie' in content and ('zakonczyl' in content or 'zamknal' in content)):
        """ function
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)
        """

    # Two reactions for 'tomek'
    if 'tomek' in content:
        """ function
        emoji = get(client.emojis, name='tomek')
        await message.add_reaction(emoji)
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)
        """

    # Beast mode on
    if message.content == 'cum_beast_mode on' and message.author.id in admin_ids:
        """ function
        beast_mode = True
        await client.change_presence(activity=discord.Game('Cum Beast Mode'))
        """
    # Beast mode off
    if message.content == 'cum_beast_mode off' and message.author.id in admin_ids:
        """ function
        beast_mode = False
        await client.change_presence(status=None)
        """
    
    # Erty jest zajęty
    if message.content == 'erty?':
        """ function
        await message.reply('erty jest zaerty')
        """

client.run('ODMyMjIzNDczOTk2MTM2NDU5.YHgqgg.KDDH0Nlre0nunCwPdu-TlinpPPw')
