"""This module has all the dictionaries and lists
necessary fo the operation of the bot"""

OGOLNY_CHANNEL = 768865472552108115
MUSIQQO_CHANNEL = 768865735841546261
AGAR_AGAR_CHANNEL = 803636340369260544
STATUSERTY_CHANNEL = 952611789974151278
SHOTBOW_TRACKER_DISCORD_ID = 923253469597540402

sending_hours = [
    [7, 11],
    [12, 16],
    [17, 22]
]

emoji_library = {
    'haha': '😆',
    'kurwa': '🚫',
    'nie wiem': '🤷',
    'spi': '💤',
    'swiat': '🌍',
    'krupiergames.000webhostapp.com/ia': '🛑',
    'ee' : '🐚',
    'stundink': '🧑‍🎤',
    'studnik': '🧑‍🎤',
    'singer': '🧑‍🎤',
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
    'emojimeister': '🤚',
    '-p': '▶',
    '-leave': '👋',
    'stop': '🛑',
    'hej': '👋',
    'czesc': '👋',
    'siema': '👋',
    'hello': '👋',
    'halo': '👋',
    'penis':'🍆',
    'sentymi':'🥏',
    'rage': '👺',
    'wsciekly': '👺',
    'wkurwi': '👺',
    'denerwuj': '👺',
    'zly': '👺',
    'prosze': '🥺',
    'dziekuje': '❤',
    'fur': '😻',
    'spider': '🕷',
    'tok' : '🛠',
    'chemi' : '🏉',
    'biol' : '🍫',
    'geograf' : '🧱'
}

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
    'ekon': 'an',
    'oburz' : 'kfrankvegeta_disgusted',
    'hustawka' : 'senteran_fajrancik',
    'krzeslo' : 'senteran_monocle',
    'sus' : 'suserty',
    'sex' : 'sexeos',
    'fotel' : 'senteran_fotelteran',
    'emoji': 'emojimeister',
    'rafa': 'ertafa',
    'wolnik': 'erturnik',
    'erturnik': 'erturnik',
    'wonly': 'erturnik',
    'garbage': 'garbage_medal',
    'kn': 'kp',
    'pog': 'pogerty',
    'odpowiedz': 'pray_answer',
    'terror': 'senteran_terrorysta',
    'placz': 'smiling_pytel_with_tear',
    'ogien': 'strazertycy',
    'pali': 'strazertycy',
    'strazertycy': 'strazertycy',
    'tense': 'tense',
    'eindhoven' : 'tue_rejection',
    'delft' : 'tue_rejection',
    'holandia' : 'tue_rejection',
    'reject' : 'tue_rejection',
    'odrzut' : 'tue_rejection',
    'marius' : 'tue_rejection',
    'kucht' : 'tue_rejection',
    'sraker' : 'apetizer_sranie',
    'sranie' : 'apetizer_sranie',
    'natzi' : 'nahtzee',
    'nahtzee' : 'nahtzee',
    'yahtzee' : 'nahtzee',
    'chad_jan' : 'chad_jan',
    'chad_mariusz' : 'chad_mariusz',
    'matma' : 'witczak',
    'matemat' : 'witczak',
    'angielski' : 'kp',
    'fizyk' : 'js',
    'chad_sebek' : 'chad_sebek',
    'ib' : 'ibresults'
}

send_library = {
    'adres ip serwera': 'Adres ip serwera minecraft: 25.19.225.194',
    'login do hamachi': 'Login do hamachi: Senteran12345 (możliwe \
        także +6, + 7), hasło: senteran12',
    'ile masz lat': 'urodziłem się 15 kwietnia 2021!',
    'co potrafisz?': 'reagować na wiadomości!',
    'kiedy sie spotykamy': 'Ja mogę z wami zawsze być ♥',
    'jak sie nauczyc grac w poe?': 'Polecam ten poradnik: \
        https://www.poe-vault.com/guides/ultimate-beginners-comprehensive-guide',
    'w co gramy': 'Wykres dostępnych gier jest dostępny tu: \
        https://docs.google.com/spreadsheets/d/1BefpD-0jU_2GDn-yyG8_-HUVYyUBxnoK86ntY4O6Uo4/edit#gid=0',
    'gdzie jedziemy': 'Wykres dostępnych dat jest dostępny tu: \
        https://docs.google.com/spreadsheets/d/1BefpD-0jU_2GDn-yyG8_-HUVYyUBxnoK86ntY4O6Uo4/edit#gid=740564050',
    'cum trilogy': '-p welcome to the cumzone\n-p your cum wont last\n-p heir to the cum throne',
    'jak wielki jest penis seby?': '40 centymetrów flacid',
    'emoji sraker' : 'https://www.youtube.com/watch?v=eWb78tJtYRk'
}

music_library = {
    'dajesz tensa': 'rage.mp3',
    'dajesz powrot 1': 'powrót_krupiera.mp3',
    'dajesz special': 'senteran_special_20k_subów.mp4',
    'dajesz powrot 2': 'powrot_krupiera2.mp3',
    'dajesz powrot 3': 'Powrot_krupiera3.mp3'
}

krupier_users = {
    'Senteran' : 351780319306973194,
    'Krupier' : 443836613609390080,
    'Kato' : 181373861575524352,
    'ertymaster' : 521779771600797716,
    'exeos' : 329675010291662848,
    'KFrankVegeta' : 692034532966137886,
    'Lakey' : 249196779965251584,
    'Sebek' : 479613178272153600,
    'Kuchta' : 255768379200241665,
    'Hot Dog Nibba' : 511480754958630913,
    'Aleksandra Pawlik' : 692014502073466900,
    'Frido' : 253985014557966338
}

