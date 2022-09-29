"""
    This is the main module of the application.
    It handles the running of the bot and initiates functions
"""
import sys
import os
import asyncio

import discord
from discord.utils import get
from google_images_search import GoogleImagesSearch

from dictionaries import admin_ids, krupier_users, STATUSERTY_CHANNEL, OGOLNY_CHANNEL, BUDOWA_CHANNEL, WIEZIENIE_CHANNEL, KRUPIER_ID, EMOJIBOT_ID
from file_handler import get_value
from modules.functions import args_to_string
from shotbow_tracker import CHECK_DELAY, SEND_DELAY, shotbow_checker, shotbow_request, status_message, karerty_message
from word import send_word_of_emojis
from slalom import emoji_slalom, emoji_slalom_infinite

from functions import\
    process_content, default_reactions,\
    custom_reactions,play_default_music, play_music, send_messages, send_word_triangle, search_for_image,\
    display_reactions, join_voice_channel, leave_voice_channel, pause_music,\
    resume_music, manual_response, emojimeister_return,\
    custom_reaction, reply_to_message, help_other_helps,\
    help_commands, help_replies, help_songs, help_emoji, help_custom_emoji,\
    change_nicknames, return_nicknames, write_to_channel, dm_user,\
    BEAST_MODE, change_nicknames_to_custom,\
    delete_message_by_id, paper_janka, policjant, deszcz, delft_results, delft_message, change_nick, attachment_profile_picture, bot_selection

# prevent __pycache__ folder from being created
sys.dont_write_bytecode = True


# WAŻNE! Do działanie trzeba zainstalować dodatkowo moduł: windows-curses
# dzięki, pomocny komentarz!

intnets = discord.Intents.all()
client = discord.Client(intents = intnets)
client2 = discord.Client(intents = intnets)
emoji2 = discord.Client(intnets = intnets)
emoji3 = discord.Client(intnets = intnets)
emoji4 = discord.Client(intnets = intnets)
emoji5 = discord.Client(intnets = intnets)
emoji6 = discord.Client(intnets = intnets)
emoji7 = discord.Client(intnets = intnets)
emoji8 = discord.Client(intnets = intnets)
emoji9 = discord.Client(intnets = intnets)
emoji10 = discord.Client(intnets = intnets)

bots_dict =  {
    1 : client,
    2 : emoji2,
    3 : emoji3,
    4 : emoji4,
    5 : emoji5,
    6 : emoji6,
    7 : emoji7,
    8 : emoji8,
    9 : emoji9,
    10 : emoji10,
}

gis = GoogleImagesSearch(os.getenv('GOOGLE_KEY'), '6a39c51a75423e301')

CHANGE_NICKS = False
MANUAL_RESPONSE = False
SEND_GOOD_MESSAGES = False
GO_TO_SVB = False
GO_TO_KRUPIER = True
THIS_SHOULDNT_EXIST = False
TRACKERTY = True


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
        kr = await client.fetch_guild(KRUPIER_ID)
        me = await kr.fetch_member(EMOJIBOT_ID)
        nick = me.nick
        if nick == "Mieszadło do betonu":
            channel = await client.fetch_channel(BUDOWA_CHANNEL)
            await channel.connect()
        else:
            channel = await client.fetch_channel(WIEZIENIE_CHANNEL)
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

    if content.startswith('emoji'):
        args = message.content.split()
        try:
            bots = bot_selection(args[0].removeprefix('emoji'))
        except:
            bots = []

        for bot in bots:
            current = bots_dict[bot]

            try:
                command = process_content(args[1])
                if command == 'nick':
                    await change_nick(message, current, args[2:])
                elif command == 'zagraj':
                    await play_music(message)
                elif command == 'print':
                    print(args)
                elif command == 'wejdz':
                    await join_voice_channel(message, current)
                elif command == 'zdjecie':
                    await search_for_image(current, args[2:], gis)
                elif command == 'wyjdz' or 'https://tenor.com/view/robert-kubica-orlen-wypierdalaj-autograph-signing-gif-14480393' in message.content:
                    await leave_voice_channel(message, current)
                elif command == 'zdjecie_attachment' or command == 'zdjecie_zalacznik':
                    await attachment_profile_picture(message, current)
                elif command == 'restart':
                    restart()
                elif command == 'status':
                    #await set_status(message, current, args[2:])
                    #await reply(message, current, f'Changing status to {args_to_content(args[2:])}')
                    pass
                    
            except IndexError:
                print('Index error in command parsing')

    

        

    # send messages
    await send_messages(content, message)

    if message.content.startswith("trójkąt "):
        await send_word_triangle(message)

    # Zdjęcie profilowe z Google Image Search
    
    
    

    # Wyświetlenie liczby reakcji
    if 'ile reakcji' in content:
        await display_reactions(message)

    # Wchodzenie na kanał
    

    # Wychodzenie z kanału
    

    # Stop muzyki
    if 'emoji stop' in content:
        await pause_music(message)

    # Pauza muzyki
    if 'emoji pauza' in content:
        await pause_music(message)

    # Wstrzymanie muzyki
    if 'emoji wznow' in content:
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

    # Erty jest zajęty
    if message.content == 'erty?':
        await reply_to_message(message, 'erty jest zajety')

    if content == 'emoji help':
        await help_other_helps(message)

    if message.content.startswith('emoji napisz do ') and not (message.author.id == krupier_users['Krupier']) :
        try:
            await write_to_channel(message, client)
        except discord.errors.HTTPException:
            await message.reply('The message failed to send')

    if message.content.startswith('emoji dm '):
        try:
            await dm_user(message, client)
        except discord.errors.HTTPException:
            await message.reply('The DM failed to send')

    if message.content.startswith('emoji usun ') and message.author.id in admin_ids:
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
    
    if 'mariusz' in content or 'kuchta' in content:
        await message.channel.send(file=discord.File('src\rejection.png'))
    
    if 'emoji policjant' == content:
        await policjant(client, message)
    
    if 'emoji deszcz' == content:
        await deszcz(message)
    
    if message.content == 'emoji odliczanie wyniki delft':
        await delft_results(message)

