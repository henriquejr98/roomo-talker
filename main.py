from hotels import RoomoHotels
from roomo_talker import Roomo
from hotels_offers import RommoOffers, main
import consts
import datetime
import asyncio
from time import sleep

roomo_hotels = RoomoHotels()
cities, codes = roomo_hotels.get_cities()

first_variables = {
            "date": lambda : datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "cities": lambda : cities
            }

first_roomo_talker = Roomo(my_prompt=consts.PROMPT1, partial_variables=first_variables)

while True:
    print()
    query = input('>> ')
    ans = first_roomo_talker.talk(query)
    final_answer = first_roomo_talker.parse_answer(ans)
    print(final_answer)
    if 'Muito obrigado! Aguarde um momento enquanto verifico a disponibilidade...' in final_answer:
        break

first_data = first_roomo_talker.data
children = [str(child['age']) for child in first_data['children']]
# print(first_data)

info = {
    'check_in': first_data['check-in'],
    'check_out': first_data['check-out'],
    'adults': str(first_data['adults']),
    'children_age': ','.join(children),
    'city_code': codes[first_data['city']]
    }

available_rooms = asyncio.run(main(info))
second_variables = {
    "hotels": lambda : available_rooms
}

second_roomo_talker = Roomo(my_prompt=consts.PROMPT2, partial_variables=second_variables)
# print(available_rooms)
ans = second_roomo_talker.talk('Quais hoteis tem disponível?')
print(ans['text'])
while True:
    print()
    query = input('>> ')
    ans = second_roomo_talker.talk(query)
    print(ans['text'])