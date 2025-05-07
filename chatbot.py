import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Check your .env file.")

def chat_with_groq(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot."},
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print("[HTTP Error]")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return "The chatbot service returned an HTTP error. Please try again later."
    except requests.exceptions.RequestException as req_err:
        print("[Request Error]")
        print(req_err)
        return "Unable to connect to the chatbot service. Please check your internet connection."
    except Exception as e:
        print("[Unexpected Error]")
        import traceback
        traceback.print_exc()
        return "An unexpected error occurred while processing your request."
