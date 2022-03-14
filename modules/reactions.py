import discord
from discord.utils import get

from functions import reaction


custom_emoji_library = {
    'erty': 'ertymaster',
    'adam': 'ertymaster',
    'bigas': 'ertymaster',
    'senteran': 'senteran',
    'jacek': 'senteran',
    'kulik': 'senteran',
    'jan': 'krupier',
    'pytel': 'krupier',
    'krup': 'krupier',
    'sebek': 'sebek',
    'seba': 'sebek',
    'timm': 'sebek',
    'exeos': 'exeos',
    'pawel': 'exeos',
    'mobil': 'exeos_mobile',
    'telefon': 'exeos_mobile',
    'zajac': 'exeos',
    'kato': 'kato',
    'kamil': 'kato',
    'kuchta': 'kuchta',
    'mariusz': 'kuchta',
    'lakey': 'lakey',
    'piotr': 'lakey',
    'praczyns': 'praczyns',
    'raczynski': 'praczyns',
    'alan': 'hot_dog_nibba',
    'frido': 'frido',
    'wf': 'tomek',
    'chad': 'chad',
    'fajran': 'fajrancik',
    'fajrancik': 'senteran_fajrancik',
    'wtf': 'wtf',
    'ertymi': 'ertymi',
    'ertymeister': 'ertymeister',
    'clyde': 'clyde',
    'cas': 'cas_francuski',
    'bw': 'bw',
    'js': 'js',
    'javascript': 'js',
    'auto': 'auto',
    'bmw': 'auto',
    'ford': 'auto',
    'skoda': 'auto',
    'karolina': 'kfrankvegeta',
    'kfrankvegeta': 'kfrankvegeta',
    'rys': 'kfrankvegeta',
    'wstret': 'kfrankvegeta_disgusted',
    'niesma': 'kfrankvegeta_disgusted',
    'ola': 'ap',
    'aleksandra': 'ap',
    'pawlik': 'ap',
    'benet': 'benet_rekord',
    'sie rozgrzac': 'witczak',
    'oczadly': 'tomek',
    'witczak': 'witczak',
    'bazyl': 'bazyl',
    'najman': 'najman',
    'mama': 'mama',
    'lis': 'lis',
    'fur': 'lis',
    'kp': 'kp',
    'an': 'an',
    'oburz' : 'kfrankvegeta_disgusted',
    'hustawka' : 'senteran_fajrancik',
    'krzeslo' : 'senteran_monocle',
    'sus' : 'suserty',
    'sex' : 'sexeos',
    'fotel' : 'senteran_fotelteran',
    'shrek' : 'shrerty'
}

reactions_starts = {
    'erturnik': '?erturnik', 
    'wolmy': '?erturnik',
    'garbage': '?garbage_medal',
    'terror': '?senteran_terrorysta',
    'placz': '?smiling_pytel_with_tear',
    'tense': '?tense',
    'strazert': '?strazertycy',
    'pali': '?strazertycy',
    'ogien': '?strazertycy',
    'odpowiedz': '?pray_answer',
    'haha': '😆',
    'spi': '💤',
    'ostr': '🌶',
    'xd': '😂',
    'kurde': '😯',
    'prosze': '🙏',
    'agar': '🔴',
    'fur' : '😻',
    'zly': '👺',
    'denerwuj': '👺',
    'wkurwi': '👺',
    'wsciekly': '👺',
    'penis':'🍆',
    'stop': '🛑'
}

reactions_ends = {
    'rafa': '?ertafa',
    'wolnik': 'erturnik',
    'rok' : '🪨'
}

reactions_contains = {
    'kp' : '?kp',
    'kn': '?kp',
    'kurwa': '🚫',
    '?': '🧐',
    'entj': '♑',
    'intj': '♑'
}

reactions_whole_word = {
    'emoji': '?emojimeister',
    'pog': '?pogerty',
    'swiat': '🌍',
    'krupiergames.000webhostapp.com/ia': '🛑',
    'tak': '✅',
    'nie': '❎',
    'ee' : '🐚',
    'stundink': '🧑‍🎤',
    'studnik': '🧑‍🎤',
    'singer': '🧑‍🎤',
    'spicy': '🌶',
    'bruh': '🦕',
    'ok': '👌',
    'angielski': '🐚',
    'emojimeister': '🤚',
    'kiedy': '❓',
    'spider' : '🕷️',
    'dziekuje' : '❤',
    'prosze': '🥺',
    'rage': '👺',
    'sentymi':'🥏',
    'halo': '👋',
    'hello': '👋',
    'siema': '👋',
    'czesc': '👋',
    'hej': '👋',
    '-leave': '👋',
    '-p': '▶',
    'dobra': '👌'
}

reaction_phrase = {
    'nie wiem': '🤷',
    'o co chodzi': '❓',
    'co sie dzieje': '❓',
    'co sie stalo': '❓'
}

async def react(message, content, client):
    for word in content:
        for element in reactions_starts:
            if word.startswith(element):
                react_with_emoji(message, reactions_starts[element], client)
        
        for element in reactions_ends:
            if word.endswith(element):
                react_with_emoji(message, reactions_starts[element], client)
        
        for element in reactions_contains:
            if element in word:
                react_with_emoji(message, reactions_contains[element], client)
        
        for element in reactions_whole_word:
            if word == element:
                react_with_emoji(message, reactions_whole_word[element], client)
    
    for element in reaction_phrase:
        if element in content:
            react_with_emoji(message, reaction_phrase[element], client)


async def react_with_emoji(message, emoji, client):
    if not emoji.startswith("?"):
        try:
            message.add_reaction(emoji)
            reaction()
        except Exception as e:
            print(f"Reaction failed {e} || {message} || {emoji}")
    else:
        emoji = emoji[1:]
        try:
            em = get(client.emojis, name=emoji)
            message.add_reaction(em)
            reaction()
        except Exception as e:
            print(f"Reaction failed, error: {e} || message: {message} || emoji: {emoji} || client: {client}")