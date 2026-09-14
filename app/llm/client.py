from app.planning.models import Plan
import os
from typing import Any

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

    def generate_structured(
        self,
        prompt: str,
        response_schema: type[Plan],
    ) -> Plan:
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an AI Engineering Mentor. "
                    "Create clear, practical plans for accomplishing "
                    "complex engineering goals."
                ),
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return response.parsed

    def generate(
        self,
        contents: list[types.Content],
    ) -> types.GenerateContentResponse:
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[search_knowledge],
                system_instruction=(
                    "You are an AI Engineering Mentor. "
                    "Your job is to teach AI engineering concepts clearly "
                    "and practically. Adapt explanations to the learner's level. "
                    "Prefer concrete examples and explain the reasoning behind "
                    "architectural decisions."
                ),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            ),
        )

        return response