import firebase as f
import time
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat_history = f.chat_history()

def chatbot(chat):
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
    print("At any point to exit this please enter exit")
    while True:
        user_query = input("User: ")
        if user_query.lower() == "exit":
            break
        chat.add_user_message(user_query)
        AI = llm.invoke(chat.messages)
        chat.add_ai_message(AI.content)
        print(AI.content) 
chatbot(chat_history)

