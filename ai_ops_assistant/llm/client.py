import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-4o")
        
        if not self.api_key:
            print("Warning: LLM_API_KEY not found in environment variables.")

    def chat_completion(self, messages, temperature=0.7, json_mode=False):
        """
        sends a chat completion request to the LLM provider.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

if __name__ == "__main__":
    # Test
    client = LLMClient()
    if client.api_key:
        print("Testing LLM connection...")
        response = client.chat_completion([{"role": "user", "content": "Hello!"}])
        print(f"Response: {response}")
    else:
        print("Skipping test, no API key.")
