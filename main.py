import os
from typing import Optional

from dotenv import load_dotenv
from google import genai

from utils.config import SYSTEM_PROMPT


class LLMClient:
    """Client for calling the Gemini API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client."""

        # Load environment variables
        load_dotenv()

        # Get API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Please configure it in your .env file."
            )

        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)

        # Store model name
        self.model = "gemini-2.5-flash"

    def call(self, user_query: str) -> str:
        """Call the LLM with the system prompt and user query."""

        try:
            # Format the prompt with the user query
            full_prompt = SYSTEM_PROMPT.format(
                user_query=user_query
            )

            # Call Gemini API
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )

            # Check whether response contains usable text
            response_text = response.text if response else None
            if not response_text or not response_text.strip():
                return "Sorry, I couldn't generate a response. Please try again."

            return response_text.strip()

        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"


class MenuAssistant:
    """Assistant that answers restaurant-related queries using an LLM."""

    def __init__(self):
        """Initialize the menu assistant."""

        load_dotenv()

        self.llm_client = LLMClient()

    def answer(self, query: str) -> str:
        """Answer a user's restaurant-related question."""

        # Validate query
        if not query or not query.strip():
            return "Please enter a valid question."

        try:
            return self.llm_client.call(query.strip())

        except Exception as e:
            return f"Unable to process your request: {str(e)}"


def main():
    test_queries = [
        "What should I order at Sakura Sushi?",
        "What's the best dish at Bella Pasta?",
        "Tell me a joke",
        "Where should I go for affordable vegan food?",
        "Suggest an Indian restaurant.",
    ]

    print("Restaurant Menu Assistant")
    print("=" * 40)

    assistant = MenuAssistant()

    for query in test_queries:
        print(f"\nQuery: {query}")

        result = assistant.answer(query)

        print(f"Response: {result}")
        print("-" * 40)


if __name__ == "__main__":
    main()
