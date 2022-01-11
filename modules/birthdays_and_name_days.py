import datetime

from dictionaries import nick_to_name
from file_handler import get_value, store_value

birthdays = {
    '0201' : ['Kato'],
    '2903' : ['Lakey', 'Sebek'],
    '0104' : ['KFrankVegeta'],
    '2304' : ['Hot Dog Nibba'],
    '0205' : ['Senteran'],
    '1205' : ['Krupier'],
    '3110' : ['Aleksandra Pawlik'],
    '1812' : ['Exeos'],
    '2612' : ['ertymaster']
}

async def new_day(client):
    new_day_birthdays(client)
    new_day_name_days(client)

async def new_day_birthdays(client):
    now = datetime.datetime.now()
    if now.hour < 8:
        return
    
    date = f'{now.day}{now.month}'

    if date == get_value('last_checked_date'):
        return

    try:
        if birthdays[date] is not None:
            channel = client.fetch_channel(768865472552108115)
            print('asdsfvijzklmcx.,')
            # await channel.send(f'Wszystkiego najlepszego z okazji urodzin {nick_to_name[birthdays[date]]}!')
    except:
        pass
    store_value('last_checked_date', date)

async def new_day_name_days(client):
    pass