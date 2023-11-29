import requests

class RommoOffers:
    def __init__(self, info: dict) -> None:
        self.base_url = 'https://gateway.letsbook.com.br'
        self.path_url = f'/consulta-disponibilidade?checkin={info["check_in"]}&checkout={info["check_out"]}&numeroAdultos={info["adults"]}&criancas={info["children_age"]}&codigoCidade={info["city_code"]}&device=Desktop&idioma=pt-BR&moeda=BRL&emailHospede='
        self.headers = {
            'authority': 'gateway.letsbook.com.br',
            'method': 'GET',
            'path': self.path_url,
            'scheme': 'https',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Guidcarrinho': '104fb02e4eed4cfebb1a0bd40db102ce638344525891198711', # Atenção
            'Origem': 'Motor',
            'Origin': 'https://atlantica.letsbook.com.br',
            'Pragma': 'no-cache',
            'Referer': 'https://atlantica.letsbook.com.br/',
            'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'X-Api-Key': 'vMq2UPze2jUBm4ZYcp4zrzXmsdgnpxQ4YFRrFhoLCDtjw7uxhA9Gf3oXFaUd', # Atenção
        }
        self.available = {}
        self.hotels = {}
        self.lower_prices = {}
        self.complete = {}

    def make_request(self):
        r = requests.get(url=f'{self.base_url}{self.path_url}', headers=self.headers)
        data = r.json()
        return data

    def get_available_hotels(self, hotels):
        for hotel in hotels['hoteis']:
            self.hotels[hotel['nome']] = hotel['descricao']
            if hotel['quartos']:
                self.complete[hotel['nome']] = {
                    'descricao': hotel['descricao'],
                    'amenidades': hotel['amenidades'],
                    'politicas': hotel['politicas'],
                    'endereco': hotel['endereco'],
                    'telefone': hotel['telefone'],
                    'celular': hotel['celular'],
                    'email': hotel['email'],
                    'quartos': hotel['quartos'],
                    'formasPagamento': hotel['formasPagamento'],
                }
                for quarto in hotel['quartos']:
                    prices = [tarifa['valorMedioDiariaComDesconto'] for tarifa in quarto['tarifas']]
                    self.available[hotel['nome']] = {
                        quarto['nome']: {tarifa['nome']: tarifa['valorMedioDiariaComDesconto'] for tarifa in quarto['tarifas']},
                        'rooms_quantity': quarto['unidadesDisponiveis'],
                        'lowest_price': min(prices),
                        'all_prices': prices
                    }
        self.lower_prices = {hotel: f"A partir de R$ {info['lowest_price']} a diária" for hotel, info in self.available.items()}
        return {hotel: f"R$ {info['lowest_price']}" for hotel, info in self.available.items()}

    def process_data(self):
        hotels = self.make_request()
        result = self.get_available_hotels(hotels)
        return result


if __name__ == '__main__':

    info = {
    'check_in': '2023-12-20',
    'check_out': '2024-01-04',
    'adults': '2',
    'children_age': '',
    'city_code': 'BHZ'
    }

    roomo_hotels = RommoOffers(info)
    data = roomo_hotels.process_data()
    # print(roomo_hotels.available)
    # print()
    # print(roomo_hotels.lower_prices)

    tarifas = roomo_hotels.complete['Ramada Encore Minascasa Belo Horizonte']['quartos'][0]['tarifas']
    quartos = roomo_hotels.complete['Ramada Encore Minascasa Belo Horizonte']['quartos']
    ofertas = {}
    for quarto in quartos:
        ofertas[quarto['nome']] = min([tarifa['valorTotal'] for tarifa in quarto['tarifas']])


    room_offers = {}
    rooms = roomo_hotels.complete['Hilton Garden Inn Belo Horizonte Lourdes']['quartos']
    print(rooms[0]['imagemPrincipal'])
    # for room in rooms:
    #     room_offers[room['nome']] = min([fee['valorTotalComDesconto'] for fee in room['tarifas']])
    # formated = {f'Quarto {k}': f'Valor total com desconto R$ {v}' for k, v in room_offers.items()}

    # print(formated)