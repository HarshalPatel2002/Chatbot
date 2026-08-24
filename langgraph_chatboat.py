from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage

from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langgraph.checkpoint.memory import InMemorySaver

from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

HF_TOKEN = st.secrets["HF_TOKEN"]

llm = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen3.8-27B',
    task='text-generation',
    huggingfacehub_api_token=HF_TOKEN,
    max_new_tokens=100
)


model=ChatHuggingFace(llm=llm)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


def chat_node(state:ChatState):

    messages=state['messages']
    response=model.invoke(messages)

    return {'messages': messages + [response]}


checkpointer=InMemorySaver()

graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)

# initial_state={
#     'messages':[HumanMessage(content='what is the capital of india')]
# }

# chatbot.invoke(initial_state)

# print(initial_state)

# while True:

#     user_message = input('type here: ')
#     print('User :',user_message)

#     if user_message.strip().lower() in ['exit' , 'quit','bye']:
#         break

#     responce=chatbot.invoke({'messages':[HumanMessage(content=user_message)]})

#     print('AI',responce['messages'][-1].content)

