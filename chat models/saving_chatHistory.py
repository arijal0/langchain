# Example Source: https://python.langchain.com/v0.2/docs/integrations/memory/google_firestore/

from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI

"""
Steps to replicate this example:
1. Create a Firebase account
2. Create a new Firebase project and FireStore Database
3. Retrieve the Project ID
4. Install the Google Cloud CLI on your computer
    - https://cloud.google.com/sdk/docs/install
    - Authenticate the Google Cloud CLI with your Google account
        - https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    - Set your default project to the new Firebase project you created
5. pip install langchain-google-firestore
6. Enable the Firestore API in the Google Cloud Console:
    - https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com&project=crewai-automation
"""

load_dotenv()


def credentials():
    query1 = input("Are you trying to retrieve the previous chat? choose: Y/N  ")
    while query1.lower() != "y" and query1.lower() != "n":
        query1 = input("I could not understand it! Are you trying to retrieve the previous chat? choose: Y/N")
    if query1.lower() == "y":
        # document name is equivalent to session in firebase database
        query2 = input("Do you want to add document to the previous collection? (Y/N) ")
        while query2.lower() != "y" and query2.lower() != "n":
            query2 = input("I could not understand it! Do you want to add document to the previous collection? (Y/N) ")
        if query2.lower() == "y":
            collection_id = input("Enter a collection id for which you are adding new document  ")
            session_id = input("Enter a new document id to add to this collection  ")
            
        else:
            collection_id = input("Enter a prior collection id for this chat  ") 
            session_id = input("Enter prior document id to create new collection  ")
            
    else:
        collection_id = input("Enter a new collection id for this chat Example: 'Math Problem chat'  ")
        session_id = input("Enter a new document id for this chat Example: 'Ankit Session'  ")
        
    return session_id, collection_id


  # Setup Firebase Firestore
PROJECT_ID = "langchain-db-c302d"

def chatViaFirebase(project_id):
    # Initialize Firestore Client
    print("Initializing Firestore Client...")
    client = firestore.Client(project=project_id)

    # Initialize Firestore Chat Message History
    print("Initializing Firestore Chat Message History...")

    SESSION_ID, COLLECTION_NAME = credentials()
    chat_history = FirestoreChatMessageHistory(session_id=SESSION_ID,
    collection=COLLECTION_NAME, client=client)

    print("Chat History Initialized.")
    print("Current Chat History:", chat_history.messages)

    # Initialize Chat Model
    model = ChatOpenAI()

    print("Start chatting with the AI. Type 'exit' to quit.")

    while True:
        human_input = input("User: ")
        if human_input.lower() == "exit":
            break

        chat_history.add_user_message(human_input)

        ai_response = model.invoke(chat_history.messages)
        chat_history.add_ai_message(ai_response.content)

        print(f"AI: {ai_response.content}")


chatViaFirebase(PROJECT_ID)





  