inverse_krupier_users = {
    351780319306973194 : 'Senteran',
    443836613609390080 : 'Krupier',
    181373861575524352 : 'Kato',
    521779771600797716 : 'ertymaster',
    329675010291662848 : 'exeos',
    692034532966137886 : 'KFrankVegeta',
    249196779965251584 : 'Lakey',
    479613178272153600 : 'Sebek',
    255768379200241665 : 'Kuchta',
    511480754958630913 : 'Hot Dog Nibba',
    692014502073466900 : 'Aleksandra Pawlik',
    253985014557966338 : 'Frido'
}

krupier_ids = [
    351780319306973194,
    443836613609390080,
    181373861575524352,
    521779771600797716,
    329675010291662848,
    692034532966137886,
    249196779965251584,
    479613178272153600,
    255768379200241665,
    511480754958630913,
    692014502073466900,
    253985014557966338
]

krupier_users_list = [
    'Senteran',
    'Krupier',
    'Kato',
    'ertymaster',
    'exeos',
    'KFrankVegeta',
    'Lakey',
    'Sebek',
    'Kuchta',
    'Hot Dog Nibba',
    'Aleksandra Pawlik',
    'Frido'
]

NAMES_J = [
    'Janek',
    'Jacek',
    'Jakub',
    'Jaroslaw',
    'Jakub'
]
NAMES_M = [
    'Mariusz',
    'Mikołaj'
]
NAMES_P = [
    'Piotr',
    'Paweł'
]
NAMES_S = [
    'Sebastian',
    'Sam'
]
NAMES_K = [
    'Kamil',
    'Krzysztof'
]
NAMES_A = [
    'Adam',
    'Alfons'
]
NAMES_KZ = [
    'Karolina',
    'Kaja'
]
NAMES_AZ = [
    'Aleksandra'
]
NAZWISKA_K = []
NAZWISKA_P = []
NAZWISKA_T = []
NAZWISKA_B = []
NAZWISKA_Z = []
NAZWISKA_R = []
NAZWISKA_W = []

nick_to_name_beginning_dictionary = {
    'Senteran': NAMES_J,
    'Krupier' : NAMES_J,
    'Kuchta' : NAMES_M,
    'Lakey' : NAMES_P,
    'Sebek' : NAMES_S,
    'Kato' : NAMES_K,
    'ertymaster' : NAMES_A,
    'exeos' : NAMES_P,
    'KFrankVegeta' : NAMES_KZ,
    'Hot Dog Nibba' : NAMES_A,
    'Aleksandra Pawlik' : NAMES_AZ,
    'Frido' : NAMES_P
}

nick_to_surname_dictionary = {
    'Senteran': NAZWISKA_K,
    'Krupier' : NAZWISKA_P,
    'Kuchta' : NAZWISKA_K,
    'Lakey' : NAZWISKA_P,
    'Sebek' : NAZWISKA_T,
    'Kato' : NAZWISKA_K,
    'ertymaster' : NAZWISKA_B,
    'exeos' : NAZWISKA_Z,
    'KFrankVegeta' : NAZWISKA_R,
    'Hot Dog Nibba' : NAZWISKA_W,
    'Aleksandra Pawlik' : NAZWISKA_P,
    'Frido' : NAZWISKA_K
}
names_today = {
    'Senteran': '',
    'Krupier' : '',
    'Kuchta' : '',
    'Lakey' : '',
    'Sebek' : '',
    'Kato' : '',
    'ertymaster' : '',
    'exeos' : '',
    'KFrankVegeta' : '',
    'Hot Dog Nibba' : '',
    'Aleksandra Pawlik' : '',
    'Frido' : ''
}

names_to_nick = {
    'Senteran': 'Senteran',
    'Krupier' : 'Krupier',
    'Kuchta' : 'Kuchta',
    'Lakey' : 'Lakey',
    'Sebek' : 'Sebek',
    'Kato' : 'Cumeel',
    'ertymaster' : 'ertymaster',
    'exeos' : 'Paweł Zając',
    'KFrankVegeta' : 'KFrankVegeta',
    'Hot Dog Nibba' : 'Hot Dog Nibba',
    'Aleksandra Pawlik' : 'Aleksandra Pawlik',
    'Frido' : 'Frido'
}

names_to_custom_nick = {
    'Senteran': 'じゃっく',
    'Krupier' : 'じょん',
    'Kuchta' : 'まりうす',
    'Lakey' : 'ぴーたー',
    'Sebek' : 'せばすちゃん',
    'Kato' : 'かみる',
    'ertymaster' : 'あだむ',
    'exeos' : 'ぽーる 野うさぎ',
    'KFrankVegeta' : 'かろりな',
    'Hot Dog Nibba' : 'あらん',
    'Aleksandra Pawlik' : 'あれくさんだー 収納すぺーす',
    'Frido' : 'ぽーる くりん'
}

image_search_params = {
    'q': '...',
    'num': 1,
    'safe': 'medium'
}

admin_ids = [
    443836613609390080,
    351780319306973194
]

nick_to_name = {
    'Senteran': 'Jacek',
    'Krupier' : 'Janek',
    'Kuchta' : 'Mariusz',
    'Lakey' : 'Piotrek',
    'Sebek' : 'Seba',
    'Kato' : 'Kamil',
    'ertymaster' : 'Adam',
    'exeos' : 'Paweł Z',
    'KFrankVegeta' : 'Karolina',
    'Hot Dog Nibba' : 'Alan',
    'Aleksandra Pawlik' : 'Ola',
    'Frido' : 'Paweł K'
}

voice_channels = [
    796011408931291179,
    824606836103708723,
    788012657437179908,
    788023076402495518,
    788718443708940340,
    793068340176355328,
    791066706218844161,
    837330961300979732,
    791389010538266625
]
