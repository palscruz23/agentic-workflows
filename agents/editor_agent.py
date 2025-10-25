import streamlit as st
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def editor_agent(task: str, model: str = "gpt-5-mini") -> str:
    """
    Executes editorial tasks such as reflection, critique, or revision.
    """
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()

    print("==================================")
    print("🧠 Editor Agent")
    print("==================================")
    messages = [
        {"role": "system", "content": "You are an editor agent. Your job is to reflect on, critique, or improve existing drafts. DO NOT provde recommendations for the next steps at the end. DO NOT ask any questions on the next steps at the end."},
        {"role": "user", "content": task}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    used_tokens = response.usage.total_tokens
    print("Used Tokens:\n", used_tokens)
    return response.choices[0].message.content, used_tokens

