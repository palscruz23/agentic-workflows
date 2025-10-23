# This file makes the agents directory a Python package

# # Global client instance that all agents can access
# client = None

# def set_client(openai_client):
#     """Set the OpenAI client for all agents to use."""
#     global client
#     client = openai_client

#     # Also set it in each agent module
#     from . import planner_agent, research_agent, editor_agent, execution_agent, writer_agent
#     planner_agent.client = openai_client
#     research_agent.client = openai_client
#     editor_agent.client = openai_client
#     execution_agent.client = openai_client
#     writer_agent.client = openai_client
