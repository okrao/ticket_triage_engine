import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# 1. Define the exact structure the AI MUST return
class TicketTriage(BaseModel):
    category: str = Field(description="The main issue category: Billing, Technical Support, Account Access, or General Inquiry")
    priority: str = Field(description="Priority level: Low, Medium, High, or Critical")
    sentiment: str = Field(description="The customer's emotional state: Positive, Neutral, Frustrated, or Angry")
    department_routing: str = Field(description="Which team gets this ticket: Tier 1 Support, Advanced Tech (Tier 2), Billing Dept, or Retention")
    summary: str = Field(description="A 1-sentence concise summary of the customer's problem")

def get_client():
    load_dotenv()
    load_dotenv("../.env")
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if groq_key:
        return OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
    elif openai_key:
        return OpenAI(api_key=openai_key)
    raise ValueError("Set OPENAI_API_KEY or GROQ_API_KEY in the environment before running this script.")

if __name__ == "__main__":
    client = get_client()

    # 3. Simulate a messy customer email
    raw_customer_ticket = """
    Ticket #88492
    From: angry_customer99@email.com
    Message: I have been trying to log into my account for three days and it keeps saying my password is wrong. 
    I reset it twice and it STILL won't work. I have an automatic payment coming out tomorrow and if I get an 
    overdraft fee because I can't check my balance I am going to cancel my entire account. Fix this immediately!
    """

    print("Processing incoming customer ticket...")

    # 4. Prompt the model to extract and structure the data
    system_prompt = """You are an automated contact center triage system. 
    Analyze the incoming customer ticket and extract the exact information required.
    You must return the data in perfect JSON format matching the requested schema.
    Do not include any other conversational text."""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user", 
                "content": f"Extract the data for this ticket and return JSON matching this schema: {TicketTriage.model_json_schema()}\n\nTicket Text: {raw_customer_ticket}"
            }
        ],
        temperature=0.1
    )

    # 5. Parse and validate the output using Pydantic
    raw_json_response = completion.choices[0].message.content
    parsed_ticket = TicketTriage.model_validate_json(raw_json_response)

    print("\n--- TRIAGE COMPLETE: STRUCTURED ROUTING DATA ---")
    print(f"Category:   {parsed_ticket.category}")
    print(f"Priority:   {parsed_ticket.priority}")
    print(f"Sentiment:  {parsed_ticket.sentiment}")
    print(f"Routing to: {parsed_ticket.department_routing}")
    print(f"Summary:    {parsed_ticket.summary}")
    print("------------------------------------------------\n")

    print("Raw JSON Payload for Database:")
    print(raw_json_response)