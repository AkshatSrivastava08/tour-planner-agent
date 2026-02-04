import argparse
import sys
from dotenv import load_dotenv

from ai_ops_assistant.agents.planner import PlannerAgent
from ai_ops_assistant.agents.executor import ExecutorAgent
from ai_ops_assistant.agents.verifier import VerifierAgent

load_dotenv()

# UTF-8 encoding for stdout to prevent Windows console errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="AI Operations Assistant - Tour Planner")
    parser.add_argument("--query", type=str, help="The travel plan query")
    args = parser.parse_args()

    if not args.query:
        print("Please provide a query using --query")
        return

    print(f"\n--- AI Operations Assistant ---\nQuery: {args.query}\n")

    # 1. Planner
    planner = PlannerAgent()
    plan = planner.create_plan(args.query)
    
    if not plan:
        print("Failed to create plan.")
        return

    print(f"\n[Plan Generated]:\n{plan}\n")

    # 2. Executor
    executor = ExecutorAgent()
    results = executor.execute_plan(plan)
    
    print(f"\n[Execution Log]:\n{results}\n")

    # 3. Verifier
    verifier = VerifierAgent()
    final_output = verifier.verify_and_format(args.query, results)

    print(f"\n[Final Response]:\n{final_output}\n")

if __name__ == "__main__":
    main()
