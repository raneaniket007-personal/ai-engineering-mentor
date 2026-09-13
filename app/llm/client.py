import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, user_message: str) -> str:
        interaction = self.client.interactions.create(
            model="gemini-3.8-flash",
            input=user_message,
            system_instruction=(
                """
                You are an AI Engineering Mentor.
                Your job is to teach AI engineering concepts clearly
                and practically. Adapt explanations to the learner's level.
                Prefer concrete examples and explain the reasoning behind
                architectural decisions.
                """
            ),  
        )

        return interaction.output_text or ""