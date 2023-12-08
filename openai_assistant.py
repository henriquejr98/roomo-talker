import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from flask import jsonify, request, stream_with_context, Response
from hotels_offers import RommoOffers
import consts
import threading

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

users = {}
lock_geral = threading.Lock()
lock_by_number = {}


class RoomoAssistant:
    def __init__(self, assistant_id) -> None:
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id
        self.create_thread()
        self.user_phone = None
        self.offers = None
        self.room_offers = {}
        self.book = {}

    def create_thread(self):
        empty_thread = self.client.beta.threads.create()
        self.thread_id = empty_thread.id
        return empty_thread.id
    
    def delete_thread(self):
        response = self.client.beta.threads.delete(self.thread_id)
        return response.deleted

    def create_message(self, msg):
        message = self.client.beta.threads.messages.create(
            self.thread_id,
            role="user",
            content=msg,
        )
        return message.id

    def list_messages(self):
        messages = self.client.beta.threads.messages.list(self.thread_id)
        list_content = [message.content[0].text.value for message in messages.data]
        return list_content
    
    def talk(self, msg):
        self.create_message(msg)
        run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
                model="gpt-3.5-turbo-1106", # Sobrescreve gpt-4 da assistant,
        )
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run.id
            )
            # print(run.status)
            if run.status == "requires_action":
                my_args = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                called_function = run.required_action.submit_tool_outputs.tool_calls[0].function.name
                # print(called_function)
                tool_call_id = run.required_action.submit_tool_outputs.tool_calls[0].id

                run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": tool_call_id,
                        "output": getattr(self, called_function)(**my_args) if my_args else getattr(self, called_function)()
                    }
                    ]
                )
        messages = self.list_messages()
        return messages[0]

    def validate_dates(self, check_in, check_out):
        now = datetime.now()
        if len(check_in) == 5 or len(check_out) == 5:
            input_check_in = datetime.strptime(check_in, "%d/%m")
            input_check_out = datetime.strptime(check_out, "%d/%m")
            if input_check_in.month < now.month or (input_check_in.month == now.month and input_check_in.day < now.day):
                year = now.year + 1
            else:
                year = now.year
            formated_check_in = input_check_in.replace(year=year)

            if input_check_out.month < now.month or (input_check_out.month == now.month and input_check_out.day < now.day):
                year = now.year + 1
            else:
                year = now.year
            formated_check_out = input_check_out.replace(year=year)
        else:
            formated_check_in = datetime.strptime(check_in, "%d/%m/%Y")
            formated_check_out = datetime.strptime(check_out, "%d/%m/%Y")

        formated_now = now.strftime("%d-%m-%Y")
        if formated_check_in > now:
            if formated_check_out > now:
                if formated_check_out > formated_check_in:
                    self.book['check_in'] = formated_check_in.strftime("%Y-%m-%d")
                    self.book['check_out'] = formated_check_out.strftime("%Y-%m-%d")
                    self.book['num_nights'] = (formated_check_out - formated_check_in).days
                    return f'As datas de check-in e check-out são válidas. Serão {self.book["num_nights"]} diárias.'
                else:
                    return 'A data de check-out não pode ser menor que a data do check-in.'
            else:
                return f'A data de check-out não pode ser menor que a do dia de hoje ({formated_now})'
        else:
                return f'A data de check-in não pode ser menor que a do dia de hoje ({formated_now})'

    def get_current_date(self):
        now = datetime.now()
        formated_now = now.strftime("%d/%m/%Y")
        return formated_now
    
    def get_hotels_info(self, adults, children_ages, city):
        self.book['adults'] = adults
        self.book['children_ages'] = children_ages
        self.book['city'] = [consts.CITY_CODES[city], city]

        info = {
            'check_in': self.book['check_in'],
            'check_out': self.book['check_out'],
            'adults': adults,
            'children_age': children_ages,
            'city_code': consts.CITY_CODES[city]
            }
        self.offers = RommoOffers(info)
        try:
            self.offers.process_data()
            data = self.offers.lower_prices
            return str(data) if data else 'Não foram encontrados hotéis para essa data e local.'
        except KeyError:
            'Erro no servidor interno de consultas.'

    def get_hotel_info(self, hotel_name):
        self.book['hotel_name'] = hotel_name
        return self.offers.hotels[hotel_name]
    
    def get_rooms_info(self, hotel_name):
        rooms = self.offers.complete[hotel_name]['quartos']
        for room in rooms:
            self.room_offers[room['nome']] = {
                'min_price': min([fee['valorTotalComDesconto'] for fee in room['tarifas']]),
                'description': room['descricao'],
                'image': room['imagemPrincipal'],
            }

        formated = {k: f'R$ {v["min_price"]}.00' for k, v in self.room_offers.items()}

        return f'Nomes e valores dos quartos com desconto considerando as {self.book["num_nights"]} diárias.' + str(formated) 
        
    def get_room_info(self, room_name):
        self.book['room_name'] = room_name
        room_detail = {
            'Descrição' :self.room_offers[room_name]['description'],
            'Foto principal': self.room_offers[room_name]['image']
        }

        return str(room_detail)
    
    def summarize_booking(self, email):
        self.book['email'] = email

        formated = {
            'E-mail': self.book['email'],
            'Cidade': self.book['city'][1],
            'Nome do hotel': self.book['hotel_name'],
            'Nome do quarto': self.book['room_name'],
            'Data do check-in': self.book['check_in'],
            'Data do check-out': self.book['check_out'],
            'Quantidade de diárias': self.book['num_nights'],
            'Quantidade de adultos': self.book['adults'],
        }
        return str(formated)


def get_assistant(user_phone):
    with lock_geral:
        if user_phone not in users.keys():
            chain = RoomoAssistant('asst_qayuVh8i6bSMF0lYy1UxkBG6')
            users[user_phone] = chain
            print("New chain created.")
        else:
            chain = users[user_phone]
        return chain

def get_lock(user_phone: str):
    with lock_geral:
        if user_phone in lock_by_number:
            return lock_by_number[user_phone]
        else:
            lock_by_number[user_phone] = threading.Lock()
            return lock_by_number[user_phone]

def ask():
    data = request.get_json()
    user_phone = data.get('user_phone')
    user_input = data.get('user_input')

    if not user_phone:
        return jsonify({"error": "User number phone is required"}), 400

    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    chain = get_assistant(user_phone)

    lock = get_lock(user_phone)

    with lock:
        answer = chain.talk(user_input)
        response = {
            "answer": answer
        }

        data = json.dumps(response)
        return Response(stream_with_context(data), content_type='application/json')
    

if __name__ == "__main__":
    # roomo = RoomoAssistant('asst_dt5eWgjY8vQqz1Oo6skWvk3D')
    roomo = RoomoAssistant('asst_qayuVh8i6bSMF0lYy1UxkBG6')
    while True:
        try:
            msg = input('>> ')
            print(roomo.talk(msg))
            print()
        except KeyboardInterrupt or KeyError:
            print(roomo.book)
            break


