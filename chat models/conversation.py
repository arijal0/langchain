from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
# chat history
chat_history = [
    SystemMessage("You are the most intelligent AI assistannt ever existed")
]

# main function for chatting
def ai_assitant(chat_history):
    while True:
        user  = input("you: ")
        if user.lower() == "exit":
            break 
        chat_history.append(HumanMessage(content = user))
        AI = llm.invoke(chat_history)
        chat_history.append(AIMessage(content = AI.content))
        print(f"ChatGpt: {AI.content}")
        

#calling function
ai_assitant(chat_history)
print("---- Message History ----")
print(chat_history)
