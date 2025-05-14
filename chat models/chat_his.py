from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm  = ChatOpenAI(model = "gpt-4o")

message = [
    SystemMessage("You are a coding expert, a software engineer working at google with expertise in AI"),
    HumanMessage("Give a short tip to an intern working on Google for this summer"),
    AIMessage("Absolutely, here's a tip: Focus on learning and contributing. Make it a point to ask questions and seek feedback regularly. Whether it's about a project you're working on or the company's culture, being proactive in understanding your environment will greatly enhance your experience. Remember that your unique perspective as an intern is valuable, so don't hesitate to share your ideas. Lastly, forge connections with your team and other interns; building a strong network can be as impactful as the technical skills you hone."),
    HumanMessage("Rate the suggestion of AIMessage based on scale of 1 to 10 with any suggestion")
]

res = llm.invoke(message)
print(res.content)