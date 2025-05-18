from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableBranch
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env
load_dotenv()


#you can add a function to choose LLM but I am just going with gemini for this one. Why? Cause it's free duh.



def feedback_system():
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    user = input("We are very happy to have you as a loyal customer.\nPlease share your feedback with us: ")

    conditional_template = ChatPromptTemplate.from_messages([
        ("system","You are a great feedback receiver and you respond to the people's feedback for anything it does not mater what the feedback is about and "
        "your main work is focusing on rating the feedback Positive, Negative, Neutral, Escalated"),
        ("human","Here is the feedback: {feedback}. Flag this feedback as Positive, Negative, Neutral or Escalated")
    ])

    # Define prompt templates for different feedback types
    # I will improve these redundant feedback template in futuere :(
    positive_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "Generate a thank you note for this positive feedback: {feedback}."),
        ]
    )

    negative_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "Generate a response addressing this negative feedback: {feedback}."),
        ]
    )

    neutral_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "Generate a request for more details for this neutral feedback: {feedback}.",
            ),
        ]
    )

    escalate_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "Generate a message to escalate this feedback to a human agent: {feedback}.",
            ),
        ]
    )

    branches = RunnableBranch(
    (
        lambda x: "positive" in x,
        positive_feedback_template | model | StrOutputParser()  # Positive feedback chain
    ),
    (
        lambda x: "negative" in x,
        negative_feedback_template | model | StrOutputParser()  # Negative feedback chain
    ),
    (
        lambda x: "neutral" in x,
        neutral_feedback_template | model | StrOutputParser()  # Neutral feedback chain
    ),
    escalate_feedback_template | model | StrOutputParser()
    )

    chains = conditional_template | branches 
    res = chains.invoke({"feedback":user})
    return res

print(feedback_system())