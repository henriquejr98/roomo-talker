import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from hotels_offers import RommoOffers
import consts

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


class RoomoAssistant:
    def __init__(self, assistant_id) -> None:
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id
        self.create_thread()

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
                # instructions = "" # Sobrescreve ao prompt da assistant
        )
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run.id
            )
            # print(run.status)
            if run.status == "requires_action":
                my_args = eval(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                called_function = run.required_action.submit_tool_outputs.tool_calls[0].function.name
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

    def get_current_time_and_date(self):
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")   

        return formatted_now
    
    def get_hotels_info(self, check_in, check_out, adults, children_ages, city):
        info = {
        'check_in': check_in,
        'check_out': check_out,
        'adults': adults,
        'children_age': children_ages,
        'city_code': consts.CITY_CODES[city]
        }
        offers = RommoOffers(info)
        data = offers.process_data()
        if data:
            return str(data)
        return 'Não foram encontrados hotéis para essa data e local.'

        

if __name__ == "__main__":
    # roomo = RoomoAssistant('asst_dt5eWgjY8vQqz1Oo6skWvk3D')
    roomo = RoomoAssistant('asst_qayuVh8i6bSMF0lYy1UxkBG6')
    while True:
        msg = input('>> ')
        print(roomo.talk(msg))
        print()


