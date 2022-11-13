from os import stat
from mcstatus import MinecraftServer
import datetime

from file_handler import store_value, get_value
import discord
import datetime

# CONSTANTS
CHANNEL = 923257476747526227
KARERTY = 960470484116439040
MINIMUM_PERSONS = 160
SEND_DELAY = 30000
CHECK_DELAY = 600
BEFORE_HOUR = 7
AFTER_HOOUR = 22

async def shotbow_checker(client):
    now = datetime.datetime.now()
    hour = now.hour

    if hour >= AFTER_HOOUR or hour <= BEFORE_HOUR:
        store_value('check_result', '0')
        return
    
    server = MinecraftServer.lookup("play.shotbow.net")
    status = server.status()
    if status.players.online > MINIMUM_PERSONS:
        chan = client.get_channel(CHANNEL)

        # commented out in order for the bot to not send messages and constantly check
        # await chan.send("Aktualnie na shotbole gra {0} graczy".format(status.players.online))
        # store_value('check_result', '1')

        store_value('check_result', '0')
    else:
        store_value('check_result', '0')
    
    await client.change_presence(activity=discord.Game(f'with {status.players.online} players on Shotbow'))


async def shotbow_request(client, message):
    server = MinecraftServer.lookup("play.shotbow.net")
    status = server.status()
    await message.reply('Aktualnie na shotbole gra {0} graczy'.format(status.players.online))
    await client.change_presence(activity=discord.Game(f'with {status.players.online} players on Shotbow'))


async def status_message(channel, last, status, mobile):
    cur = datetime.datetime.now()
    created = last.created_at

    cur_mod = cur
    cur_mod += datetime.timedelta(hours=1)
    

    min = f"{cur_mod.minute}"
    if cur_mod.minute < 10:
        min = f"0{min}"
    
    mob = " "
    if mobile:
        mob = " mobile "
    
    message = f'{cur_mod.hour}.{min}{mob}{status}'

    if last.content == message:
        return
    
    if status == discord.Status.online:
        s = await channel.send(message)
        store_value('last_statuserty_message_id', str(s.id))
    else:
        mess = await channel.fetch_message(int(get_value('last_statuserty_message_id')))
        c = mess.content
        c += f'\n{message}'
        await mess.edit(content=c)

async def karerty_message(message, client):
    channel = client.get_channel(KARERTY)

    await channel.send(message)