import streamlit as st
import firebase as f
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def streamlit_chatbot():
    st.title("LangChain Firebase Chatbot")
    
    # Initialize session state to store chat variables
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Firebase setup sidebar
    with st.sidebar:
        st.header("Firebase Setup")
        
        # Choose between new or existing chat
        retrieve_previous = st.radio(
            "Are you trying to retrieve a previous chat?",
            ('New Chat', 'Retrieve Previous Chat')
        )
        
        if retrieve_previous == 'Retrieve Previous Chat':
            add_to_previous = st.radio(
                "Do you want to add document to the previous collection?",
                ('Yes', 'No')
            )
            
            if add_to_previous == 'Yes':
                collection_id = st.text_input("Enter a collection id for which you are adding new document")
                session_id = st.text_input("Enter a new document id to add to this collection")
            else:
                collection_id = st.text_input("Enter a prior collection id for this chat")
                session_id = st.text_input("Enter prior document id to create new collection")
        else:
            collection_id = st.text_input("Enter a new collection id for this chat (Example: 'Math Problem chat')")
            session_id = st.text_input("Enter a new document id for this chat (Example: 'Ankit Session')")
        
        # Initialize button
        if st.button("Initialize Chat"):
            if collection_id and session_id:
                # Create FirestoreChatMessageHistory instance
                st.session_state.chat_history = f.FirestoreChatMessageHistory(
                    session_id=session_id,
                    collection=collection_id,
                    client=f.client
                )
                
                # Load existing messages if any
                if st.session_state.chat_history.messages:
                    st.session_state.messages = st.session_state.chat_history.messages
                
                st.success(f"Chat initialized with collection '{collection_id}' and session '{session_id}'")
            else:
                st.error("Please fill in both collection ID and session ID")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message.type):
            st.write(message.content)
    
    # Chat input
    if st.session_state.chat_history is not None:
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message to chat
            st.session_state.chat_history.add_user_message(user_input)
            st.session_state.messages = st.session_state.chat_history.messages
            
            # Display user message
            with st.chat_message("human"):
                st.write(user_input)
            
            # Get AI response
            with st.chat_message("ai"):
                with st.spinner("Thinking..."):
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
                    response = llm.invoke(st.session_state.messages)
                    st.write(response.content)
            
            # Add AI message to chat history
            st.session_state.chat_history.add_ai_message(response.content)
            st.session_state.messages = st.session_state.chat_history.messages
    else:
        st.info("Please initialize your chat in the sidebar first.")

if __name__ == "__main__":
    streamlit_chatbot()