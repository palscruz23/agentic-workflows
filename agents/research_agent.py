import json
from datetime import datetime
from tools import research_tools
import streamlit as st  
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())
if "client" not in st.session_state:
    st.session_state.client = OpenAI()
# Global client - will be set by parent module
client = st.session_state.client

def research_agent(task: str, model: str = "gpt-5-mini", max_tool_call: int = 3):
    """
    Execute a research task using tools with aisuite (without manual loop).
    """
    print("==================================")
    print("🔍 Research Agent")
    print("==================================")
    tool_calls = 0
    prompt = f"""
You are a research assistant with 

Task:
{task}

Date today is {datetime.now().strftime('%Y-%m-%d')}
Limit tool calling into {max_tool_call} maximum.

"""
    def run_tool(name, args):
        if name == "arxiv_search_tool":
            return research_tools.arxiv_search_tool(**args)
        if name == "tavily_search_tool":
            return research_tools.tavily_search_tool(**args)
        if name == "wikipedia_search_tool":
            return research_tools.wikipedia_search_tool(**args)
        return {"error": f"Unknown tool: {name}"}

    messages = [
        {"role": "system", "content": """
            You are an expert researcher specialized in gathering academic or technical content. You have access to the following tools:
            - arxiv_tool: for finding academic papers
            - tavily_tool: for general web search
            - wikipedia_tool: for encyclopedic knowledge 
            ✅ Make the research concise.
            🚫 DO NOT provde recommendations for the next steps at the end. 
            🚫 DO NOT ask any questions on the next steps at the end.
            """},
        {"role": "user", "content":prompt.strip()}]
    tools = [research_tools.arxiv_tool_def, research_tools.tavily_tool_def, research_tools.wikipedia_tool_def]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        # messages.append(msg)
        kept = msg.tool_calls[:max_tool_call]
        sanitized_assistant = {
            "role": "assistant",
            "content": msg.content,
            "tool_calls": kept,
        }
        messages.append(sanitized_assistant)
        for call in msg.tool_calls:
            tool_calls += 1
            print(call.function.name, call.function.arguments)
            if tool_calls <= max_tool_call:
                result = run_tool(call.function.name, json.loads(call.function.arguments))
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": call.function.name,
                    "content": json.dumps(result)
                })
        if tool_calls > 3:
            messages.append({
                "role": "assistant",
                "content": "I have reached the maximum tool usage as instructed. ",
            })
            
        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
            reasoning_effort = "minimal"
        )
        
        content = final_response.choices[0].message.content
        print("✅ Output:\n", content)
        used_tokens = response.usage.total_tokens
        print("Used Tokens:\n", used_tokens)
        return content, used_tokens

    except Exception as e:
        print("❌ Error:", e)
        return f"[Model Error: {str(e)}]"
