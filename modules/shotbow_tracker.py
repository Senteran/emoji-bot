from mcstatus import MinecraftServer

from file_handler import store_value

# CONSTANTS
CHANNEL = 923257476747526227
MINIMUM_PERSONS = 150
DM_SENTERAN = False
SEND_DELAY = 30000
CHECK_DELAY = 600

async def shotbow_checker(client):
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