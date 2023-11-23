import requests
from time import sleep
import asyncio
import aiohttp

class RoomoHotels:
    def __init__(self) -> None:
        self.headers = {
        'authority': 'gateway.letsbook.com.br',
        'method': 'GET',
        'path': '/destinos',
        'scheme': 'https',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Guidcarrinho': '',
        'Origem': 'Motor',
        'Origin': 'https://atlantica.letsbook.com.br',
        'Pragma': 'no-cache',
        'Referer': 'https://atlantica.letsbook.com.br/',
        'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-Api-Key': 'vMq2UPze2jUBm4ZYcp4zrzXmsdgnpxQ4YFRrFhoLCDtjw7uxhA9Gf3oXFaUd'
        }
        self.url = 'https://gateway.letsbook.com.br/destinos'

    def get_hotels(self):
        response = requests.get(url=self.url, headers=self.headers)
        hotels = response.json() # pip install brotli
        return hotels

    def get_cities(self):
        hotels = self.get_hotels()
        city_codes = {hotel['nomeCidade'].split('-')[0].strip(): hotel['codigoCidade'] for hotel in hotels}
        unique_cities = list(set(city_codes.keys()))
        return unique_cities, city_codes


if __name__ == "__main__":
    roomo_hotels = RoomoHotels()
    cities, codes = roomo_hotels.get_cities()
    # print(cities)
    print(codes)
