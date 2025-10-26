import streamlit as st
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Page config
st.set_page_config(
    page_title="Agentic Workflow Platform",
    page_icon="🤖",
    layout="centered"
)

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
        <h2 style='text-align: center; color: white; margin: 0;'>✍️ Research Assistant</h2>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>General Academic & Scientific Research</p>
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
        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <p><strong>👉 Navigate to: Pages → Research Assistant</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Research Assistant 2: Medical Research
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h2 style='text-align: center; color: white; margin: 0;'>🔍 Dr. ResearchRx</h2>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>Evidence-Based Medical Research</p>
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
        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <p><strong>👉 Navigate to: Pages → Clinical Evidence</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # OpenRCA: Database Assistant
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff8c42 0%, #ffd700 100%); padding: 25px; border-radius: 10px; color: white; margin-bottom: 15px;'>
        <h2 style='text-align: center; color: white; margin: 0;'>🔧 OpenRCA</h2>
        <p style='text-align: center; margin: 5px 0 0 0; opacity: 0.9;'>Root Cause Analysis Database Assistant</p>
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

            **Workflow Time:** 1-2 minutes
            """)

        st.warning("🔧 Best for analyzing equipment failures and maintenance data")
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
