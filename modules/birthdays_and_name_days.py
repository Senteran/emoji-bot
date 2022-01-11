import datetime

from dictionaries import nick_to_name

birthdays = {
    '0201' : ['Kato'],
    '2903' : ['Lakey', 'Sebek'],
    '0104' : ['KFrankVegeta'],
    '2304' : ['Hot Dog Nibba'],
    '0205' : ['Senteran'],
    '1205' : ['Krupier'],
    '1812' : ['Exeos'],
    '2612' : ['ertymaster']
}

async def new_day_birthdays(client):
    now = datetime.datetime.now()
    date = f'{now.day}{now.month}'
    try:
        if birthdays[date] is not None:
            channel = client.fetch_channel(768865472552108115)
            await channel.send(f'Wszystkiego najlepszego z okazji urodzin {nick_to_name[birthdays[date]]}!')
    except:
        pass