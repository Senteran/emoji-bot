import discord
from discord.utils import get
import youtube_dl
import asyncio
from os import remove

emoji_library = {
    'haha': '😆',
    'kurwa': '🚫',
    'nie wiem': '🤷',
    'spi': '💤',
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
    'emojimeister': '🤚',
    '-p': '▶',
    '-leave': '👋',
    'stop': '🛑',
    'hej': '👋',
    'czesc': '👋',
    'siema': '👋',
    'hello': '👋',
    'halo': '👋',
    '?': '🧐',
    'rage': '👺',
    'wsciekly': '👺',
    'wkurwi': '👺',
    'denerwuj': '👺',
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
    'pawel': 'exeos',
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
    'sie rozgrzac': 'witczak',
    'oczadly': 'tomek',
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
    'jak sie nauczyc grac w poe?': 'Polecam ten poradnik: https://www.poe-vault.com/guides/ultimate-beginners-comprehensive-guide',
    'w co gramy': 'Wykres dostępnych gier jest dostępny tu: https://docs.google.com/spreadsheets/d/1BefpD-0jU_2GDn-yyG8_-HUVYyUBxnoK86ntY4O6Uo4/edit#gid=0',
    'tata simulator': 'Link do pobrania tata simulator (działa tylko na windows): https://drive.google.com/drive/folders/1tQjZv3pjK8dkdnYODdlfq6dPs4nKYdkW?usp=sharing'
}

# Przechowuje polskie znaki oraz ich odpowiedniki aby móc je zamienić (Nie jestem pewny co do 'ó' może by to zmienić na 'o' zamiast?)
polskie_znaki = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ó': 'u',
    'ż': 'z',
    'ź': 'z',
    'ł': 'l',
    'ś': 's',
    'ń': 'n'
}

music_library = {
    'dajesz tensa':'rage.mp3',
    'dajesz powrót': 'powrót_krupiera.mp3',
    'dajesz special': 'senteran_special_20k_subów.mp4'
}

client = discord.Client()

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        filename = filename
        return filename



@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Stworzenie temp_content które zmienia content wiadomości na same małe znaki
    temp_content = message.content
    temp_content = temp_content.lower()
    # Stworzenie pustego content który bęzdie przechowywał string bez polskich znaków
    content = ""
    # Przechowuje czy znak został dodany jako przemieniony
    znak_dodany = False

    # Iteruje przez każdy znak z temp_content
    for char in temp_content:
        # Iteruje przez każdy znak w dzienniku polskie_znaki
        for znak in polskie_znaki:
            # Jeżeli aktualny znak z dzienniku jest równy char z contentu wiadomości to go zamieniamy
            if znak == char:
                content = content + polskie_znaki[znak]
                # Skoro został dodany znak to znak_dodany = True, aby na przykład nie zmienić 'ą' na 'a' i potem też dodać 'ą'
                znak_dodany = True
        # Jeżeli char z contentu nie został znaleziony w dzienniku to normalny znak zostaje dodany do content
        if not znak_dodany:
            content = content + char
        # Na końcu trzeba powrócić znak_dodany do False aby w następnej iteracji głównego for wszystko działało poprawnie
        znak_dodany = False

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
    # Granie muzyki
    for element in music_library:
        if element in content:
            channel = message.author.voice.channel
            try:
                await channel.connect()
            except:
                pass
            filename = 'src/' + music_library[element]
            server = message.guild
            voice_client = server.voice_client
            voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
            await message.channel.send('Currently playing: ' + music_library[element])
        
    # Granie muzyki los santos
    if 'erty zagraj ' in message.content:
        server = message.guild
        voice_client = server.voice_client

        text = message.content
        url = text.removeprefix('erty zagraj')
        filename = await YTDLSource.from_url(url, loop=True)
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(executable='data/ffmpeg.exe', source=filename))
        await message.channel.send('**Now playing:** {}'.format(filename))

        # remove_song jest dopiero tu, ponieważ musi się stać po voice_client.stop() aby nie próbować usunąć pliku w użyciu oraz ponieważ jak było tuż po nim to czasami nie działało
        # sensowną opcją jest więc danie go tu ponieważ jest po await send czyli minie chwila i plik powinien mieć wystarczająco czasu aby przestać być zablokowanym
        remove_song()
        write_song_filename(filename)
        

    # send messages
    for element in send_library:
        if element in content:
            await message.channel.send(send_library[element])

    # Wyświetlenie liczby reakcji
    if 'ile reakcji' in content:
        file = open('data/reactions.txt', 'r')
        reactions = file.read()
        await message.reply('Już zareagowałem: ' + reactions + ' razy!')
    
    # Wchodzenie na kanał
    if 'erty wejdz' in content:
        channel = message.author.voice.channel
        await channel.connect()

    # Wychodzenie z kanału
    if 'erty wyjdz' in content:
        await message.add_reaction('👋')
        await message.guild.voice_client.disconnect()
    
    # Stop muzyki
    if 'erty stop' in content:
        await message.add_reaction('🛑')
        message.guild.voice_client.stop()
    
    # Pauza muzyki
    if 'erty pauza' in content:
        await message.add_reaction('⏸')
        message.guild.voice_client.pause()
    
    # Wstrzymanie muzyki
    if 'erty wznuw' in content:
        await message.add_reaction('⏯')
        message.guild.voice_client.resume()
    
    # Ręczna odpowiedź
    if 'czesc emojimeister!' in content:
        response = input('Input the response to ' + message.content + ': ')
        await message.reply(response)

    # los santos customs (ultra customowe rzeczy)
    # Witczak combinations for ending the call
    if 'witczak' in content or ('spotkanie' in content and ('zakonczyl' in content or 'zamknal' in content)):
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)

    # Two reactions for 'tomek'
    if 'tomek' in content:
        emoji = get(client.emojis, name='tomek')
        await message.add_reaction(emoji)
        emoji = get(client.emojis, name='witczak')
        await message.add_reaction(emoji)

# Usuwa piosenke aktualnie zapisaną w pliku data/song.txt
def remove_song():
    file = open('data/song.txt', 'r')
    filename = file.read()
    file.close
    if not (filename == ''):
        remove(filename)
        file = open('data/song.txt', 'w')
        file.write('')
        file.close

# Dodaje ścieżkę danej piosenki do pliko data/song.txt
def write_song_filename(filename):
    file = open('data/song.txt', 'w')
    file.write(filename)
    file.close

# Dodaje 1 do pliku data/reactions.txt
def reaction():
    file = open('data/reactions.txt', 'r')
    reactions = int(file.read())
    reactions = reactions + 1
    file.close()
    file = open('data/reactions.txt', 'w')
    file.write(str(reactions))
    file.close()


client.run('ODMyMjIzNDczOTk2MTM2NDU5.YHgqgg.KDDH0Nlre0nunCwPdu-TlinpPPw')
