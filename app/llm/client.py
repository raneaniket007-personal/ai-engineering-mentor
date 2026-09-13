import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools.knowledge import search_knowledge

load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, user_message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                tools=[search_knowledge],
                system_instruction=(
                    "You are an AI Engineering Mentor. "
                    "Your job is to teach AI engineering concepts clearly "
                    "and practically. Adapt explanations to the learner's level. "
                    "Prefer concrete examples and explain the reasoning behind "
                    "architectural decisions."
                ),
            ),
        )

        return response.text or ""