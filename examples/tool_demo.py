#!/usr/bin/env python3
"""
Demo script showcasing the ProximaAI tools functionality.
"""

import sys
import os
import json
from proximaai.utils.logger import setup_logging, get_logger

# Setup logging
logger = setup_logging(level="INFO")

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proximaai.tools.tool_registry import ToolRegistry
from proximaai.tools.agent_builder import AgentBuilder

tool_registry = ToolRegistry()


def log_header(title):
    """Log a formatted header."""
    logger.info(f"🎯 {title}")


def log_section(title):
    """Log a formatted section."""
    logger.info(f"📋 {title}")


def demo_agent_builder():
    """Demonstrate the AgentBuilder tool."""
    log_header("AGENT BUILDER DEMO")
    
    # Get the agent builder tool
    agent_builder = tool_registry.get_tool("agent_builder")
    
    if not agent_builder or not isinstance(agent_builder, AgentBuilder):
        logger.error("AgentBuilder tool not found or invalid type!")
        return
    
    # Example agent specification
    agent_spec = {
        "name": "ResumeAnalyzer",
        "description": "Specialized agent for analyzing and optimizing resumes",
        "system_prompt": """You are a resume analysis expert. Your job is to:
1. Parse and analyze resume content
2. Extract key skills and experience
3. Provide optimization suggestions
4. Calculate ATS compatibility scores

Always provide detailed, actionable feedback to help users improve their resumes.""",
        "tools": ["resume_parser", "resume_optimizer"],
        "model": "anthropic:claude-3-7-sonnet-latest",
        "temperature": 0.1
    }
    
    log_section("Creating Specialized Agent")
    logger.info("🔄 Creating a specialized Resume Analyzer agent...")
    result = agent_builder._run(json.dumps(agent_spec))
    logger.info("Agent created successfully", result=result)
    
    # List created agents
    log_section("Created Agents")
    agents = agent_builder.list_agents()
    if agents:
        for agent in agents:
            logger.info(f"🤖 {agent['name']} (ID: {agent['id']})", 
                       description=agent['description'],
                       tools=agent['tools'])
    else:
        logger.info("📭 No agents created yet.")


def demo_tool_registry():
    """Demonstrate the tool registry functionality."""
    log_header("TOOL REGISTRY DEMO")
    
    # List all available tools
    log_section("Available Tools by Category")
    categories = tool_registry.list_available_tools()
    for category, tools in categories.items():
        logger.info(f"🔧 {category.upper()}:")
        for tool_name in tools:
            tool = tool_registry.get_tool(tool_name)
            if tool:
                # Truncate description for better readability
                desc = tool.description.strip()
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                logger.info(f"   • {tool_name}: {desc}")
    
    # Get tool descriptions
    log_section("Tool Details")
    descriptions = tool_registry.get_tool_descriptions()
    for tool_name, description in descriptions.items():
        logger.info(f"🛠️ {tool_name.upper()}:")
        # Format description with proper indentation
        lines = description.strip().split('\n')
        for line in lines:
            if line.strip():
                logger.info(f"   {line.strip()}")


def main():
    """Run the demo."""
    log_header("PROXIMAAI TOOLS DEMO")
    logger.info("🚀 Welcome to ProximaAI! This demo showcases our comprehensive tool suite.")
    
    try:
        demo_tool_registry()
        demo_agent_builder()
        
        log_header("DEMO COMPLETED")
        logger.info("✅ All demonstrations completed successfully!")
        logger.info("🎉 Your ProximaAI system is ready to use!")
        
    except Exception as e:
        logger.exception("Error during demo", error=str(e))


if __name__ == "__main__":
    main() 