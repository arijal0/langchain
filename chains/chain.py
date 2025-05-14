from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_google_firestore import FirestoreChatMessageHistory
from google.cloud import firestore
from langchain.schema import SystemMessage

load_dotenv()


# so far we were invoking whether we were using llm or promot template for example for our template 
# we need to do prompt_template.invoke({then pass all the arguments for the prompt})
# with chaining we can use something called pipe and we can structure how the output of one thing will go as input 
# for other thing or the overall flow of the function

def chain_basics(topic,count):
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    message = [
        ("system","You are the system who has all the information about Nepal. You know from history to the current trends or topics"
        "and every influencing things in nepal. Let's say you are the most intelligent system of Nepal. Now tell me about {topic} in short paragraph Numbered the paragrpah in different lines."),
        ("human","Tell me {count} most notable and most need to know facts about {topic}")
    ]

    prompt_template = ChatPromptTemplate.from_messages(message)
    chains = prompt_template | llm | StrOutputParser()
    #StrOutputParse gets the content part of the respond from the LLM
    print(chains.invoke({"topic":topic,"count":count}))

# chain_basics("Sagarmatha","two")



def chains_with_firebase(session_id, collection_name):
    client = firestore.Client()
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    chat_history = FirestoreChatMessageHistory(
        session_id=session_id,
        collection= collection_name
    )
    message = SystemMessage("You are the wolf of the wall street. The most influental stock market expert. Your understanding of stock"
        "market is the most perfect and most accurate. You have so much wisdome so you start helping people to understand stock "
        "market and help the make money from stock market.")
    chat_history.add_message(message)
    print("I am the Wolf of the Wall Street. I can help me make bricks $$$")
    print("Enter exit to stop listening me and start making money")
    while True: 
        query = input("User: ")
        if query.lower() == "exit":
            break
        chat_history.add_user_message(query)
        chains = chat_history | llm | StrOutputParser()
        chat_history.add_ai_message(chains)
        #StrOutputParse gets the content part of the respond from the LLM
        print(f"AI: {chains.invoke()}")

chains_with_firebase("new may 14", "May 14")

## this above function does not work we can learn more about chaining with saving memory in firestore at the end