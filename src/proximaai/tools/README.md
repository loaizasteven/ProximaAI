# ProximaAI Tools

This directory contains Python tools for job search, resume analysis, and career coaching.

## PerplexityWebSearchTool

- **Location:** [`perplexity_search.py`](./perplexity_search.py)

### Why a New Approach?

Previously, some tools (like Perplexity search) were implemented as MCP (Model Context Protocol) subprocesses, requiring a separate server process and communication over stdio. This approach worked locally but caused major issues when deploying to cloud platforms like LangGraph Studio, where:
- Subprocesses and custom servers are not supported or are unreliable.
- System-level dependencies cannot be controlled.

### The Solution: Pure Python Perplexity Tool

**`perplexity_search.py`** implements `PerplexityWebSearchTool`, a pure Python tool that:
- Calls the Perplexity API directly using `httpx`.
- Requires no subprocesses, servers, or MCP protocol.
- Is portable and cloud-compatible.
- Can be registered and used like any other Python tool in the registry.

**Usage Example:**
```python
from proximaai.tools.perplexity_search import PerplexityWebSearchTool

tool = PerplexityWebSearchTool()
result = tool._run("What is the mission of Meta?")
print(result)
```

### How It Differs from the MCP Version
- **MCP Version:** Required launching a separate server process, communicating over stdio, and managing environment variables for the subprocess. This was fragile and not supported in cloud environments.
- **Pure Python Version:** Runs entirely in-process, with no external dependencies or subprocesses. All API calls are made directly from Python, making it robust and cloud-ready.
