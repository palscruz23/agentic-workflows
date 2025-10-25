
import json
import re
from datetime import datetime
import streamlit as st
from .research_agent import research_agent
from .editor_agent import editor_agent
from .writer_agent import writer_agent
from .medical_agent import medical_agent
import time
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())


def agent_register(page):
    if page == "researcher":
        agent_registry = {
            "research_agent": research_agent,
            "editor_agent": editor_agent,
            "writer_agent": writer_agent,
        }
    elif page == "medical":
        agent_registry = {
            "medical_agent": medical_agent,
            "editor_agent": editor_agent,
            "writer_agent": writer_agent,
        }
    return agent_registry

def clean_json_block(raw: str) -> str:
    """
    Clean the contents of a JSON block that may come wrapped with Markdown backticks.
    """
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    return raw.strip()


def executor_agent(plan_steps: list[str], model: str = "gpt-5-mini", page: str = "researcher"):
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()

    history = []

    print("==================================")
    print("🎯 Execution Agent")
    print("==================================")
    if "steps" not in st.session_state:
        st.session_state.steps = [container1, container2, container3, container4, container5] = [None]*5
        st.session_state.expanders = st.expander("Agent Steps", expanded=True)

    total_used_token = 0
    with st.session_state.expanders:
        for i, step in enumerate(plan_steps):
            st.session_state.steps[i] = st.container(border=True)
            st.session_state.steps[i].write(f"Step {i+1}: {step}")
    
    for i, step in enumerate(plan_steps):
        agent_decision_prompt = f"""
        You are an execution manager for a multi-agent research team.
        
        Given the following instruction, identify which agent should perform it and extract the clean task.
        
        Return only a valid JSON object with two keys:
        - "agent": one of {list(agent_register(page).keys())}
        - "task": a string with the instruction that the agent should follow
        
        Only respond with a valid JSON object. Do not include explanations or markdown formatting.
        
        Instruction: "{step}"
        """
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": agent_decision_prompt}]
            )
        
        raw_content = response.choices[0].message.content
        cleaned_json = clean_json_block(raw_content)
        agent_info = json.loads(cleaned_json)
        
        agent_name = agent_info["agent"]
        task = agent_info["task"]

        context = "\n".join([
            f"Step {j+1} executed by {a}:\n{r}" 
            for j, (s, a, r) in enumerate(history)
        ])
        enriched_task = f"""You are {agent_name}.
        
        Here is the context of what has been done so far:
        {context}
        
        Your next task is:
        {task}
        """

        print(f"\n🛠️ Executing with agent: `{agent_name}` on task: {task}")
        agent_registry = agent_register(page)
        if agent_name in agent_registry:
            with st.session_state.steps[i]:
                start_time = time.time()
                with st.spinner(f"Executing... ", show_time=True):
                    output, used_token = agent_registry[agent_name](enriched_task, model=st.session_state.model)
                    history.append((step, agent_name, output))
                    total_used_token += used_token
                    print(f"✅ Agent Used Tokens:\n{used_token}")
                    elapsed_time = time.time() - start_time
                    print(f"✅ Elapsed Time: {elapsed_time:.2f} seconds")
                    st.success(f"✅ Completed with {used_token} token used in {elapsed_time:.2f} seconds!")
        else:
            with st.session_state.steps[i]:
                start_time = time.time()
                with st.spinner(f"Executing... ", show_time=True):
                    output, used_token = f"⚠️ Unknown agent: {agent_name}"
                    history.append((step, agent_name, output))
                    total_used_token += used_token
                    print(f"✅ Agent Used Tokens:\n{used_token}")
                    elapsed_time = time.time() - start_time
                    print(f"✅ Elapsed Time: {elapsed_time:.2f} seconds")
                    st.success(f"✅ Completed with {used_token} token used in {elapsed_time:.2f} seconds!")
            
    print(f"✅ Output:\n{output}")
    print(f"✅ Total Tokens Used:\n{total_used_token}")
        
    return history, total_used_token

