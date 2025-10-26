import streamlit as st
import sys
import os
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import sqlite3

# Add parent directory to path to import agents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.database_agent import database_agent

# Load environment variables
load_dotenv(find_dotenv())

# Database path
DB_PATH = 'data/rca_data.db'

def init_chatbot():
    """Initialize session state for the chatbot"""
    if "client" not in st.session_state:
        st.session_state.client = OpenAI()
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4o-mini"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_sql_details" not in st.session_state:
        st.session_state.show_sql_details = True
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None

def clear_chat():
    """Clear chat history"""
    st.session_state.messages = []
    st.rerun()

def get_sample_questions():
    """Return sample questions for the RCA database"""
    return [
        "What are the top 3 most expensive failures?",
        "Show me all failures in the Processing Plant area",
        "Which equipment has the longest downtime?",
        "What are the most common root causes?",
        "Show failures with downtime over 50 hours"
    ]

def get_database_tables():
    """Get list of tables from the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        st.error(f"Error fetching tables: {e}")
        return []

def get_table_data(table_name, limit=100):
    """Get data from a specific table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()

@st.dialog("Database Browser", width="large")
def show_database_browser():
    """Display database browser dialog"""
    st.markdown("### Browse Database Tables")
    st.info("Quick view of database tables - limited to 100 rows per table")

    tables = get_database_tables()

    if not tables:
        st.warning("No tables found in the database")
        return

    selected_table = st.selectbox("Select a table to view:", tables)

    if selected_table:
        st.markdown(f"#### Table: `{selected_table}`")

        # Get table data
        df = get_table_data(selected_table)

        if not df.empty:
            # Add row filtering section
            st.markdown("##### Filter Rows")

            filter_enabled = st.checkbox("Enable row filtering", value=False)

            filtered_df = df.copy()

            if filter_enabled:
                # Select column to filter
                filter_column = st.selectbox(
                    "Select column to filter:",
                    options=df.columns.tolist(),
                    help="Choose which column to filter by"
                )

                # Get unique values from selected column
                unique_values = df[filter_column].dropna().unique().tolist()

                # Handle different data types
                if len(unique_values) > 50:
                    # For columns with many unique values, use text input
                    filter_value = st.text_input(
                        f"Enter value to filter in '{filter_column}':",
                        help="Enter the exact value or partial match"
                    )

                    if filter_value:
                        # Case-insensitive partial match
                        filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
                else:
                    # For columns with fewer unique values, use multiselect
                    selected_values = st.multiselect(
                        f"Select values from '{filter_column}':",
                        options=sorted(unique_values, key=str),
                        default=None,
                        help="Select one or more values to filter"
                    )

                    if selected_values:
                        filtered_df = df[df[filter_column].isin(selected_values)]

            # Display table info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows Shown", len(filtered_df))
            with col2:
                st.metric("Total Rows", len(df))
            with col3:
                st.metric("Columns", len(df.columns))

            # Display dataframe
            st.dataframe(filtered_df, use_container_width=True, height=400)

            # Option to download
            csv = filtered_df.to_csv(index=False)
            download_label = f"Download {selected_table}" + (" (filtered)" if filter_enabled and len(filtered_df) < len(df) else "")
            st.download_button(
                label=f"{download_label} as CSV",
                data=csv,
                file_name=f"{selected_table}{'_filtered' if filter_enabled else ''}.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"No data found in table: {selected_table}")

def process_query(prompt):
    """Process a query and generate a response"""
    try:
        # Call database_agent with return_details=True
        result = database_agent(
            query=prompt,
            model=st.session_state.model,
            return_details=True
        )
        return result, None
    except Exception as e:
        return None, str(e)

def display_chat_message(role, content, details=None):
    """Display a chat message with optional expandable details"""
    with st.chat_message(role):
        st.markdown(content)

        if details and st.session_state.show_sql_details:
            # Display SQL queries and refinement process
            with st.expander("View SQL Details", expanded=False):
                st.markdown("**Initial SQL Query (V1):**")
                st.code(details['sql_v1'], language='sql')

                st.markdown("**Results from V1:**")
                st.dataframe(details['results_v1'], use_container_width=True)

                st.markdown("**Refinement Feedback:**")
                st.info(details['feedback'])

                st.markdown("**Refined SQL Query (V2):**")
                st.code(details['sql_v2'], language='sql')

                st.markdown("**Final Results:**")
                st.dataframe(details['results_v2'], use_container_width=True)

def main():
    init_chatbot()

    # Page header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #D24726 0%, #ff8c42 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>🔧OpenRCA📖</h1>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>Ask questions about equipment failures from RCA database</p>
    </div>
    """, unsafe_allow_html=True)
    # Info box
    st.info("This chatbot uses with Text-to-SQL tools to query the RCA (Root Cause Analysis) synthetic database. Typical workflow takes 1-2 minutes.")

    # Sidebar
    with st.sidebar:
        st.header("Settings")

        # Clear chat button
        if st.button("Clear Chat History", use_container_width=True):
            clear_chat()

        # Database browser button
        st.header("Database Tools")
        if st.button("📊 Browse Database", use_container_width=True, type="secondary"):
            show_database_browser()

        # Sample questions
        st.header("Sample Questions")
        st.markdown("Click a question to use it:")

        for question in get_sample_questions():
            if st.button(question, key=question, use_container_width=True):
                # Set pending query to be processed
                st.session_state.pending_query = question
                st.rerun()

        st.divider()

        # GitHub footer
        st.markdown(
            """
            <div class='sidebar-footer'>
                <a href='https://github.com/palscruz23/agentic-workflows' target='_blank' style='text-decoration: none;'>
                    GitHub Repository
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.pending_query:
        prompt = st.session_state.pending_query
        
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            display_chat_message(
                "assistant",
                message["content"],
                message.get("details")
            )

    # Chat input
    if prompt := st.chat_input("Ask a question about the RCA database...") or st.session_state.pending_query:
        if st.session_state.pending_query:
            prompt = st.session_state.pending_query
            st.session_state.pending_query = None
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question and querying the database...", show_time=True):
                result, error = process_query(prompt)

            if error:
                error_msg = f"An error occurred: {error}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            else:
                # Display the answer
                st.markdown(result['answer'])

                # Show SQL details if enabled
                if st.session_state.show_sql_details:
                    with st.expander("View SQL Details", expanded=False):
                        st.markdown("**Initial SQL Query (V1):**")
                        st.code(result['sql_v1'], language='sql')

                        st.markdown("**Results from V1:**")
                        st.dataframe(result['results_v1'], use_container_width=True)

                        st.markdown("**Refinement Feedback:**")
                        st.info(result['feedback'])

                        st.markdown("**Refined SQL Query (V2):**")
                        st.code(result['sql_v2'], language='sql')

                        st.markdown("**Final Results:**")
                        st.dataframe(result['results_v2'], use_container_width=True)

                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result['answer'],
                    "details": result
                })
        st.rerun()
if __name__ == "__main__":
    main()
