import discord
from discord.utils import get

emoji_library = {
    'haha': '😆',
    'kurwa': '🚫',
    'nie wiem': '🤷',
    'śpi': '💤',
    'spi': '💤',
    'świat': '🌍',
    'swiat': '🌍',
    'tak': '✅',
    'krupiergames.000webhostapp.com/ia': '🛑',
    'nie': '❎',
    'stundink': '🧑‍🎤',
    'studnik': '🧑‍🎤',
    'spicy': '🌶',
    'ostr': '🌶',
    'bruh': '🦕',
    'xd': '😂',
    'kurde': '😯',
    'proszę': '🙏',
    'prosze': '🙏',
    'agar': '🔴',
    'ok': '👌',
    'dobra': '👌',
    'intj': '♑',
    'entj': '♑',
    'angielski': '🐚',
    'o co chodzi': '❓',
    'co sie dzieje': '❓',
    'co sie stalo': '❓',
    'kiedy': '❓',
    'emojimeister': '🐱‍👤',
    '-p': '▶',
    '-leave': '👋',
    'stop': '🛑',
    'hej': '👋',
    'cześć': '👋',
    'czesc': '👋',
    'siema': '👋',
    'hello': '👋',
    'halo': '👋',
    '?': '🧐',
    'rage': '👺',
    'wściekły': '👺',
    'wsciekly': '👺',
    'wkurwi': '👺',
    'denerwuj': '👺',
    'zły': '👺',
    'zly': '👺',
    'ola': '👩',
    'karolina': '👩‍🦰'
}

custom_emoji_library = {
    'erty': 'ertymaster',
    'adam': 'ertymaster',
    'bigas': 'ertymaster',
    'senteran': 'senteran',
    'jacek': 'senteran',
    'kulik': 'senteran',
    'krupier': 'krupier',
    'janek': 'krupier',
    'pytel': 'krupier',
    'krupr': 'krupier',
    'sebek': 'sebek',
    'seba': 'sebek',
    'timm': 'sebek',
    'exeos': 'exeos',
    'paweł': 'exeos',
    'pawel': 'exeos',
    'zając': 'exeos',
    'zajac': 'exeos',
    'kuchta': 'kuchta',
    'mariusz': 'kuchta',
    'praczyns': 'praczyns',
    'raczynski': 'praczyns',
    'alan': 'hot_dog_nibba',
    'frido': 'frido',
    'fat pusher': 'fat_pusher',
    'wf': 'tomek',
    'chad': 'chad',
    'fajrancik': 'fajrancik',
    'nie odpisuje': 'ertymaster',
    'eleganc': 'koneser',
    'wtf': 'wtf',
    'ertymi': 'ertymi',
    'ertymeister': 'ertymeister',
    'clyde': 'clyde',
    'cas': 'cas',
    'bw': 'bw',
    'auto': 'auto',
    'bmw': 'auto',
    'ford': 'auto',
    'skoda': 'auto',
    'benet': 'benet_rekord',
    'business merger': 'business_merger',
    'się rozgrzać': 'witczak',
    'sie rozgrzac': 'witczak',
    'oczadły': 'tomek',
    'oczadly': 'tomek',
    'tomek': 'tomek',
    'witczak': 'witczak',
    'bazyl': 'bazyl',
    'najman': 'najman',
    'mama': 'mama',
    'lis': 'lis',
    'kp': 'kp',
    'an': 'an',
    'presentetaio': 'presentetaio'
}

send_library = {
    'adres ip serwera': 'Adres ip serwera minecraft: 25.30.92.167',
    'login do hamachi': 'Login do hamachi: Senteran12345 (możliwe także +6, + 7), hasło: senteran12',
    'ile masz lat': 'urodziłęm się 15 kwietnia 2021, możesz chyba samodzielnie obliczyć!',
    'co potrafisz?': 'reagować na wiadomości!',
    'kiedy się spotykamy': 'Ja mogę z wami zawsze być ♥',
    'jak się nauczyć grać w poe?': 'Polecam ten poradnik: https://www.poe-vault.com/guides/ultimate-beginners-comprehensive-guide',
    'w co gramy': 'Wykres dostępnych gier jest dostępny tu: https://docs.google.com/spreadsheets/d/1BefpD-0jU_2GDn-yyG8_-HUVYyUBxnoK86ntY4O6Uo4/edit#gid=0',
    'tata simulator': 'Link do pobrania tata simulator (działa tylko na windows): https://drive.google.com/drive/folders/1tQjZv3pjK8dkdnYODdlfq6dPs4nKYdkW?usp=sharing'
}

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content
    content = content.lower()

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

    # send messages
    for element in send_library:
        if element in content:
            await message.channel.send(send_library[element])

    if 'ile reakcji' in content:
        file = open('reactions.txt', 'r')
        reactions = file.read()
        await message.reply('Już zareagowałem: ' + reactions + ' razy!')

    # los santos customs (ultra customowe rzeczy)
    if content == 'dajesz tensa' or content == 'dawaj tensa':
        channel = message.author.voice.channel
        await channel.connect()
        filename = 'rage.mp3'
        server = message.guild
        voice_channel = server.voice_client
        voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg.exe', source=filename))
        await message.channel.send('Currently playing: tense1983 rage compilation')

    if 'witczak' in content or ('spotkanie' in content and (
            'zakonczyl' in content or 'zakończył' in content or 'zamknął' in content or 'zamknal' in content)):
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)


def reaction():
    file = open('reactions.txt', 'r')
    reactions = int(file.read())
    reactions = reactions + 1
    file.close()
    file = open('reactions.txt', 'w')
    file.write(str(reactions))
    file.close()


client.run('ODMyMjIzNDczOTk2MTM2NDU5.YHgqgg.KDDH0Nlre0nunCwPdu-TlinpPPw')
#Podpis Senterana