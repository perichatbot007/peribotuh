import os
import re
import spacy
import requests
import wikipedia
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 🔄 Load environment variables
load_dotenv()

class Chatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm", disable=["parser"])
        self.model = SentenceTransformer("BAAI/bge-large-en")
        self.chat_history = []

    def clean_text(self, text):
        """Clean and preprocess text using SpaCy."""
        doc = self.nlp(str(text))
        return ' '.join(token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct)

    def get_response(self, user_input):
        """Handle standard or tool-based queries."""
        if not user_input.strip():
            return "⚠ Please enter a valid question."

        tool_response = self.detect_tool(user_input)
        if tool_response:
            return tool_response

        return self.call_groq(user_input)

    def call_groq(self, user_input):
        """Generate a response via the Groq API."""
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

    def wiki_search(self, topic):
        """Search and summarize a Wikipedia topic."""
        if not topic:
            return "⚠ Please specify a topic to search on Wikipedia."

        try:
            summary = wikipedia.summary(topic, sentences=2)
            return f"📚 Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"⚠ Multiple topics found. Did you mean: {', '.join(e.options[:3])}?"
        except wikipedia.exceptions.PageError:
            return "⚠ Topic not found on Wikipedia."
        except Exception as e:
            return f"❌ Wikipedia error: {e}"

    def detect_tool(self, user_input):
        """Check if a tool-based response is needed."""
        lower_input = user_input.lower()

        if "wikipedia" in lower_input:
            topic = lower_input.replace("wikipedia", "").strip()
            return self.wiki_search(topic)

        return None

    def chat(self):
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
