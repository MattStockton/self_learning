import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found.")

openai.api_key = OPENAI_API_KEY

def generate_subtopics(prompt: str) -> list:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        text_out = response["choices"][0]["message"]["content"].strip()
        subtopics = [s.strip() for s in text_out.split(",") if s.strip()]
        return subtopics
    except:
        return []

def generate_content(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"].strip()
    except:
        return "Error: No content generated."