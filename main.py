from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

print('''
 ---------------------------------------------------------------------
|       Здрвствуйте, это парсер ваших покупок на алиэкспресс!         |
| Итак, для начала введите название товара который желаете приобрести |
 ---------------------------------------------------------------------''')

search = input('Название товара: ').replace(' ', '+')
url = f'https://aliexpress.ru/wholesale?SearchText={search}'
html = urlopen(url)
bs = BeautifulSoup(html, features="lxml")

items = bs.find('div', {'class': re.compile(r'product-snippet_ProductSnippet__grid__......')}).find_all('div', {
    'class': re.compile(r'product-snippet_ProductSnippet__content__......')})

import csv

with open('aliexpress.csv', 'w') as file:
    writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(('Name', 'Price', 'Rating', 'Times bought', 'Store'))
    for item in items:
        try:
            name = item.find('div', {'class': re.compile(r'product-snippet_ProductSnippet__name__......')}).text
            if len(name) > 20:
                name = name[:20] + '...'
            price = item.find('div', {'class': re.compile(r'snow-price_SnowPrice__mainM__......')}).text
            rating = item.find('div', {'class': re.compile(r'product-snippet_ProductSnippet__score__......')}).text
            timesBought = item.find('div',
                                    {'class': re.compile(r'product-snippet_ProductSnippet__sold__......')}).text
            store = item.find('div', {'class': re.compile(r'product-snippet_ProductSnippet__caption__......')}).text

            writer.writerow((name, price, rating, timesBought, store))
        except:
            pass
    print('Ура! Все получилось! Смотрите список товаров в файле "aliexpress.csv"')
