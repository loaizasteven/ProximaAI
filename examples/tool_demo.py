#!/usr/bin/env python3
"""
Demo script showcasing the ProximaAI tools functionality.
"""

import sys
import os
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from proximaai.tools.tool_registry import ToolRegistry
from proximaai.tools.agent_builder import AgentBuilder

tool_registry = ToolRegistry()


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")


def print_section(title):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 40)


def demo_agent_builder():
    """Demonstrate the AgentBuilder tool."""
    print_header("AGENT BUILDER DEMO")
    
    # Get the agent builder tool
    agent_builder = tool_registry.get_tool("agent_builder")
    
    if not agent_builder or not isinstance(agent_builder, AgentBuilder):
        print("❌ AgentBuilder tool not found or invalid type!")
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
    
    print_section("Creating Specialized Agent")
    print("🔄 Creating a specialized Resume Analyzer agent...")
    result = agent_builder._run(json.dumps(agent_spec))
    print(f"✅ {result}\n")
    
    # List created agents
    print_section("Created Agents")
    agents = agent_builder.list_agents()
    if agents:
        for agent in agents:
            print(f"🤖 {agent['name']} (ID: {agent['id']})")
            print(f"   📝 {agent['description']}")
            print(f"   🛠️  Tools: {', '.join(agent['tools'])}")
            print()
    else:
        print("📭 No agents created yet.")


def demo_tool_registry():
    """Demonstrate the tool registry functionality."""
    print_header("TOOL REGISTRY DEMO")
    
    # List all available tools
    print_section("Available Tools by Category")
    categories = tool_registry.list_available_tools()
    for category, tools in categories.items():
        print(f"\n🔧 {category.upper()}:")
        for tool_name in tools:
            tool = tool_registry.get_tool(tool_name)
            if tool:
                # Truncate description for better readability
                desc = tool.description.strip()
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                print(f"   • {tool_name}: {desc}")
    
    # Get tool descriptions
    print_section("Tool Details")
    descriptions = tool_registry.get_tool_descriptions()
    for tool_name, description in descriptions.items():
        print(f"\n🛠️  {tool_name.upper()}:")
        # Format description with proper indentation
        lines = description.strip().split('\n')
        for line in lines:
            if line.strip():
                print(f"   {line.strip()}")


def main():
    """Run the demo."""
    print_header("PROXIMAAI TOOLS DEMO")
    print("🚀 Welcome to ProximaAI! This demo showcases our comprehensive tool suite.")
    
    try:
        demo_tool_registry()
        demo_agent_builder()
        
        print_header("DEMO COMPLETED")
        print("✅ All demonstrations completed successfully!")
        print("🎉 Your ProximaAI system is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 