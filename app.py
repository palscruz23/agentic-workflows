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

# Load environment variables
load_dotenv(find_dotenv())

def init_chatbot():

    if "client" not in st.session_state:
        st.session_state.client = OpenAI()
        # Set the client globally for all agents
        # agents.set_client(st.session_state.client)


def main():
    init_chatbot()
    st.title("Research Assistant Agent")
    topic = st.text_input("Enter your research topic", key="research_topic")
    if topic:
        start_time = time.time()
        with st.spinner("Planning...", show_time=True):
            steps = planner_agent(topic)
        executor_history, total_used_token = executor_agent(steps)
        st.session_state.expanders.write(f"Total Used Tokens: {total_used_token}")
        elapsed_time = time.time() - start_time
        st.session_state.expanders.write(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        st.container(border=True).markdown(executor_history[-1][-1].strip("`"))
if __name__ == "__main__":
    st.session_state.num_chat_messages = 5
    main()