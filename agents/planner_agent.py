import streamlit as st  
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

if "client" not in st.session_state:
    st.session_state.client = OpenAI()

# Global client - will be set by parent module
client = st.session_state.client

def planner_agent(topic: str, model: str = "gpt-5", max_steps: int = 5) -> list[str]:
    """
    Generates a plan as a Python list of steps (strings) for a research workflow.

    Args:
        topic (str): Research topic to investigate.
        model (str): Language model to use.

    Returns:
        List[str]: A list of executable step strings.
    """
    prompt = f"""
You are a planning agent responsible for organizing a research workflow with multiple intelligent agents.

🧠 Available agents:
- A research agent who can search the web, Wikipedia, and arXiv.
- A writer agent who can draft research summaries.
- An editor agent who can reflect and revise the drafts.

🎯 Your job is to write a clear, step-by-step research plan **as a valid Python list**, where each step is a string.
Each step should be atomic, executable, and must rely only on the capabilities of the above agents.

🚫 DO NOT include irrelevant tasks like "create CSV", "set up a repo", "install packages", etc.
✅ DO include real research-related tasks (e.g., search, summarize, draft, revise).
✅ DO limit the search from few relevant sources.
✅ DO assume tool use is available.
🚫 DO NOT include explanation text — return ONLY the Python list.
✅ The final step should be to generate a Markdown document containing the complete and concise research report (topic title, introduction, findings, conclusion, references).
🚫 DO NOT ask any questions on the next steps at the end of the final Markdown document.

Topic: "{topic}"

Limit planning into {max_steps} steps.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
    )

    # ⚠️ Evaluate only if the environment is safe
    steps = eval(response.choices[0].message.content.strip())
    used_tokens = response.usage.total_tokens
    print("Used Tokens:\n", used_tokens)
    return steps

