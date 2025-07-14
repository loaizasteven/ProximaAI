"""
ProximaAI Tools - Collection of tools for job search, resume building, and career coaching.
"""

from proximaai.tools.agent_builder import AgentBuilder, AgentSpec
from proximaai.tools.perplexity_search import PerplexityWebSearchTool

__all__ = [
    # Agent Building
    "AgentBuilder",
    "AgentSpec",
    
    # Web Search
    "PerplexityWebSearchTool"
] 