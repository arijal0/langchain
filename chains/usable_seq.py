# SMTP auth error this doesnot work still adding here will change in future
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
import os
import smtplib
from email.mime.text import MIMEText

# Load environment variables from .env
load_dotenv()

# --- Email Configuration ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_STR = os.getenv("SMTP_PORT")
SMTP_PORT = int(SMTP_PORT_STR) if SMTP_PORT_STR else 587 # Default to 587 if not set or invalid

# --- Email Sending Function ---
def send_email_with_joke(translated_joke_text: str) -> dict:
    subject = "Here's your Dad Joke!"
    body = f"Your translated dad joke is:\n\n{translated_joke_text}"


    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT]):
        status = "Email configuration is incomplete in .env file. Email not sent."
        print(status)
        return {"joke_sent": translated_joke_text, "email_status": status}

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        print(f"Attempting to send email to {RECEIVER_EMAIL} via {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        status = f"Email successfully sent to {RECEIVER_EMAIL}"
        print(status)
        return {"joke_sent": translated_joke_text, "email_status": status}
    except smtplib.SMTPAuthenticationError as e:
        status = f"SMTP Authentication Error: {e}. Check your SENDER_EMAIL/SENDER_PASSWORD and ensure 'less secure app access' is on or use an App Password for Gmail."
        print(status)
        return {"joke_sent": translated_joke_text, "email_status": status}
    except Exception as e:
        status = f"Failed to send email: {e}"
        print(status)
        return {"joke_sent": translated_joke_text, "email_status": status}
    
# Create a ChatOpenAI model

model = ChatOpenAI(model="gpt-4o")
output = StrOutputParser()

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

email_wrapper = RunnableLambda(send_email_with_joke)

transaltor_wrapper = RunnableLambda(lambda output:{"text":output,"language":"French"})

chain = (dad_joke_template
        | model | output
        | transaltor_wrapper
        | translate_content
        | model 
        |  output
        |  email_wrapper
        )
res = chain.invoke({"count":2, "topic":"Dad's daughter being delusional about her being financially independent"})

print(res)
