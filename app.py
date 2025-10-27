import streamlit as st
import streamlit.components.v1 as components
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Page config
st.set_page_config(
    page_title="Agentic Workflow Platform",
    page_icon="🤖",
    layout="centered"
)

def render_mermaid(mermaid_code, height=400, center=False):
    """Render mermaid diagram using HTML and mermaid.js"""
    center_style = ""
    if center:
        center_style = """
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 20px;
                min-height: 100%;
            }
            .mermaid {
                display: flex;
                justify-content: center;
            }
        </style>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        {center_style}
    </head>
    <body>
        <div class="mermaid">
{mermaid_code}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=True)

@st.dialog("Research Assistant Workflow", width="large")
def show_research_diagram():
    mermaid_code = """
flowchart TD
    Start([User Topic]) --> Planner[Planner Agent<br/>Generate 5 Steps]
    Planner --> Executor[Executor Agent]

    Executor --> |Route Step|Research[Research Agent<br/>arXiv, Tavily, Wikipedia]
    Executor --> |Route Step|Writer[Writer Agent<br/>Draft Content]
    Executor --> |Route Step|Editor[Editor Agent<br/>Refine Content]

    Research --> Context[Context Storage]
    Writer --> Context
    Editor --> Context

    Context --> Loop{More<br/>Steps?}
    Loop --> |Yes|Executor
    Loop --> |No|Report[Final Report]
    Report --> End([Display])

    style Start fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style End fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style Planner fill:#87CEEB,stroke:#333,stroke-width:2px,color:#000
    style Executor fill:#FFB347,stroke:#333,stroke-width:2px,color:#000
    style Research fill:#DDA0DD,stroke:#333,stroke-width:2px,color:#000
    style Writer fill:#F0A0C0,stroke:#333,stroke-width:2px,color:#000
    style Editor fill:#C9A0DC,stroke:#333,stroke-width:2px,color:#000
    style Report fill:#98FB98,stroke:#333,stroke-width:2px,color:#000
    """
    render_mermaid(mermaid_code, height=600)
    st.caption("Multi-agent orchestration pattern: Planner → Executor → Specialized Agents → Context Accumulation → Final Report")

@st.dialog("Clinical Evidence Workflow", width="large")
def show_clinical_diagram():
    mermaid_code = """
flowchart TD
    Start([Medical Topic]) --> Planner[Planner Agent<br/>Generate 5 Steps]
    Planner --> Executor[Executor Agent]

    Executor --> |Route Step|Medical[Medical Agent<br/>PubMed, Cochrane]
    Executor --> |Route Step|Writer[Writer Agent<br/>Draft Content]
    Executor --> |Route Step|Editor[Editor Agent<br/>Refine Content]

    Medical --> Context[Context Storage]
    Writer --> Context
    Editor --> Context

    Context --> Loop{More<br/>Steps?}
    Loop --> |Yes|Executor
    Loop --> |No|Report[Clinical Report]
    Report --> End([Display])

    style Start fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style End fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style Planner fill:#87CEEB,stroke:#333,stroke-width:2px,color:#000
    style Executor fill:#FFB347,stroke:#333,stroke-width:2px,color:#000
    style Medical fill:#FF69B4,stroke:#333,stroke-width:2px,color:#000
    style Writer fill:#F0A0C0,stroke:#333,stroke-width:2px,color:#000
    style Editor fill:#C9A0DC,stroke:#333,stroke-width:2px,color:#000
    style Report fill:#98FB98,stroke:#333,stroke-width:2px,color:#000
    """
    render_mermaid(mermaid_code, height=600)
    st.caption("Multi-agent orchestration pattern with medical-specific data sources")

@st.dialog("OpenRCA Database Workflow", width="large")
def show_openrca_diagram():
    mermaid_code = """
