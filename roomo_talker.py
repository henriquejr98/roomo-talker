from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import json
import consts
import datetime
from dotenv import load_dotenv

class Roomo:
    def __init__(self, my_prompt, partial_variables={}) -> None:
        load_dotenv()
        self.llm = ChatOpenAI()
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(my_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ],
            partial_variables=partial_variables,
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.data = None


    def talk(self, query: str) -> str:
        conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            # verbose=True,
            memory=self.memory
        )
        ans = conversation({"question": query})
        return ans

    def parse_answer(self, answer):
        """Parse the answer for the first iteration."""
        if '{' in answer['text']:
            self.data = self.extract_json(answer['text'])
            return 'Muito obrigado! Aguarde um momento enquanto verifico a disponibilidade...'
        else:
            return answer['text']

    @staticmethod
    def extract_json(data: str):
        try:
            json_start = data.index('{')
            json_end = data.rindex('}') + 1
            json_str = data[json_start:json_end]
            json_data = json.loads(json_str)
            return json_data
        except ValueError:
            return None


if __name__ == "__main__":
    from hotels import RoomoHotels

    roomo_hotels = RoomoHotels()
    cities, codes = roomo_hotels.get_cities()

    partial_variables = {
                "date": lambda : datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "cities": lambda : cities
                }

    first_roomo_talker = Roomo(my_prompt=consts.PROMPT1, partial_variables=partial_variables)

    while True:
        print()
        query = input('>> ')
        ans = first_roomo_talker.talk(query)
        final_answer = first_roomo_talker.parse_answer(ans)
        print(final_answer)
        if 'Buscando reservas...' in final_answer:
            break

    print(first_roomo_talker.data)



