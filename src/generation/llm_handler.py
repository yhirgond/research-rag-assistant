import os
from dotenv import load_dotenv
import httpx
from openai import OpenAI

load_dotenv()


class LLMHandler:
    def __init__(self, model="gpt-4o-mini", max_tokens=1000, temperature=0.2):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            http_client=httpx.Client()
        )

    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert research assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_with_history(self, prompt, history):
        try:
            messages = [{"role": "system", "content": "You are an expert research assistant."}]
            messages.extend(history)
            messages.append({"role": "user", "content": prompt})
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"