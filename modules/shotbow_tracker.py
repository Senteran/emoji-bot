import discord
from mcstatus import MinecraftServer

# CONSTANTS
CHANNEL = 923257476747526227
MINIMUM_PERSONS = 150
DM_SENTERAN = True
SEND_DELAY = 30000
CHECK_DELAY = 600

async def shotbow_checker(client):
    server = MinecraftServer.lookup("play.shotbow.net")
    status = server.status()
    file = open('data/check_result.txt', 'w', encoding='utf-8')
    if status.players.online > MINIMUM_PERSONS:
        chan = client.get_channel(CHANNEL)
        await chan.send("Aktualnie na shotbole gra {0} graczy".format(status.players.online))
        file.write("1")
    else:
        file.write("0")
    file.close()
    
    if DM_SENTERAN:
        user = await client.fetch_user(351780319306973194)
        await user.send('obudziłem się!')