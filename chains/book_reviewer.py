from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env
load_dotenv()

def choose_model():
    user = input('Which model would you like to use? A: "Claude", C: "ChatGPT", G: "Gemini"')
    if user.upper() == "C":
        model = ChatOpenAI(model="gpt-4o")
        print(f"You are using: ChatGpt")
    elif user.upper() == "A":
        model = ChatAnthropic(model="claude-3-7-sonnet-20250219")  #sepcify model
        print(f"You are using: Claude")
    else:
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        print(f"You are using: Gemini")
    return model


# choose_model()   tested & working

def parallel_template():
    llm = choose_model()
    output = StrOutputParser()

    #first chains.invoke(dict) would pass to the first p=object in the chain
    book_summary= ChatPromptTemplate.from_messages([
        ("system","You are the world best book analyser and reviewer. You have all the information about any book anyone ask you for"
        "you know content of everybook exist in this world"),
        ("human","Can you get me the main thesis of book named {book}. Also gather the summary, mainplot and main character (if any exists) in this book")
    ])

    book = input("Enter a name of book for which you want to proceed with: ")

    def book_plot(summary):
        plot_template = ChatPromptTemplate.from_messages([
            ("system", "You can extract the book plot from the very to very small detail of the book. you are an expert"),
            ("human","Generate the breif plot of {summary} focusing on main theme")
        ])

        return plot_template.format_prompt(summary = summary)
    
    def main_character(summary):
        main_template = ChatPromptTemplate.from_messages([
            ("system", "You can extract the book character if any exists from the very to very small detail of the book. you are an expert"),
            ("human","Generate the breif introduction of characters and their part in this book of {summary} focusing on main theme")
        ])

        return main_template.format_prompt(summary = summary)

    plot_wrapper = RunnableLambda(lambda x: book_plot(x))
    main_char_wrapper = RunnableLambda(lambda x: main_character(x))  # we cconverted the output from the third
    #chain to an object

    plot_chain = plot_wrapper | llm | output
    main_char_chain = main_char_wrapper | llm | output
    # we can put wrappers togethet with the chains e.x
    #plot_chain = RunnableLambda(lambda x: book_plot(x)) | llm | output       -> like this

    def verdict_combiner(book_plot,book_char):
        print(f"Book Plot: \n{book_plot} \n Book_ character: \n{book_char}")
    
    #parallen chains has to be prompted and should be in chains individually
    chain = (
        book_summary
        | llm
        | output
        | RunnableParallel(branches = {"plot":plot_chain,"characters":main_char_chain})
        | RunnableLambda( lambda x: verdict_combiner(x["branches"]["plot"], x["branches"]["characters"]))
    )

    #output segment
    res = chain.invoke({"book":book})

    return res

print(parallel_template())