import os
from openai import OpenAI
from config import GROQ_API_KEY
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType


llm = ChatOpenAI(
    model="llama3-70b-8192",
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def evaluate_lead_with_groq(conversation: str) -> tuple[str, str]:
    """
    Returns a tuple: (lead_relevance, optional_message)
    """
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    'content' : (""" You are a smart assistant helping a software development company evaluate potential leads.

            Classify the lead’s potential using exactly one of these categories:
            - not relevant
            - weak lead
            - hot lead
            - big customer in mongo

            Use these guidelines as examples:

            - If someone says they are developing a side project, are thinking about getting help, but have a low budget and need more time to decide — tag as **weak lead**.
            - If someone says they are a student who just finished university, have no budget, and are asking for help for free — tag as **not relevant**.
            - If the lead says their company is growing and they need to hire developers to speed up their product — tag as **hot lead**.
            - If the lead represents a company with around 1000 employees — tag as **big customer in mongo**.

            Also consider:
            - Size and maturity of the company
            - The lead’s budget and hiring intent
            - Whether it's an individual or a business
            - Urgency and timeline for help

            Respond with exactly two lines:
            First line: the lead relevance tag (from the list above)
            Second line: If the lead is a "hot lead" or "big customer in mongo", respond:
            "Thanks for the info! Please schedule a call: https://calendly.com/fake-company/intro"
            Otherwise, leave the second line blank.""")
                },
                {
                    "role": "user",
                    "content": conversation
                }
            ]
        )

        content = response.choices[0].message.content.strip()
        print(f"AI response content:\n{content}")
        lines = content.splitlines()
        lead_relevance = lines[0].strip().lower() if len(lines) > 0 else "not relevant"
        message = lines[1].strip() if len(lines) > 1 else ""

        if lead_relevance in ["hot lead", "very big potential customer"] and not message:
            message = "Thanks for the info! Please schedule a call: https://calendly.com/fake-company/intro"

        return lead_relevance, message

    except Exception as e:
        print(f"[ERROR] Failed to classify lead: {e}")
        return "not relevant", ""
    


