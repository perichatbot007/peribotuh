# chatbot.py

import os
import re
import spacy
import requests
import datetime
import PyPDF2
import wikipedia
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 🔄 Load environment variables
load_dotenv()

class Chatbot:
    def __init__(self):
        """Initialize the chatbot components."""
        self.nlp = spacy.load("en_core_web_sm", disable=["parser"])
        self.model = SentenceTransformer("BAAI/bge-large-en")
        self.chat_history = []

    def clean_text(self, text):
        """Clean and preprocess user input text."""
        doc = self.nlp(str(text))
        return ' '.join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)

    def get_response(self, user_input):
        """Get the chatbot's response based on user input."""
        if not user_input.strip():
            return "⚠ Please enter a valid question."

        # Step 1: Use internal tools or Groq API
        tool_response = self.detect_tool(user_input)
        if tool_response:
            return tool_response

        # Step 2: Fallback to Groq API
        return self.call_groq(user_input)

    def call_groq(self, user_input):
        """Call the Groq API to get a response."""
        print("🚀 Calling Groq API...")
        try:
            groq_api_key = os.environ.get("GROQ_API_KEY")
            if not groq_api_key:
                return "❌ Groq API key not set."

            self.chat_history.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": "You are a helpful assistant."}] + self.chat_history

            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": messages
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content'].strip()
                self.chat_history.append({"role": "assistant", "content": content})
                return content
            else:
                return f"⚠ Groq error {response.status_code}: {response.text}"
        except Exception as e:
            return f"❌ Failed to contact Groq: {e}"

    def get_weather(self, user_input):
        """Fetch weather information for a given location."""
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "❌ Weather API key not set."

        match = re.search(r"in\s+(.+)", user_input.lower())
        location = match.group(1).strip() if match else "Chennai"

        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': location, 'appid': api_key, 'units': 'metric'}

        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('cod') != 200:
                return f"⚠ Could not fetch weather: {data.get('message', '')}"
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"🌤 Weather in {location.title()}: {weather}, {temp}°C"
        except Exception as e:
            return f"❌ Error retrieving weather: {e}"

    def get_time(self):
        """Get the current date and time."""
        now = datetime.datetime.now()
        return f"🕒 Current time is: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    def wiki_search(self, user_input):
        """Fetch a summary from Wikipedia based on the user input."""
        topic = user_input.lower().replace("wikipedia", "").strip()
        if not topic:
            return "⚠ Please specify a topic to search on Wikipedia."

        try:
            summary = wikipedia.summary(topic, sentences=2)
            return f"📚 Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"⚠ Multiple topics found: {e.options[:3]}"
        except wikipedia.exceptions.PageError:
            return "⚠ Topic not found on Wikipedia."
        except Exception as e:
            return f"❌ Wikipedia error: {e}"

    def read_pdf(self, file_path):
        """Read and extract text from a provided PDF file path."""
        try:
            if not os.path.exists(file_path):
                return "⚠ PDF file not found."

            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            return text[:1000] + '...' if text else "⚠ No text found in PDF."
        except Exception as e:
            return f"❌ Failed to read PDF: {e}"

    def detect_tool(self, user_input):
        """Detect the tool (weather, time, Wikipedia, PDF reader) to use based on user input."""
        lower_input = user_input.lower()

        if "weather" in lower_input:
            return self.get_weather(user_input)
        elif "time" in lower_input or "date" in lower_input:
            return self.get_time()
        elif "wikipedia" in lower_input:
            return self.wiki_search(user_input)
        elif "read pdf" in lower_input:
            match = re.search(r"read pdf\s+(.*\.pdf)", lower_input)
            file_path = match.group(1).strip() if match else None
            if file_path:
                return self.read_pdf(file_path)
            else:
                return "⚠ Please specify a valid PDF file to read."
        return None

    def chat(self):
        """Start the chatbot in a simple command-line interface."""
        print("🤖 Hello! I am your chatbot. Type 'bye' to exit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == 'bye':
                print("Chatbot: Goodbye! 👋")
                break
            response = self.get_response(user_input)
            print(f"Chatbot: {response}")


if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()