@client2.event
async def on_message(message):
    content = process_content(message.content)

    if content == 'ile gra' or content == 'ile gra?':
        await shotbow_request(client2, message)
    
    if content.startswith('karerty ') and message.author.id != krupier_users['ertymaster']:
        m = message.content[8:]
        await karerty_message(m, client2)

@client.event
async def on_member_update(before, after):
    if before.id == krupier_users['ertymaster'] and TRACKERTY:
        if before.mobile_status != after.mobile_status:
            channel = await client2.fetch_channel(STATUSERTY_CHANNEL)
            message = await channel.history(limit=1).flatten()

            await status_message(channel, message[0], after.mobile_status, True)
        elif before.status != after.status:
            channel = await client2.fetch_channel(STATUSERTY_CHANNEL)
            message = await channel.history(limit=1).flatten()

            await status_message(channel, message[0], after.status, False)
    
    if before.display_name == "Fallowpelt" and after.display_name == "Senteran":
        await after.edit(nick="Fallowpelt")
        channel = await client.fetch_channel(OGOLNY_CHANNEL)
        message = await channel.history(limit=1).flatten()
        emoji = get(client.emojis, name="nahtzee")
        await message[0].add_reaction(emoji)

async def daily():
    while True:
        await asyncio.sleep(10000)

async def delft_results_loop():
    while True:
        await asyncio.sleep(10)
        await delft_message(client)


loop = asyncio.get_event_loop()
loop.create_task(client.start(os.getenv('EMOJI_BOT')))
loop.create_task(client2.start(os.getenv('SHOTBOW_BOT')))

loop.create_task(emoji2.start(os.getenv('EMOJI2')))
loop.create_task(emoji3.start(os.getenv('EMOJI3')))
loop.create_task(emoji4.start(os.getenv('EMOJI4')))
loop.create_task(emoji5.start(os.getenv('EMOJI5')))
loop.create_task(emoji6.start(os.getenv('EMOJI6')))
loop.create_task(emoji7.start(os.getenv('EMOJI7')))
loop.create_task(emoji8.start(os.getenv('EMOJI8')))
loop.create_task(emoji9.start(os.getenv('EMOJI9')))
loop.create_task(emoji10.start(os.getenv('EMOJI10')))


loop.create_task(delft_results_loop())
loop.run_forever()



def restart():
    intnets = discord.Intents.all()
    client = discord.Client(intents = intnets)
    client2 = discord.Client(intents = intnets)
    emoji2 = discord.Client(intnets = intnets)
    emoji3 = discord.Client(intnets = intnets)
    emoji4 = discord.Client(intnets = intnets)
    emoji5 = discord.Client(intnets = intnets)
    emoji6 = discord.Client(intnets = intnets)
    emoji7 = discord.Client(intnets = intnets)
    emoji8 = discord.Client(intnets = intnets)
    emoji9 = discord.Client(intnets = intnets)
    emoji10 = discord.Client(intnets = intnets)



    loop = asyncio.get_event_loop()
    loop.create_task(client.start(os.getenv('EMOJI_BOT')))
    loop.create_task(client2.start(os.getenv('SHOTBOW_BOT')))

    loop.create_task(emoji2.start(os.getenv('EMOJI2')))
    loop.create_task(emoji3.start(os.getenv('EMOJI3')))
    loop.create_task(emoji4.start(os.getenv('EMOJI4')))
    loop.create_task(emoji5.start(os.getenv('EMOJI5')))
    loop.create_task(emoji6.start(os.getenv('EMOJI6')))
    loop.create_task(emoji7.start(os.getenv('EMOJI7')))
    loop.create_task(emoji8.start(os.getenv('EMOJI8')))
    loop.create_task(emoji9.start(os.getenv('EMOJI9')))
    loop.create_task(emoji10.start(os.getenv('EMOJI10')))


    loop.create_task(delft_results_loop())
    loop.run_forever()