flowchart TD
    Start([User Query]) --> DB[Load Database<br/>& Schema]
    DB --> Gen1[Generate SQL V1]
    Gen1 --> Exec1[Execute V1]

    Exec1 --> Eval{Evaluate<br/>Correctness}
    Eval --> |Needs Improvement|Refine[Refine SQL V2]
    Eval --> |Correct|Interpret

    Refine --> Exec2[Execute V2]
    Exec2 --> Interpret[Interpret Results]

    Interpret --> Success{Success?}
    Success --> |No & < 5 attempts|Eval
    Success --> |Yes|Answer[Natural Language<br/>Answer]

    Answer --> End([Display + SQL Details])

    style Start fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style End fill:#90EE90,stroke:#333,stroke-width:2px,color:#000
    style DB fill:#87CEEB,stroke:#333,stroke-width:2px,color:#000
    style Gen1 fill:#FFD700,stroke:#333,stroke-width:2px,color:#000
    style Eval fill:#DDA0DD,stroke:#333,stroke-width:2px,color:#000
    style Refine fill:#FFB347,stroke:#333,stroke-width:2px,color:#000
    style Interpret fill:#98FB98,stroke:#333,stroke-width:2px,color:#000
    style Answer fill:#87CEEB,stroke:#333,stroke-width:2px,color:#000
    """
    render_mermaid(mermaid_code, height=600, center=True)
    st.caption("Iterative refinement pattern: Generate SQL → Execute → Evaluate → Refine → Interpret → Answer (Loop until success or max 5 attempts)")

def main():
    # Custom CSS for landing page - wider and responsive
    st.markdown("""
        <style>
        /* Wider container for landing page */
        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Mobile responsive - columns stack automatically */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            /* Reduce gradient box padding on mobile */
            div[style*='gradient'] {
                padding: 20px !important;
            }
        }

        /* Push sidebar footer to bottom */
        [data-testid="stSidebar"] > div:first-child {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        .sidebar-footer {
            margin-top: auto;
            padding: 1rem 0;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    # Hero Section
    st.markdown("<h1 style='text-align: center;'>🤖 Agentic Workflow Platform</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: #666;'>AI-Powered Multi-Agent Platform for Research & Database Analysis</p>",
                unsafe_allow_html=True)

    st.markdown("---")

    # Introduction
    st.markdown("""
    ### Welcome to the Agentic Workflow Platform

    This intelligent multi-agent platform provides specialized AI assistants for different workflows—from academic research
    to medical evidence gathering to database analysis. Simply choose your assistant and let the AI agents handle the rest.

    **Research Workflows:**
    1. **Planner Agent** - Breaks down your research topic into actionable steps
    2. **Research/Medical Agent** - Searches credible databases and sources
    3. **Writer Agent** - Drafts well-structured summaries and reports
    4. **Editor Agent** - Reviews, critiques, and refines the content
    5. **Execution Agent** - Orchestrates the entire workflow

    **Database Workflow:**
    1. **Database Agent** - Converts natural language to SQL queries
    2. **Query Refinement** - Iteratively improves SQL accuracy
    3. **Result Interpretation** - Translates data into actionable insights

    Choose your assistant below to get started:
    """)

    st.markdown("---")

    # Research Assistant 1: General Research
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>✍️Research Assistant📓</h1>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>AI agent that conducts research and generates reports.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 View Details & Features", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Ideal for:**
            - Academic research papers
            - Technical documentation
            - Scientific literature reviews
            - General knowledge gathering

            **Typical Use Cases:**
            - Computer Science & AI research
            - Physics & Mathematics
            - Engineering topics
            - General academic inquiries
            """)

        with col2:
            st.markdown("""
            **Data Sources:**
            - 📚 **arXiv** - Academic papers and preprints
            - 🌐 **Tavily** - General web search
            - 📖 **Wikipedia** - Encyclopedic knowledge

            **Workflow Time:** 2-3 minutes
            """)

        st.info("💡 Best for broad academic topics across multiple disciplines")

        if st.button("📊 View Workflow Diagram", key="research_diagram"):
            show_research_diagram()

        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <p><strong>👉 Navigate to: Pages → Research Assistant</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Research Assistant 2: Medical Research
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>🔍 Dr. ResearchRx⚕️</h1>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>Medical researcher that searches credible references</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🩺 View Details & Features", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Ideal for:**
            - Clinical research
            - Medical literature reviews
            - Evidence-based medicine
            - Healthcare decision support

            **Typical Use Cases:**
            - Disease research & treatment options
            - Drug efficacy & safety studies
            - Clinical guidelines & protocols
            - Medical condition analysis
            """)

        with col2:
            st.markdown("""
            **Data Sources:**
            - 🩺 **PubMed** - Medical research papers & clinical studies
            - 📊 **Cochrane Library** - Systematic reviews & meta-analyses

            **Workflow Time:** 2-3 minutes
            """)

        st.success("⚕️ Best for medical, clinical, and healthcare topics")

        if st.button("📊 View Workflow Diagram", key="clinical_diagram"):
            show_clinical_diagram()

        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <p><strong>👉 Navigate to: Pages → Clinical Evidence</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # OpenRCA: Database Assistant
    st.markdown("""
    <div style='background: linear-gradient(135deg, #D24726 0%, #ff8c42 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h1 style='text-align: center; color: white; margin: 0;'>🔧OpenRCA📖</h1>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>Ask questions about equipment failures from RCA database</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 View Details & Features", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Ideal for:**
            - Equipment failure analysis
            - Root cause investigation
            - Corrective action tracking
            - Maintenance data exploration

            **Typical Use Cases:**
            - Finding most expensive failures
            - Identifying common failure patterns
            - Analyzing downtime by equipment
            - Reviewing corrective actions
            """)

        with col2:
            st.markdown("""
            **Features:**
            - 🗣️ **Natural Language Queries** - Ask questions in plain English
            - 🔄 **Smart SQL Generation** - AI converts questions to SQL
            - 📊 **Database Browser** - Explore tables with filtering
            - 📥 **Export Data** - Download filtered results as CSV

            **Workflow Time:** 20-40 seconds.
            """)

        st.warning("🔧 Best for analyzing equipment failures and maintenance data")

        if st.button("📊 View Workflow Diagram", key="openrca_diagram"):
            show_openrca_diagram()

        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <p><strong>👉 Navigate to: Pages → OpenRCA</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features section
    st.markdown("### ✨ Key Features")

    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        st.markdown("""
        **🤖 Fully Autonomous**
        - Zero manual intervention
        - Intelligent task planning
        - Self-organizing agents
        """)

    with feat_col2:
        st.markdown("""
        **🎯 Evidence-Based**
        - Credible sources only
        - Peer-reviewed content
        - APA format citations
        """)

    with feat_col3:
        st.markdown("""
        **📝 Complete Reports**
        - Structured markdown output
        - Introduction & findings
        - Conclusion & references
        """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666;'>
        <p><strong>Built with Streamlit | Powered by HuggingFace</strong></p>
        <p>Navigate using the sidebar to access <strong>Research Assistant</strong>, <strong>Clinical Evidence</strong>, or <strong>OpenRCA</strong></p>
    </div>
    """, unsafe_allow_html=True)

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
