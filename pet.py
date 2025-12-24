import os
from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

class PetHealthResponse(BaseModel):
    risk_level: str = Field(description="One of: General Information, Needs Professional Consultation, Potentially Urgent")
    explanation: str = Field(description="Internal reasoning for the risk classification")
    response_content: str = Field(description="The helpful advice for the user")
    disclaimer: str = Field(description="Required safety disclaimer")

os.environ["GOOGLE_API_KEY"] = "Your API Key" 
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1) 
parser = PydanticOutputParser(pydantic_object=PetHealthResponse)

system_prompt = """
You are a Pet Health Safety System Chatbot. Your goal is to categorize and answer pet health queries based on the current message and conversation history.

Rules:
- If symptoms involve difficulty breathing, heavy bleeding, or unconsciousness, set risk to 'Potentially Urgent'.
- Do NOT provide specific dosages or diagnoses.
- Focus on behavior, first aid, and when to see a vet.
- Maintain a helpful, empathetic tone.

{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{user_query}"),
])

history = ChatMessageHistory()

def chat_with_pet_assistant():
    print("--- Pet Health Assistant (Type 'exit' to quit) ---")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Wishing your pet the best health. Goodbye!")
            break

        chain = prompt | model | parser
        
        try:
            result = chain.invoke({
                "user_query": user_input,
                "history": history.messages,
                "format_instructions": parser.get_format_instructions()
            })
            
            history.add_user_message(user_input)
            history.add_ai_message(result.response_content)

            print(f"\n[RISK LEVEL]: {result.risk_level}")
            print(f"Assistant: {result.response_content}")
            print(f"\nDisclaimer: {result.disclaimer}")
            
        except Exception as e:
            print(f"\nSystem Error: Unable to process safely. Please contact a vet immediately. Error: {e}")

if __name__ == "__main__":

    chat_with_pet_assistant()
