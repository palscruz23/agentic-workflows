import streamlit as st
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def writer_agent(task: str, model: str = "gpt-5-mini") -> str:
    """
    Executes writing tasks, such as drafting, expanding, or summarizing text.
    """
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()

    print("==================================")
    print("✍️ Writer Agent")
    print("==================================")
    messages = [
        {"role": "system", "content": "You are a writing agent specialized in generating well-structured academic or technical content.  Report contents are recommended to be in paragraph form except for reference section. Reference shall have APA format citation with full links. DO NOT provide recommendations for the next steps at the end. DO NOT ask any questions on the next steps at the end."},
        {"role": "user", "content": task}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    used_tokens = response.usage.total_tokens
    print("Used Tokens:\n", used_tokens)
    return response.choices[0].message.content, used_tokens
