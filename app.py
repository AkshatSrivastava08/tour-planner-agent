import streamlit as st
import os
import sys
from dotenv import load_dotenv
import time

# Ensure proper path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_ops_assistant.agents.planner import PlannerAgent
from ai_ops_assistant.agents.executor import ExecutorAgent
from ai_ops_assistant.agents.verifier import VerifierAgent

load_dotenv()

st.set_page_config(page_title="Tour Planner Agent", page_icon="✈️", layout="wide")

st.title("✈️ AI Tour Planner Agent")
st.markdown("Enter your travel request below, and the AI agents will plan, execute, and verify your itinerary.")

query = st.text_input("Where do you want to go?", "Plan a 3-day trip to Tokyo involving culture and food.")

if st.button("Generate Plan"):
    if not query:
        st.warning("Please enter a query first.")
    else:
        status_container = st.container()
        
        with status_container:
            # Planner
            with st.status("🧠 Planner Agent is working...", expanded=True) as status:
                st.write("Initializing Planner...")
                planner = PlannerAgent()
                plan = planner.create_plan(query)
                
                if plan:
                    st.write("✅ Plan created successfully!")
                    st.json(plan)
                    status.update(label="Planner Agent Complete", state="complete", expanded=False)
                else:
                    st.error("❌ Failed to generate plan.")
                    status.update(label="Planner Agent Failed", state="error")
                    st.stop()

            # Executor
            execution_results = []
            with st.status("⚙️ Executor Agent is working...", expanded=True) as status:
                st.write("Initializing Executor...")
                executor = ExecutorAgent()
                
                # We can iterate manually here to show progress if we modify execute_plan, 
                # but for now we'll just run it.
                st.write("Executing steps...")
                execution_results = executor.execute_plan(plan)
                
                st.write("✅ Execution complete!")
                for res in execution_results:
                     with st.expander(f"Step {res['step_id']}: {res['instruction']}"):
                        st.write(f"**Tool:** {res.get('tool', 'N/A')}") # Executor output schema might need tweak to include tool name in output if not there
                        st.json(res['output'])

                status.update(label="Executor Agent Complete", state="complete", expanded=False)

            # Verifier
            with st.status("🧐 Verifier Agent is working...", expanded=True) as status:
                st.write("Verifying and formatting...")
                verifier = VerifierAgent()
                final_response = verifier.verify_and_format(query, execution_results)
                status.update(label="Verification Complete", state="complete", expanded=False)
                st.write("✅verified")

        st.divider()
        st.subheader("🎉 Final Itinerary")
        st.markdown(final_response)
