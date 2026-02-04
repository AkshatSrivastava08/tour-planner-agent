import json
from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner")

    def create_plan(self, user_query: str):
        self.log(f"Creating plan for: {user_query}")
        
        system_prompt = """
        You are a Planner Agent. Your goal is to break down a user's request into a series of actionable steps that can be performed by an Executor Agent using specific tools.
        
        Available Tools:
        1. WeatherTool: Fetch weather for a specific city. Args: {"city": "City Name"}
        2. SerperTool: Search the web for information (events, places, etc.). Args: {"query": "Search query"}
        
        Output format:
        You must output ONLY valid JSON.
        Structure:
        {
            "steps": [
                {
                    "id": 1,
                    "instruction": "Description of what to do",
                    "tool": "WeatherTool" or "SerperTool",
                    "args": {"arg_name": "arg_value"}
                }
            ]
        }
        """
        
        user_prompt = f"User Query: {user_query}\n\nGenerate the plan."
        
        response = self.llm.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            json_mode=True
        )

        if not response:
            self.log("No response from LLM (check API keys).")
            return None

        try:
            plan = json.loads(response)
            self.log("Plan created successfully.")
            return plan
        except json.JSONDecodeError:
            self.log("Failed to decode plan JSON.")
            return None
