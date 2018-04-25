import requests
import scrapy

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
}


rooms = requests.get('http://homes.e1.ru/kupit/rooms-1,2,3,4,5/?gorod=all&form=11102&zhilaya_novostrojki=1', headers=headers)

#autos =  requests.get('https://auto.e1.ru/car/all/?federal_district[]=32334&price_currency=rur', headers=headers)

with open("rooms.html", "w") as rooms_file:
   rooms_file.write(rooms.content)

#with open("autos.html", "w") as autos_file:
#   autos_file.write(autos.content)

#response = requests.get(url, headers=headers)     
