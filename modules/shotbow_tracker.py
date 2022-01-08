from os import stat
from mcstatus import MinecraftServer

from file_handler import store_value
import discord
import datetime

# CONSTANTS
CHANNEL = 923257476747526227
MINIMUM_PERSONS = 160
DM_SENTERAN = False
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
    
    if DM_SENTERAN:
        user = await client.fetch_user(351780319306973194)
        await user.send('obudziłem się!')

async def shotbow_request(message):
    server = MinecraftServer.lookup("play.shotbow.net")
    status = server.status()
    await message.reply('Aktualnie na shotbole gra {0} graczy'.format(status.players.online))