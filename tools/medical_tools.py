# --- Standard library ---
import os

# --- Third-party ---
from dotenv import load_dotenv
from tavily import TavilyClient

# Init env
load_dotenv()


def pubmed_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches PubMed for medical research papers and publications matching the given query.

    Args:
        query (str): Medical topic or search keywords.
        max_results (int): Maximum number of results to return (default 5).

    Returns:
        list[dict]: A list of dictionaries with keys like 'title', 'content', and 'url'.
    """
    max_results = min(max_results, 5)  # Limit to reasonable number

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")

    # Get optional base URL for Tavily
    api_base_url = os.getenv("DLAI_TAVILY_BASE_URL")

    # Initialize Tavily client
    params = {'api_key': api_key}
    if api_base_url:
        params['api_base_url'] = api_base_url

    client = TavilyClient(**params)

    try:
        # Search with domain restriction to PubMed
        response = client.search(
            query=query,
            max_results=max_results,
            include_domains=["pubmed.ncbi.nlm.nih.gov"]
        )

        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", ""),
                "score": r.get("score", 0)
            })

        return results if results else [{"message": "No results found on PubMed for this query."}]

    except Exception as e:
        return [{"error": f"PubMed search failed: {str(e)}"}]


pubmed_tool_def = {
    "type": "function",
    "function": {
        "name": "pubmed_search_tool",
        "description": "Searches PubMed (pubmed.ncbi.nlm.nih.gov) for medical research papers, clinical studies, and publications related to the query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Medical topic or search keywords for PubMed database."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}


def cochrane_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches Cochrane Library for systematic reviews and evidence-based medical information.

    Args:
        query (str): Medical topic or search keywords.
        max_results (int): Maximum number of results to return (default 5).

    Returns:
        list[dict]: A list of dictionaries with keys like 'title', 'content', and 'url'.
    """
    max_results = min(max_results, 5)  # Limit to reasonable number

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")

    # Get optional base URL for Tavily
    api_base_url = os.getenv("DLAI_TAVILY_BASE_URL")

    # Initialize Tavily client
    params = {'api_key': api_key}
    if api_base_url:
        params['api_base_url'] = api_base_url

    client = TavilyClient(**params)

    try:
        # Search with domain restriction to Cochrane Library
        response = client.search(
            query=query,
            max_results=max_results,
            include_domains=["cochranelibrary.com"]
        )

        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", ""),
                "score": r.get("score", 0)
            })

        return results if results else [{"message": "No results found on Cochrane Library for this query."}]

    except Exception as e:
        return [{"error": f"Cochrane Library search failed: {str(e)}"}]


cochrane_tool_def = {
    "type": "function",
    "function": {
        "name": "cochrane_search_tool",
        "description": "Searches Cochrane Library (cochranelibrary.com) for systematic reviews, meta-analyses, and evidence-based medical information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Medical topic or search keywords for Cochrane Library database."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}


def medical_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches both PubMed and Cochrane Library for comprehensive medical information.

    Args:
        query (str): Medical topic or search keywords.
        max_results (int): Maximum number of results per source (default 5).

    Returns:
        list[dict]: Combined results from both PubMed and Cochrane Library.
    """
    results = []

    # Search PubMed
    pubmed_results = pubmed_search_tool(query, max_results)
    for result in pubmed_results:
        if "error" not in result and "message" not in result:
            result["source"] = "PubMed"
            results.append(result)

    # Search Cochrane Library
    cochrane_results = cochrane_search_tool(query, max_results)
    for result in cochrane_results:
        if "error" not in result and "message" not in result:
            result["source"] = "Cochrane Library"
            results.append(result)

    if not results:
        return [{"message": "No results found on PubMed or Cochrane Library for this query."}]

    # Sort by relevance score if available
    results.sort(key=lambda x: x.get("score", 0), reverse=True)

    return results


medical_search_tool_def = {
    "type": "function",
    "function": {
        "name": "medical_search_tool",
        "description": "Searches both PubMed and Cochrane Library simultaneously for comprehensive medical research information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Medical topic or search keywords."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results per source (PubMed and Cochrane).",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}


# Tool mapping for medical search tools
medical_tool_mapping = {
    "pubmed_search_tool": pubmed_search_tool,
    "cochrane_search_tool": cochrane_search_tool,
    "medical_search_tool": medical_search_tool
}
