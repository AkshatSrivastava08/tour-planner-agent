from .base_agent import BaseAgent
from ..tools.weather_tool import WeatherTool
from ..tools.serper_tool import SerperTool

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Executor")
        self.tools = {
            "WeatherTool": WeatherTool(),
            "SerperTool": SerperTool()
        }

    def execute_plan(self, plan: dict):
        self.log("Starting execution...")
        results = []
        
        if not plan or "steps" not in plan:
            self.log("Invalid plan structure.")
            return []

        for step in plan["steps"]:
            step_id = step.get("id")
            instruction = step.get("instruction")
            tool_name = step.get("tool")
            args = step.get("args", {})
            
            self.log(f"Step {step_id}: {instruction} (Tool: {tool_name})")
            
            tool = self.tools.get(tool_name)
            if tool:
                # Dynamically call the method based on tool type
                if tool_name == "WeatherTool":
                    output = tool.get_weather(**args)
                elif tool_name == "SerperTool":
                    output = tool.search(**args)
                else:
                    output = {"error": "Unknown tool method"}
            else:
                output = {"error": f"Tool {tool_name} not found"}
            
            results.append({
                "step_id": step_id,
                "instruction": instruction,
                "output": output
            })
            
        self.log("Execution complete.")
        return results
