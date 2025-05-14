from langchain_google_firestore import FirestoreChatMessageHistory
from google.cloud import firestore   # this package retreive the client id or project id from the environment
from dotenv import load_dotenv
load_dotenv()

client = firestore.Client() # retreiving the client id in client variable to pass it to the firechatmessagehistory


# additional we can add a function to choose between default environment project or different project easily

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

def chat_history():
    SESSION_ID, COLLECTION_NAME = credentials()
    chat_history = FirestoreChatMessageHistory(session_id=SESSION_ID,
    collection=COLLECTION_NAME, client=client)

    return chat_history

