---
title: Agentic Workflows
emoji: 🤖
colorFrom: blue
colorTo: gray
sdk: streamlit
sdk_version: 1.49.1
app_file: app.py
pinned: false
license: mit
short_description: 'Multi-Agent Systems for different workflows'
---

# 🤖 Agentic Research Workflow

An intelligent multi-agent system that automates the entire research process—from planning to execution to report generation. Simply provide a topic, and our AI agents will collaborate to conduct comprehensive research while you focus on what matters.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.49.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### **🤖 Fully Autonomous**
- Zero manual intervention required
- Intelligent task planning and decomposition
- Self-organizing multi-agent coordination

### **🎯 Evidence-Based**
- Searches only credible, peer-reviewed sources
- Medical databases (PubMed, Cochrane Library)
- Academic databases (arXiv, Wikipedia, Tavily)
- APA format citations

### **📝 Complete Reports**
- Structured markdown output
- Introduction, findings, and conclusions
- Comprehensive reference sections
- Publication-ready format

## 🏗️ Architecture

The system uses a **5-agent workflow** that works collaboratively:

1. **Planner Agent** - Breaks down research topics into actionable steps
2. **Research/Medical Agent** - Searches credible databases and sources
3. **Writer Agent** - Drafts well-structured summaries and reports
4. **Editor Agent** - Reviews, critiques, and refines content
5. **Execution Agent** - Orchestrates the entire workflow

## 📱 Applications

The application includes three pages accessible via the Streamlit sidebar:

### 🏠 **Landing Page**
- Overview of the agentic workflow system
- Choose between Research Assistant or Clinical Evidence
- Key features and capabilities
- Navigation to specialized research assistants

### ✍️ **Research Assistant** (General Academic & Scientific)

**Ideal for:**
- Academic research papers
- Technical documentation
- Scientific literature reviews
- General knowledge gathering

**Data Sources:**
- 📚 **arXiv** - Academic papers and preprints
- 🌐 **Tavily** - General web search
- 📖 **Wikipedia** - Encyclopedic knowledge

**Typical Use Cases:**
- Computer Science & AI research
- Physics & Mathematics
- Engineering topics
- General academic inquiries

**Workflow Time:** 5-10 minutes

### 🔍 **Dr. ResearchRx** (Evidence-Based Medical Research)

**Ideal for:**
- Clinical research
- Medical literature reviews
- Evidence-based medicine
- Healthcare decision support

**Data Sources:**
- 🩺 **PubMed** - Medical research papers & clinical studies
- 📊 **Cochrane Library** - Systematic reviews & meta-analyses

**Typical Use Cases:**
- Disease research & treatment options
- Drug efficacy & safety studies
- Clinical guidelines & protocols
- Medical condition analysis

**Workflow Time:** 2-3 minutes

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Tavily API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/palscruz23/agentic-workflow.git
cd agentic-workflow
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

4. **Run the application:**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### 🐳 Docker Deployment

You can also run the application using Docker for a containerized deployment:

**Option 1: Using Docker Compose (Recommended)**

1. **Create `.env` file** with your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

3. **Access the application:**
Open your browser at `http://localhost:8501`

4. **Stop the container:**
```bash
docker-compose down
```

**Option 2: Using Docker directly**

1. **Build the Docker image:**
```bash
docker build -t agentic-workflow .
```

2. **Run the container:**
```bash
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e TAVILY_API_KEY=your_tavily_api_key_here \
  --name agentic-research \
  agentic-workflow
```

3. **View logs:**
```bash
docker logs -f agentic-research
```

4. **Stop the container:**
```bash
docker stop agentic-research
docker rm agentic-research
```

## 📂 Project Structure

