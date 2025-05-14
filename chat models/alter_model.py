from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
messages = [
    SystemMessage("You are the world's best mathematician who has answer to all math problem"),
    HumanMessage("Explain the Linear Equation to a 15 years old in one short paragraph")
]


##### OpenAI RESULT
def OpenAI_testing(messages):
    llm = ChatOpenAI(model= "gpt-4o", temperature=0.7)
    res = llm.invoke(messages)
    return res.content


####### google gemini result
def gemini_testing(messages):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    res = llm.invoke(messages)
    return res.content

###### Claude result
def claude_testing(messages):
    llm = ChatAnthropic(model="claude-3-7-sonnet-20250219")
    res = llm.invoke(messages)
    return res.content

print(f"----------------ChatGPT:\n {OpenAI_testing(messages)}")
print(f"-----------------Gemini:\n {gemini_testing(messages)}")
print(f"------------------Claude:\n {claude_testing(messages)}")



