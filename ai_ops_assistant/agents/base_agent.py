from ..llm.client import LLMClient

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.llm = LLMClient()

    def log(self, message: str):
        print(f"[{self.name}] {message}")
