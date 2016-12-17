import requests

rooms = requests.get('http://homes.e1.ru/kupit/rooms-1,2,3,4,5/?gorod=all&form=11102&zhilaya_novostrojki=1')

autos =  requests.get('https://auto.e1.ru/car/all/?federal_district[]=32334&price_currency=rur')

with open("rooms.html", "w") as rooms_file:
   rooms_file.write(rooms.content)

with open("autos.html", "w") as autos_file:
   autos_file.write(autos.content)
     
