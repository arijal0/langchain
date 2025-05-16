from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

# Define prompt template for movie summary
summary_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a movie critic."),
        ("human", "Provide a brief summary of the movie {movie_name} while generating this summary mainly focus on two things that is plot and characters ."),
    ]
)

# Define plot analysis step
def analyze_plot(plot):
    plot_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a movie critic."),
            ("human", "Analyze the plot: {plot}. In two paragraph Generate it's strengths and weaknesses respectively and briefly explain each content?"),
        ]
    )
    return plot_template.format_prompt(plot=plot)

# Define character analysis step
def analyze_characters(characters):
    character_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a movie critic."),
            ("human", "Analyze the characters: {characters}. In two paragraph Generate it's strengths and weaknesses respectively and briefly explain each content?"),
        ]
    )
    return character_template.format_prompt(characters=characters)

# Combine analyses into a final verdict
def combine_verdicts(plot_analysis, character_analysis):
    return f"Plot Analysis:\n{plot_analysis}\n\nCharacter Analysis:\n{character_analysis}"

# Simplify branches with LCEL
plot_branch_chain = (
    RunnableLambda(lambda x: analyze_plot(x)) | model | StrOutputParser()
)

character_branch_chain = (
    RunnableLambda(lambda x: analyze_characters(x)) | model | StrOutputParser()
)

# Create the combined chain using LangChain Expression Language (LCEL)
chain = (
    summary_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"plot": plot_branch_chain, "characters": character_branch_chain})
    | RunnableLambda(lambda x: combine_verdicts(x["branches"]["plot"], x["branches"]["characters"]))
)

# Run the chain
result = chain.invoke({"movie_name": "Spiderman Acrross The SpiderVerse"})

print(result)