from random import random
import discord
import random
import asyncio

from dictionaries import voice_channels




async def emoji_slalom_iter(client, message):
    wait = random.randint(5, 15)
    chan_id = random.sample(voice_channels, 1)

    chan = await client.get_channel(chan_id)
    try:
        await chan.connect()
    except discord.errors.ClientException:
        await message.guild.voice_client.disconnect()
        try:
            await chan.connect()
        except Exception as e:
            print(f'Slalom error, {e}')
    
    await asyncio.sleep(wait)

loop = asyncio.get_event_loop()


async def emoji_slalom(client, message):
    for i in range(5):
        wait = random.randint(5, 15)
        chan_id = random.sample(voice_channels, 1)

        chan = await client.get_channel(chan_id)
        try:
            await chan.connect()
        except discord.errors.ClientException:
            await message.guild.voice_client.disconnect()
            try:
                await chan.connect()
            except Exception as e:
                print(f'Slalom error, {e}')
        
        await asyncio.sleep(wait)

async def emoji_slalom_infinite(client, message):
    loop.create_task(emoji_slalom_iter(client, message))
    loop.run_forever()

async def cancel_infinite_slalom():
    for task in loop:
        task.cancel()