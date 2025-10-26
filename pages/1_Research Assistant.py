import pandas as pd
import streamlit as st
import os
import uuid
from dotenv import find_dotenv, load_dotenv
from agents.planner_agent import planner_agent
from agents.research_agent import research_agent
from agents.writer_agent import writer_agent
from agents.editor_agent import editor_agent
from agents.execution_agent import executor_agent
import agents  # Import the package to access set_client
from openai import OpenAI
from datetime import datetime
import re
from IPython.display import Markdown, display
import time
import streamlit.components.v1 as components

# Load environment variables
load_dotenv(find_dotenv())

def init_chatbot():

    if "client" not in st.session_state:
        st.session_state.client = OpenAI()
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4o-mini"
    if "page" not in st.session_state:
        st.session_state.page = "researcher"
        # Set the client globally for all agents
        # agents.set_client(st.session_state.client)
    st.session_state.page = "researcher"


def scroll_to_element(element_id):
    """Scroll to a specific element by ID"""
    components.html(
        f"""
        <script>
            const element = window.parent.document.getElementById('{element_id}');
            if (element) {{
                element.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }}
        </script>
        """,
        height=0,
    )

def main():
    init_chatbot()
    st.markdown("<h1 style='text-align: center;'>✍️ Research Assistant 📓</h1>", 
            unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>An AI agent that conducts research and generates reports.</h4>",
                unsafe_allow_html=True)
    st.info("Typical workflow takes 2-3 minutes.")
    topic = st.text_input("Enter your research topic", key="research_topic")
    if topic:
        start_time = time.time()
        with st.spinner("Planning tasks...", show_time=True):
            steps = planner_agent(topic, page=st.session_state.page)
        executor_history, total_used_token = executor_agent(steps, page=st.session_state.page)
        st.session_state.expanders.write(f"Total Tokens Used: {total_used_token}")
        elapsed_time = time.time() - start_time
        st.session_state.expanders.write(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        st.markdown('<div id="report"></div>', unsafe_allow_html=True)
        st.container(border=True).markdown(executor_history[-1][-1].strip("`"))
        scroll_to_element("report")
        # Sidebar footer - GitHub link at bottom
    st.sidebar.markdown(
        """
        <div class='sidebar-footer'>
            <a href='https://github.com/palscruz23/agentic-workflows' target='_blank' style='text-decoration: none;'>
                💻 GitHub Repository
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()

