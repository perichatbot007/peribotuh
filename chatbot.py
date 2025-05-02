import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def chat_with_groq(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192"
        "",  # ✅ Use supported model
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        print("Response content:", response.text)
        return "Error: Groq API returned an error."
    except Exception as e:
        print("General Exception:", e)
        return "Error: Something went wrong while calling Groq API."
