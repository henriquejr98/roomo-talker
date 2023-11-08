from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from pydantic import BaseModel
from typing import List, Dict, Any
from pprint import pprint
import consts_entity

llm = ChatOpenAI()

conversation = ConversationChain(
    llm=llm,
    # verbose=True,
    prompt=consts_entity.ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm)
)

try:
    while True:
        print()
        msg = input('>> ')
        print(conversation.predict(input=msg))
        data = conversation.memory.entity_store.store

except KeyboardInterrupt:
    keys = [k for k in data.keys()]
    print(keys)