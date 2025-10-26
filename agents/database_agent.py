import streamlit as st
import sqlite3
import pandas as pd
from utils.database import create_tables, create_metadata, get_metaschema
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from typing import Tuple

# Load environment variables
load_dotenv(find_dotenv())

PATH = 'data/rca_data.db'

def evaluate_and_refine_sql(
    question: str,
    sql_query: str,
    df: pd.DataFrame,
    schema: str,
    model: str = "gpt-5",
    sql_error: Exception = None
) -> Tuple[str, str]:
    """
    Evaluates SQL query results and refines the query if needed to better answer the user's question.

    This function uses an LLM to review whether the SQL query output adequately addresses
    the user's original question. If improvements are needed, it generates a refined SQL query.

    Args:
        question (str): The original natural language question from the user.
        sql_query (str): The SQL query that was executed.
        df (pd.DataFrame): The resulting DataFrame from executing the SQL query.
        schema (str): The database schema information for reference.
        model (str, optional): The language model to use for evaluation. Defaults to "gpt-5".

    Returns:
        Tuple[str, str]: A tuple containing:
            - feedback (str): Brief evaluation and suggestions for improvement.
            - refined_sql (str): The improved SQL query, or the original if no changes needed.

    Note:
        If the LLM response is not valid JSON, the function falls back to returning
        the original SQL query with the raw response as feedback.
    """
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()

    prompt = f"""
You are an expert SQL reviewer specializing in query optimization and accuracy validation.

## CONTEXT
**User's Original Question:**
{question}

**Generated SQL Query:**
```sql
{sql_query}
```

**Query Results:**
{df.to_string(index=False)}

**Table Schema:**
{schema}

**SQL Error:**
{sql_error}

## YOUR TASK
Analyze whether the SQL query correctly and completely answers the user's question. Include other columns which may be relevant to the question. When aggregations are used, make sure there are no duplications in the RCA ID.

Step 1: Briefly evaluate if the SQL output answers the user's question. 
Step 2: If the SQL could be improved, provide a refined SQL query. If SQL Error is not None, rectify the issues in the refined query.
If the original SQL is already correct, return it unchanged.

## OUTPUT FORMAT
Return ONLY a valid JSON object with this exact structure:
{{
    "feedback": "Brief evaluation of the query (what's right or what needs improvement)",
    "refined_sql": "The final SQL query to execute (original or improved version)"
}}

Do not include any text outside the JSON object.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    content = response.choices[0].message.content

    # Strip markdown code blocks and fix Python-style booleans
    content_clean = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    content_clean = content_clean.replace(": True", ": true").replace(": False", ": false")

    try:
        obj = json.loads(content_clean)
        feedback = str(obj.get("feedback", "")).strip()
        refined_sql = str(obj.get("refined_sql", sql_query)).strip()
        if not refined_sql:
            refined_sql = sql_query
    except Exception as e:
        # Fallback if the model does not return valid JSON:
        # use the raw content as feedback and keep the original SQL
        print(f"❌ JSON parsing error in evaluate_and_refine_sql: {e}")
        print(f"Raw response: {content}")
        feedback = content.strip()
        refined_sql = sql_query

    return feedback, refined_sql

def database_interpreter(query: str, sql_gen_ref: pd.DataFrame, metadata: str, model: str = "gpt-5") -> Tuple[str, bool]:
    """
    Converts SQL query results into a natural language answer for the user's question.

    This function takes the raw database query results and translates them into a clear,
    human-readable response that directly answers the user's original question.

    Args:
        query (str): The original natural language question from the user.
        sql_gen_ref (pd.DataFrame): The DataFrame containing the SQL query results.
        metadata (str): The database schema metadata for context.
        model (str, optional): The language model to use for interpretation. Defaults to "gpt-5".

    Returns:
        Tuple[str, bool]: A tuple containing:
        output (str): A natural language answer that explains the query results in an easy-to-understand format.
        success (bool): True if the final SQL query was adequate to answer the query, False if refined.

    Note:
        The response focuses on clarity and readability, avoiding SQL syntax and technical jargon
        where possible. If results are empty, it explains that no data was found.
    """
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()
    prompt = f"""
You are an expert data analyst translating database query results into clear, actionable insights.

## CONTEXT
**User's Question:**
{query}

**Database Schema:**
{metadata}

**Query Results:**
{sql_gen_ref}

## YOUR TASK
Provide a natural language answer that directly addresses the user's question based on the SQL query results. Provide complete but concise answer. Provide specific details and figures from the results where relevant. 

If the natural language answer fully provides the answers to question, indicate success as True. If the results are empty or insufficient to answer the question, indicate success as False.

