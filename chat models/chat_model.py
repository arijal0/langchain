from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model= "gpt-4o", temperature=0.7)

res = llm.invoke("what is 2+2?")
print(res.content)

print("--------   function starts --------")

def get_my_gf_name():
    prompt = "I’ve been in a relationship for two years."
    "My girlfriend used to be very slim and calm, but recently "
    "she’s gained weight and gets frustrated with me over small things. Given this context, " 
    "suggest three funny and three cool pet names for her."
    llm = ChatOpenAI(model= "gpt-4o", temperature=0.7)

    res = llm.invoke(prompt)
    return res.content

print(get_my_gf_name())
    

