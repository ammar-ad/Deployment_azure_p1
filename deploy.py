
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Azure AI Foundry details
ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
API_KEY = os.getenv("AZURE_AI_API_KEY")
DEPLOYMENT = os.getenv("AZURE_AI_DEPLOYMENT")

if not ENDPOINT or not API_KEY or not DEPLOYMENT:
    raise ValueError("Set all three Azure environment variables first.")

client = OpenAI(
    api_key=API_KEY,
    base_url=ENDPOINT.rstrip("/") + "/"
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful chatbot. Answer simply and clearly."
    }
]

print("Chatbot started! Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages
        )

        answer = response.choices[0].message.content
        print("\nChatbot:", answer, "\n")

        messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        messages.pop()
        print("Error:", e)