## OUTPUT FORMAT
Return ONLY a valid JSON object with this exact structure:
{{
    "output": "Brief answer to the query",
    "success": True/False
}}
Do not include any text outside the JSON object.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    content = response.choices[0].message.content
    # Strip markdown code blocks and fix Python-style booleans
    content_clean = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    content_clean = content_clean.replace(": True", ": true").replace(": False", ": false")

    try:
        obj = json.loads(content_clean)
        output = str(obj["output"]).strip()
        success = bool(obj["success"])
        print("output ", output)
        print("success ", success)
    except Exception as e:
        # Fallback if the model does not return valid JSON
        print(f"❌ JSON parsing error: {e}")
        print(f"Raw response: {content}")
        output = content.strip()
        success = False
    return output, success

def database_agent(query: str, model: str = "gpt-5", return_details: bool = False, max_refine_attempts: int = 5) -> str | dict:
    """
    Processes natural language database queries using a two-stage SQL generation and refinement workflow.

    This function converts a natural language question into SQL, executes it against a SQLite database,
    refines the query if needed, and returns a natural language interpretation of the results.

    Workflow:
        1. Initializes database tables and retrieves schema metadata
        2. Generates an initial SQL query from the natural language question
        3. Executes and evaluates the query results
        4. Refines the SQL query based on feedback if necessary
        5. Returns a natural language interpretation of the final results

    Args:
        query (str): The user's natural language question about the database.
        model (str, optional): The language model to use for SQL generation and interpretation.
        return_details (bool, optional): If True, returns a dict with all intermediate steps. Defaults to False.

    Returns:
        str or dict: If return_details is False, returns natural language answer.
                     If return_details is True, returns dict with 'answer', 'sql_v1', 'sql_v2',
                     'feedback', 'results_v1', 'results_v2'.
    """
    # Get client from session state
    client = st.session_state.get("client") or OpenAI()

    #Initialize DB and get metadata
    conn = sqlite3.connect(PATH)
    create_tables()
    create_metadata()
    meta_schema = get_metaschema()

    prompt = f"""
You are an expert SQLite query generator. Your task is to convert natural language questions into accurate, efficient SQL queries. Only answer relevant questions based on the provided database schema. If the question is unrelated to the database, respond with "SELECT NULL;".

## TABLE SCHEMA
{meta_schema}

## USER QUESTION
{query}

## OUTPUT FORMAT
Return ONLY the SQL query without any explanation, markdown formatting, or code blocks.
Do NOT include ```sql``` tags or any other text - just the raw SQL query.

Now generate the SQL query for the user's question above:
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    sql_gen_1 = response.choices[0].message.content.strip()

    # Execute the first SQL query to get initial results
    q1 = sql_gen_1.strip().removeprefix("```sql").removesuffix("```").strip()

    # Check if query is irrelevant (returns SELECT NULL or similar)
    if q1.upper() in ["SELECT NULL;", "SELECT NULL", "NULL"]:
        conn.close()
        irrelevant_msg = "The query is not related to the investigation database."
        if return_details:
            return {
                'answer': irrelevant_msg,
                'sql_v1': q1,
                'sql_v2': q1,
                'feedback': 'Question is not related to the database schema',
                'results_v1': pd.DataFrame(),
                'results_v2': pd.DataFrame()
            }
        return irrelevant_msg

    try:
        sql_gen_orig = pd.read_sql_query(q1, conn)
    except Exception as e:
        # If first query fails, create empty dataframe with error
        sql_gen_orig = pd.DataFrame({"error": [str(e)]})
        print(f"❌ Error executing initial query: {e}")
    
    sql_error = None
    for i in range(max_refine_attempts):
        # Evaluate and refine the SQL based on initial results
        if i == 0:
            refined_sql=sql_gen_1,
            sql_gen_ref=sql_gen_orig
        feedback, refined_sql = evaluate_and_refine_sql(
                question=query,
                sql_query=refined_sql,
                df=sql_gen_ref,
                schema=meta_schema,
                model=model,
                sql_error = sql_error
            )
        # Execute the refined SQL query
        q2 = refined_sql.strip().removeprefix("```sql").removesuffix("```").strip()

        try:
            sql_gen_ref = pd.read_sql_query(q2, conn)
        except Exception as e:
            print(f"❌ Error executing refined query: {e}")
            sql_error = e
        output, success = database_interpreter(query, sql_gen_ref, metadata=meta_schema, model=model)

        print("Refinement Attempt", i+1)
        print("Success or not: ", success)
        print("📝 Reflect on V1 query:\n" + feedback)
        print("🔁 Write V2 query:\n" + refined_sql)
        print("🔁 Answer:\n" + output)
        print("\n")

        if success:
            break
    conn.close()
    

    if return_details:
        return {
            'answer': output,
            'sql_v1': q1,
            'sql_v2': q2,
            'feedback': feedback,
            'results_v1': sql_gen_orig,
            'results_v2': sql_gen_ref
        }
    return output
