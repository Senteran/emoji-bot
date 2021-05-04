import youtube_dl
import asyncio
import shutil
import discord

def to_en_str(pl_str):
    # Przechowuje polskie znaki oraz ich odpowiedniki aby móc je zamienić (Nie jestem pewny co do 'ó' może by to zmienić na 'o' zamiast?)
    polish_symbols = {
        'ą': 'a',
        'ć': 'c',
        'ę': 'e',
        'ó': 'o',
        'ż': 'z',
        'ź': 'z',
        'ł': 'l',
        'ś': 's',
        'ń': 'n'
    }
    
    # Stworzenie pustego en_str który bęzdie przechowywał string bez polskich znaków
    en_str = ""
    # Przechowuje czy znak został dodany jako przemieniony
    char_added = False

    # Celem tego całego bloku jest przejście przez każdy znak w message.content i zamienienie polskich znaków takich jak 'ą' i 'ć' na ich odpowiedniki, czyli w tym przypadku 'a' i 'c'
    # Jest to przydatne inaczej trzeba sprawdzać dwie opcje wiadomości na przykład 'zły' i 'zly', po zamianie natomiast trzeba sprawdzać tylko 'zly'
    # Iteruje przez każdy znak z pl_str
    for char in pl_str:
        # Iteruje przez każdy znak w dzienniku polskie_znaki
        for symbol in polish_symbols:
            # Jeżeli aktualny znak z dzienniku jest równy char z contentu wiadomości to go zamieniamy
            if symbol == char:
                en_str = en_str + polish_symbols[symbol]
                # Skoro został dodany znak to znak_dodany = True, aby na przykład nie zmienić 'ą' na 'a' i potem też dodać 'ą'
                char_added = True
        # Jeżeli char z contentu nie został znaleziony w dzienniku to normalny znak zostaje dodany do content
        if not char_added:
            en_str = en_str + char
        # Na końcu trzeba powrócić znak_dodany do False aby w następnej iteracji głównego for wszystko działało poprawnie
        char_added = False
    
    return en_str


async def yt_download(url, destination):
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
            shutil.move(filename, 'songs')
            filename = destination + filename
            return filename
    
    ret = await YTDLSource.from_url(url, loop=True)
    return ret

def word_triangle(message):
    string = ""
    prev = ""

    for char in message:
        prev += char
        if not char == ' ':
            string = string + "\n" + prev
    for char in message[:0:-1]:
        prev = prev.removesuffix(char)
        if not char == ' ':
            string = string + "\n" + prev
    return string