```
agentic-workflow/
├── app.py                      # Landing page (main entry point)
├── About.py                    # About page with workflow details
├── pages/
│   ├── 1_Research Assistant.py # General academic research
│   └── 2_Clinical Evidence.py  # Medical research
├── agents/
│   ├── planner_agent.py        # Task planning and decomposition
│   ├── research_agent.py       # General research (arXiv, Tavily, Wikipedia)
│   ├── medical_agent.py        # Medical research (PubMed, Cochrane)
│   ├── writer_agent.py         # Content generation
│   ├── editor_agent.py         # Content review and refinement
│   └── execution_agent.py      # Workflow orchestration
├── tools/
│   ├── research_tools.py       # arXiv, Tavily, Wikipedia search tools
│   └── medical_tools.py        # PubMed, Cochrane search tools
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore              # Docker build ignore file
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `TAVILY_API_KEY` - Your Tavily API key (required)
- `DLAI_TAVILY_BASE_URL` - Optional custom Tavily base URL

### Model Configuration

By default, the application uses `gpt-4o-mini`. You can modify this in `app.py`:

```python
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"  # Change this
```

## 💡 Usage Examples

### Example 1: General Academic Research

**Topic:** "Transformer architecture in neural networks"

**Agent Workflow:**
1. **Planner:** Breaks down into 5 steps (search arXiv, search Wikipedia, draft report, edit, finalize)
2. **Research Agent:** Searches arXiv for papers on transformers, queries Wikipedia for background
3. **Writer Agent:** Drafts comprehensive report with findings
4. **Editor Agent:** Reviews and improves clarity, structure
5. **Execution Agent:** Delivers final markdown report with references

**Output:** Complete research report with introduction, key findings, and APA citations

### Example 2: Medical Research

**Topic:** "Latest treatments for Type 2 Diabetes"

**Agent Workflow:**
1. **Planner:** Creates medical research plan
2. **Medical Agent:** Searches PubMed for clinical studies, Cochrane for systematic reviews
3. **Writer Agent:** Compiles evidence-based summary
4. **Editor Agent:** Refines medical terminology and accuracy
5. **Execution Agent:** Produces clinical evidence report

**Output:** Evidence-based medical report with peer-reviewed sources

## 🛠️ Development

### Adding New Tools

To add a new research tool:

1. Create the tool function in `tools/research_tools.py` or `tools/medical_tools.py`:
```python
def new_search_tool(query: str, max_results: int = 5) -> list[dict]:
    # Implementation
    return results
```

2. Define the tool specification:
```python
new_tool_def = {
    "type": "function",
    "function": {
        "name": "new_search_tool",
        "description": "Description of what this tool does",
        "parameters": {...}
    }
}
```

3. Add to the appropriate agent's tool mapping

### Customizing Agents

Each agent can be customized by modifying the system prompts in the respective agent files:
- `agents/planner_agent.py` - Planning strategy
- `agents/research_agent.py` - Research approach
- `agents/writer_agent.py` - Writing style
- `agents/editor_agent.py` - Review criteria

## 🧪 Testing

Run the application locally to test:
```bash
streamlit run app.py
```

Navigate to each page to ensure:
- ✅ Landing page displays correctly
- ✅ Research Assistant can search arXiv, Tavily, Wikipedia
- ✅ Clinical Evidence can search PubMed, Cochrane
- ✅ Reports are generated with proper formatting

## 🐛 Troubleshooting

### Common Issues

**Issue: Import Error for agents**
```
ImportError: cannot import name 'planner_agent' from 'agents.planner_agent'
```
**Solution:** Ensure all agent files have proper OpenAI client initialization inside functions, not at module level.

**Issue: API Key Errors**
```
ValueError: TAVILY_API_KEY not found in environment variables
```
**Solution:** Create `.env` file with required API keys.

**Issue: Session State Errors**
```
AttributeError: st.session_state has no attribute 'client'
```
**Solution:** The app initializes session state in `init_chatbot()`. Ensure it's called before using agents.

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-4o-mini](https://openai.com/)
- Research tools: [arXiv](https://arxiv.org/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/), [Cochrane Library](https://www.cochranelibrary.com/)
- Web search: [Tavily](https://tavily.com/)

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/palscruz23/agentic-workflow/issues)
- **Repository:** [GitHub Repository](https://github.com/palscruz23/rul-estimation)

---

**Built with Claude, OpenAI, Streamlit | Powered by Multi-Agent AI** 🤖
