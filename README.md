# Pet-Health-Question-Answering-System

## 1. Overall Workflow
The system follows a synchronous, linear pipeline designed to ensure that every user input results in a structured, safe response.
* Input: The user provides a text query.
* Context Injection: The system retrieves the conversation history from the ChatMessageHistory buffer and injects it into the prompt.
* Prompt Construction: The ChatPromptTemplate combines the system instructions, the Pydantic formatting instructions, the chat history, and the new query.
* LLM Processing: The model (Gemini) analyzes the input. It is instructed to reason internally (explanation) before selecting a risk level and drafting a response.
* Structured Parsing: The PydanticOutputParser intercepts the LLM's string output and converts it into a Python object. If the LLM fails to provide valid JSON, a fallback error message is triggered.
* Response & Update: The advice and disclaimer are displayed to the user, and the response is appended to the message history for future context.

## 2. Role of Structured Logic vs. LLM
This system uses a Hybrid Architecture to balance the flexibility of generative AI with the reliability of traditional software.
| Component | Role | Why?|
| --------- | ---- | ---- |
| LLM (Gemini) | Semantic understanding and text generation. | Handles the infinite variety of ways users describe symptoms |
| Structured Logic (Pydantic) | Data validation and type enforcement. | Ensures the system always returns specific fields (risk_level, disclaimer) so the UI doesn't break. |

## 3. Guardrail Strategy
To prevent the AI from providing dangerous medical advice, several layers of guardrails are implemented:
* Risk Categorization: The LLM is forced to choose from a fixed list of risk levels. This allows developers to trigger UI alerts (like red text) for "Potentially Urgent" cases.
* Prompt Constraints: The system prompt explicitly forbids specific diagnoses or medication dosages.
* Mandatory Disclaimers: Every response object requires a disclaimer field, ensuring the user is always reminded that the AI is not a replacement for a veterinarian.
* Temperature Control: Setting temperature=0.1 minimizes "hallucinations" and ensures the assistant remains factual and consistent.

## 4. Assumptions and Limitations
* Assumptions:
  - The user is describing symptoms for a common domestic pet (dog/cat).
  - The user has stable internet access to reach the Gemini API.
* Limitations:
  - Latency: As a sequential chain, the response time depends on API speed.
  - Context Window: Using ChatMessageHistory without a "trimmer" means very long conversations could eventually exceed the model's token limit or increase costs.
  - No Physical Exam: The system cannot see, hear, or touch the pet, and thus can never replace professional triage.
