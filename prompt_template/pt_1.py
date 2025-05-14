from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

def get_jokes(joke_type, joke_topic, model_name = "gpt-4o"):
    # we can easily change the models
    llm = ChatOpenAI(model= model_name)

    # PART 1: Create a ChatPromptTemplate using a template string
    template = "Tell me a {type} joke about {topic} "

    #converting simple template to langchain understandable form
    prompt_template = ChatPromptTemplate.from_template(template)

    #here we are passing arguments to our template
    prompt = prompt_template.invoke({"type":joke_type,"topic": joke_topic})

    #generating result based on our completed prompt
    print("------prompt feeding to llm------")
    print(prompt)
    res = llm.invoke(prompt)
    print(res.content)

# get_jokes("dad","coding")




def generate_cold_emails(email_tone, company, position,skill,model_name="gpt-4o"):
    llm = ChatOpenAI(model= model_name)


    messages = [
        ("system", "you are profession cold email writer who gathers information about any company first and"
        " the help clients generate a highly concise and effective cold email that almost guarrantes the responds"
        " from the company. And after generating the email you will start talking with user"),
        ("human", "Generate a cold email being {email_tone} to the {company} asking for any {position} position availabe and mention the relevant {skills} I have.")
    ]

    
    
    while True:
        template = ChatPromptTemplate.from_messages(messages)
        prompt = template.invoke({"email_tone":email_tone,
                             "company":company,
                             "position":position,
                             "skills":skill})
        print("Enter exit to stop at any point")
        res = llm.invoke(prompt)
        print(f"LLM Speaking: {res.content}")
        query = input("User: ")
        if query.lower() == "exit":
            break
        messages.append(res.content)
        messages.append(HumanMessage(content = query))


    # print("-----Input Prompt------")
    # print(prompt)
    # res = llm.invoke(prompt)
    # print("----------------LLM Output------------------------")
    # print(res.content)

generate_cold_emails("enthusiastic","Google","software engineering","python,langchain,aws,docker,react,javascript,html,css")

# llm = ChatOpenAI(model="gpt-4o")  
# messages = [
#     ("system", "You are a comedian who tells jokes about {topic}."),
#     ("human", "Tell me {joke_count} jokes."),
# ]

# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
# result = llm.invoke(prompt)
# print(result.content)