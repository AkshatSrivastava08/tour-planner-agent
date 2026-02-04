from .base_agent import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__("Verifier")

    def verify_and_format(self, user_query: str, execution_results: list):
        self.log("Verifying results and formatting answer...")
        
        system_prompt = """
        You are a Verifier Agent. Your job is to take a user's original query and the results from an execution plan, and formulate a complete, well-structured, and helpful response.
        
        If the results are insufficient or contain errors, do your best to answer what you can, but mention the limitations.
        Synthesize the information into a cohesive guide/response.
        """
        
        # Convert results to string for prompt
        results_str = ""
        for res in execution_results:
            results_str += f"Step {res['step_id']}: {res['instruction']}\nOutput: {res['output']}\n---\n"
            
        user_prompt = f"User Query: {user_query}\n\nExecution Results:\n{results_str}\n\nProvide the final response."
        
        response = self.llm.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        if not response:
            return "Unable to verify and format response due to missing LLM configuration."
            
        self.log("Verification complete.")
        return response
