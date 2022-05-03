from bs4 import BeautifulSoup
import requests
import json

from dictionaries import krupier_users
from dictionaries import AGAR_AGAR_CHANNEL

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

people_to_notify = ['Krupier', 'Kuchta', 'Sebek']
links_xkom = ['https://www.x-kom.pl/p/468276-kierownica-logitech-g29-shifter-pc-ps3-ps4.html']
links_media_expert= []
links_komputronik = []
links_rtv = []
links_ole_ole= []
links_morele = []
links_media_markt = []


async def check_for_offers(client, force=False):
    f = open('data/offers.txt',mode='r+')
    all_old_prices = json.loads(f.read())
    updated_prices = []


    for link in links_xkom:
        r = requests.get(link, headers=headers)
        new_price = BeautifulSoup(r.content, "html.parser").find('meta', property="product:price:amount").attrs['content']
        old_price = next(filter(lambda item: item['id'] == link, all_old_prices))['price']
        if float(new_price) < float(old_price) or force:
            print(f'nizsza {link} {old_price} {new_price}')
            channel = await client.fetch_channel(AGAR_AGAR_CHANNEL)

            pings = ''
            for person in people_to_notify:
                id = krupier_users[person]
                pings += f'<@{id}> '

            message = ('TEST MESSAGE' if force else '') + pings + f' Price drop from {old_price} to {new_price} at {link}'
            await channel.send(message)

        updated_prices.append({'id':link,'price':new_price})


    f.truncate(0)
    f.write(json.dumps(updated_prices))
    f.close()