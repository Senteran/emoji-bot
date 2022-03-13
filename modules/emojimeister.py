"""
    This is the main module of the application.
    It handles the running of the bot and initiates functions
"""
from logging import exception
import sys
import os
import asyncio
import time

import discord
from discord.utils import get
from google_images_search import GoogleImagesSearch

from dictionaries import admin_ids, krupier_users, AGAR_AGAR_CHANNEL
from file_handler import get_value
from modules.dictionaries import SHOTBOW_TRACKER_DISCORD_ID, STATUSERTY_CHANNEL
from shotbow_tracker import CHECK_DELAY, SEND_DELAY, shotbow_checker, shotbow_request
from word import send_word_of_emojis
from slalom import emoji_slalom, emoji_slalom_infinite

from functions import\
    initilise_variables, process_content, default_reactions,\
    custom_reactions,play_default_music, change_prefix, display_prefix, change_suffix,\
    display_suffix, play_music, send_messages, send_word_triangle, search_for_image,\
    display_reactions, join_voice_channel, leave_voice_channel, pause_music,\
    resume_music, manual_response, emojimeister_return,\
    custom_reaction, beast_mode_on, beast_mode_off, reply_to_message, help_other_helps,\
    help_commands, help_replies, help_songs, help_emoji, help_custom_emoji,\
    change_nicknames, return_nicknames, write_to_channel, dm_user,\
    PREFIX, BEAST_MODE, change_nicknames_to_custom,\
    delete_message_by_id, paper_janka

# prevent __pycache__ folder from being created
sys.dont_write_bytecode = True


# WAŻNE! Do działanie trzeba zainstalować dodatkowo moduł: windows-curses
# dzięki, pomocny komentarz!

intnets = discord.Intents.all()
client = discord.Client(intents = intnets)
client2 = discord.Client(intents = intnets)
gis = GoogleImagesSearch(os.getenv('GOOGLE_KEY'), '6a39c51a75423e301')

CHANGE_NICKS = False
MANUAL_RESPONSE = False
SEND_GOOD_MESSAGES = False
GO_TO_SVB = False
GO_TO_KRUPIER = True
THIS_SHOULDNT_EXIST = False

initilise_variables()

async def shotbow(client_t):
    while True:
        await shotbow_checker(client_t)
        s = get_value('check_result')
        if s == '1':
            await asyncio.sleep(SEND_DELAY)
        else:
            await asyncio.sleep(CHECK_DELAY)

@client.event
async def on_ready():
    """This runs upon the bot logging in to Discord servers"""
    print("Logged in as {0.user}".format(client))

    print('List of available servers:')
    for server in client.guilds:
        print(server)

    if GO_TO_KRUPIER: 
        channel = await client.fetch_channel(788023076402495518)
        await channel.connect()
    if GO_TO_SVB: 
        channel = await client.fetch_channel(640859405247709185)
        channel.connect()
    await shotbow(client2)


@client.event
async def on_message(message):
    """This runs upon a message being sent where the bot can see it,
    so it can be a DM or a message in a channel"""
    global BEAST_MODE
    global PREFIX

    content = process_content(message.content)

    if message.author == client.user:
        await default_reactions(message, content)
        await custom_reactions(message, client, content)
        return

