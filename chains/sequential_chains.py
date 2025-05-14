from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

dad_joke_template = ChatPromptTemplate.from_messages(
    [
        ("system","You have understading of dad jokes and you are the most funny dad joke writer."),
        ("human","Generate {count} dad joke about {topic}")

    ]
)

translate_content = ChatPromptTemplate.from_messages(
    [
        ("system","You are a professional translator who can translate from english to any language exist in the world"),
        ("human","Now, Convert the {text} into {language} entirely while keeping the semanatic meaning of the text same and translated language should be in English dialects")
    ]
)

transaltor_wrapper = RunnableLambda(lambda output:{"text":output,"language":"Nepali"})

chain = dad_joke_template | model | StrOutputParser() | transaltor_wrapper | translate_content | model |  StrOutputParser()
res = chain.invoke({"count":2, "topic":"Dad's daughter being delusional about her being financially independent"})

print(res)

# this shows a simple chain now we can add the more to our chain let's say generating a joke in english that's what
# LLM does unless said explicitly to translate to other language now what we  can do is add to our chain a object/ function
# that will this for us 
# but now we have used stroutputparse that gives us just content and now the content is not the object to pass in our
# langchain execution layer. so, we use a runnable lambda to convert our output into a parsable object

# so runnablelambda is a wrapper for the langchain execution layer