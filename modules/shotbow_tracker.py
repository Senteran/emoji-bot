from os import stat
from mcstatus import MinecraftServer

from file_handler import store_value
import discord
import datetime

# CONSTANTS
CHANNEL = 923257476747526227
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
        await chan.send("Aktualnie na shotbole gra {0} graczy".format(status.players.online))
        store_value('check_result', '1')
    else:
        store_value('check_result', '0')
    
    await client.change_presence(activity=discord.Game(f'with {status.players.online} players on Shotbow'))


async def shotbow_request(client, message):
    server = MinecraftServer.lookup("play.shotbow.net")
    status = server.status()
    await message.reply('Aktualnie na shotbole gra {0} graczy'.format(status.players.online))
    await client.change_presence(activity=discord.Game(f'with {status.players.online} players on Shotbow'))