#DISABLED BECAUSE SENDING GOOD MESSAGES IS OFF AND THIS IS A HUGE RESOURCE HOG
#  await check_for_new_day(client)
#  if SEND_GOOD_MESSAGES:
#    await good_blank(client)

    # emoji reactions
    # default emoji
    await default_reactions(message, content)

    # customowe emoji
    await custom_reactions(message, client, content)

    # Granie muzyki
    await play_default_music(message, content)

    # Zmienienie prefiksu
    if message.content.startswith('emoji prefix ') or message.content.startswith('emoji prefiks '):
        await change_prefix(message)

    # Wyświetlenie prefiksu
    if 'jaki prefix' in content or 'jaki prefiks' in content:
        await display_prefix(message)

    # Zmienienie sufiksu
    if message.content.startswith('emoji sufiks ') or message.content.startswith('emoji suffix'):
        await change_suffix(message)

    # Wyświetlenie sufiksu
    if 'jaki sufix' in content or 'jaki suffix' in content:
        await display_suffix(message)

    # Granie muzyki los santos
    if PREFIX + ' zagraj ' in message.content:
        await play_music(message)

    # send messages
    await send_messages(content, message)

    if message.content.startswith("trójkąt "):
        await send_word_triangle(message)

    # Zdjęcie profilowe z Google Image Search
    if message.content.startswith('emoji zdjęcie '):
        await search_for_image(message, client, gis)

    # Wyświetlenie liczby reakcji
    if 'ile reakcji' in content:
        await display_reactions(message)

    # Wchodzenie na kanał
    if message.content.startswith(PREFIX) and ' wejdz' in content:
        await join_voice_channel(message)

    # Wychodzenie z kanału
    if ((message.content.startswith(PREFIX) and ' wyjdz' in content) or
     'https://tenor.com/view/robert-kubica-orlen-wypierdalaj-autograph-signing-gif-14480393'
      in message.content):
        await leave_voice_channel(message)

    # Stop muzyki
    if message.content.startswith(PREFIX) and ' stop' in content:
        await pause_music(message)

    # Pauza muzyki
    if message.content.startswith(PREFIX) and ' pauza' in content:
        await pause_music(message)

    # Wstrzymanie muzyki
    if message.content.startswith(PREFIX) and ' wznow' in content:
        await resume_music(message)

    # Ręczna odpowiedź
    if 'czesc' in content and 'meister' in content and MANUAL_RESPONSE is True:
        await manual_response(message)

    # The return of emojimeister
    if content == 'emojimeister wroc':
        await emojimeister_return(message, client)
    
    if content == 'emoji slalom':
        try:
            await emoji_slalom(client, message)
        except Exception as e:
            print(f'error in emoji slalom, {e}')
    
    if content == 'emoji slalom inf' and False:
        await emoji_slalom_infinite(client, message)

    # los santos customs (ultra customowe rzeczy)
    # Witczak combinations for ending the call
    if ('witczak' in content or
    ('spotkanie' in content and ('zakonczyl' in content or 'zamknal' in content))):
        await custom_reaction(message, client, 'witczak')

    # Two reactions for 'tomek'
    if 'tomek' in content:
        await custom_reaction(message, client, 'witczak')
        await custom_reaction(message, client, 'tomek')

    if 'hokej' in content:
        emoji = get(client.emojis, name='sebek')
        await message.add_reaction(emoji)
        await message.add_reaction('🏒')

    if 'furnik' in content:
        emoji = get(client.emojis, name='krupier')
        await message.add_reaction(emoji)
        await message.add_reaction('👺')
    
    if content == 'emoji paper janka':
        await paper_janka(message)

    # Beast mode on
    if message.content == 'cum_beast_mode on' and message.author.id in admin_ids:
        await beast_mode_on(client)

    # Beast mode off
    if message.content == 'cum_beast_mode off' and message.author.id in admin_ids:
        await beast_mode_off(client)

    # Erty jest zajęty
    if message.content == 'erty?':
        await reply_to_message(message, 'erty jest zajety')

    if content == 'emoji help':
        await help_other_helps(message)

    if message.content.startswith('emoji napisz do '):
        try:
            await write_to_channel(message, client)
        except discord.errors.HTTPException:
            await message.reply('The message failed to send')

    if message.content.startswith('emoji dm '):
        try:
            await dm_user(message, client)
        except discord.errors.HTTPException:
            await message.reply('The DM failed to send')

    if message.content.startswith('emoji usun '):
        try:
            await delete_message_by_id(message, client)
        except discord.errors.HTTPException:
            await message.reply('An error occurred')
    
    if content.startswith('emoji slowo '):
        c = content.split(' ')
        await send_word_of_emojis(message, c[2], c[3:])
        try:
            c = content.split(' ')
            # await send_word_of_emojis(message, c[2], c[3:])
        except Exception as e:
            print(f'Exception in emoji slowo: {e}')
            await message.reply('An error occurred')

    if ' ekonomi ' in content or content[len(content)-7:len(content)] == 'ekonomi':
        try:
            await message.reply('ekonomii')
        except discord.errors.HTTPException:
            pass

    if content == 'emoji commands':
        await help_commands(message)

    if content == 'emoji replies':
        await help_replies(message)

    if content == 'emoji songs':
        await help_songs(message)

    if content == 'emoji emoji':
        await help_emoji(message)

    if content == 'emoji emoji_krupier' and message.author.id in admin_ids:
        await help_custom_emoji(message, client)

    if message.content == 'fqeauiho4378worefihusd':
        await return_nicknames(client)

    if message.content == 'f47q3hewaouilgf4wtgerswyhgs':
        await change_nicknames(client)

    if message.content == '37485euytwrohijldk4t89euir':
        await change_nicknames_to_custom(client)
    
    if message.content == '9843qujfrweailsdnkctq48frewpjiao':
        print('test')

    if 'krupier to furnik' in content:
        await reply_to_message(message, "Krupier to *furnik* ma wymóg")

@client.event
async def on_member_update(before, after):
    global THIS_SHOULDNT_EXIST
    if before.id == krupier_users['exeos']:
        if before.mobile_status == discord.Status.offline and after.mobile_status == discord.Status.online:
            if THIS_SHOULDNT_EXIST == False:
                channel = await client.fetch_channel(AGAR_AGAR_CHANNEL)
                await channel.send(f"<@!{krupier_users['exeos']}>")
                emoji = get(client.emojis, name='exeos_mobile')
                await channel.send(emoji)
                THIS_SHOULDNT_EXIST = True
            else:
                THIS_SHOULDNT_EXIST =False

@client2.event
async def on_message(message):
    content = process_content(message.content)

    if content == 'ile gra' or content == 'ile gra?':
        await shotbow_request(client2, message)

@client2.event
async def on_member_update(before, after):
    print('update')
    if before.id == krupier_users['Senteran']:
        cur = time.time()
        if before.mobile_status != after.mobile_status:
            channel = await client2.fetch_channel(STATUSERTY_CHANNEL)
            message = await channel.history(limit=1).flatten()
            created = message[0].created_at
            
            if cur - created < 5:
                if not message[0].author.id == SHOTBOW_TRACKER_DISCORD_ID:
                    await channel.send(f'ertymaster mobile jest teraz {after.mobile_status} z {before.mobile_status}')
        elif before.status != after.status:
            channel = await client2.fetch_channel(STATUSERTY_CHANNEL)
            message = await channel.history(limit=1).flatten()
            created = message[0].created_at

            if cur - created < 5:
                if not message[0].author.id == SHOTBOW_TRACKER_DISCORD_ID:
                    await channel.send(f'ertymaster pc jest teraz {after.mobile_status} z {before.status}')


async def daily():
    while True:
        await asyncio.sleep(10000)

loop = asyncio.get_event_loop()
loop.create_task(client.start(os.getenv('EMOJI_BOT')))
loop.create_task(client2.start(os.getenv('SHOTBOW_BOT')))
loop.create_task(daily())
loop.run_forever()
