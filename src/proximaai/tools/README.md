# ProximaAI Tools

This module contains a comprehensive collection of tools for job search, resume building, career coaching, and multi-agent orchestration.

## Overview

The tools are organized into several categories:

- **Agent Building**: Dynamic agent creation and management
- **Web Search**: Internet research and information gathering
- **Resume Tools**: Resume parsing, analysis, and optimization
- **Career Coaching**: Career advice, interview preparation, and skill development
- **Job Search**: Job discovery, analysis, and application tracking

## Tool Registry

The `ToolRegistry` class manages all available tools and provides a centralized way to access them:

```python
from proximaai.tools.tool_registry import tool_registry

# Get all available tools
tools = tool_registry.get_all_tools()

# Get tools by category
web_search_tools = tool_registry.get_tools_by_category("web_search")

# Get a specific tool
agent_builder = tool_registry.get_tool("agent_builder")
```

## Available Tools

### Agent Building

#### AgentBuilder
Dynamically creates specialized agents at runtime based on reasoning plans.

**Features:**
- Create agents with custom system prompts
- Attach specific tools to agents
- Manage agent lifecycle
- Track created agents

**Usage:**
```python
from proximaai.tools.agent_builder import AgentBuilder

agent_spec = {
    "name": "ResumeAnalyzer",
    "description": "Specialized agent for resume analysis",
    "system_prompt": "You are a resume analysis expert...",
    "tools": ["resume_parser", "resume_optimizer"],
    "model": "anthropic:claude-3-7-sonnet-latest",
    "temperature": 0.1
}

agent_builder = AgentBuilder(tool_registry)
result = agent_builder._run(json.dumps(agent_spec))
```

### Web Search

#### WebSearchTool
Performs web searches for job-related information.

**Features:**
- Search for company information
- Find industry trends
- Research job market data
- Get current news and updates

#### CompanyResearchTool
Researches specific companies for comprehensive information.

**Features:**
- Company culture analysis
- Recent news and developments
- Financial performance data
- Job opportunities

#### JobMarketAnalysisTool
Analyzes job market trends and conditions.

**Features:**
- Market demand analysis
- Salary range research
- Industry outlook
- Career path insights

### Resume Tools

#### ResumeParserTool
Parses and extracts information from resumes.

**Features:**
- Extract skills and experience
- Identify education level
- Calculate ATS compatibility score
- Generate improvement suggestions

**Usage:**
```python
from proximaai.tools.resume_tools import ResumeParserTool

parser = ResumeParserTool()
result = parser._run(resume_text)
```

#### ResumeOptimizerTool
Optimizes resumes for specific job postings.

**Features:**
- Keyword matching analysis
- ATS optimization suggestions
- Job-specific improvements
- Match percentage calculation

### Career Coaching

#### CareerAdvisorTool
Provides personalized career advice and guidance.

**Features:**
- Career transition support
- Skill development recommendations
- Professional growth strategies
- Industry-specific advice

#### InterviewPreparationTool
Helps prepare for job interviews.

**Features:**
- Common interview questions
- Company research points
- Preparation strategies
- Practice scenarios

#### SkillDevelopmentTool
Creates skill development plans and tracks progress.

**Features:**
- Skill gap analysis
- Learning path creation
- Progress tracking
- Resource recommendations

### Job Search

#### JobSearchTool
Searches for job opportunities based on criteria.

**Features:**
- Multi-criteria job search
- Location and remote filtering
- Experience level matching
- Company-specific searches

#### JobAnalyzerTool
Analyzes job postings for insights and requirements.

**Features:**
- Requirement extraction
- Company culture analysis
- Red/green flag identification
- Application tips generation

#### ApplicationTrackerTool
Tracks job applications and interview progress.

**Features:**
- Application status tracking
- Follow-up scheduling
- Interview coordination
- Progress monitoring

## Usage Examples

### Creating a Specialized Agent

```python
from proximaai.tools.tool_registry import tool_registry
import json

# Get the agent builder
agent_builder = tool_registry.get_tool("agent_builder")

# Create a resume analysis agent
agent_spec = {
    "name": "ResumeExpert",
    "description": "Expert resume analyzer and optimizer",
    "system_prompt": "You are a resume expert. Analyze resumes and provide optimization suggestions.",
    "tools": ["resume_parser", "resume_optimizer"],
    "temperature": 0.1
}

result = agent_builder._run(json.dumps(agent_spec))
print(result)
```

### Analyzing a Resume

```python
from proximaai.tools.resume_tools import ResumeParserTool

parser = ResumeParserTool()
resume_text = """
John Doe
Software Engineer
Experience: 5 years Python development
Skills: Python, JavaScript, AWS
"""

analysis = parser._run(resume_text)
print(analysis)
```

### Searching for Jobs

```python
from proximaai.tools.job_search import JobSearchTool
import json

job_search = JobSearchTool()
criteria = {
    "job_title": "Software Engineer",
    "location": "San Francisco",
    "remote_only": True,
    "experience_level": "senior"
}

jobs = job_search._run(json.dumps(criteria))
print(jobs)
```

## Integration with Main Agent

The tools are designed to work seamlessly with the main orchestrator agent:

```python
from proximaai.orchestrator.main_agent import agent
from proximaai.tools.tool_registry import tool_registry

# The main agent automatically has access to all tools
conversation = {
    "messages": [
        {"role": "user", "content": "Create a specialized agent for Python job search"}
    ]
}

response = agent.invoke(conversation)
print(response)
```

## Extending the Tools

To add a new tool:

1. Create a new tool class inheriting from `BaseTool`
2. Implement the `_run` method
3. Add the tool to the `ToolRegistry`
4. Update the `__init__.py` exports

Example:
```python
from langchain.tools import BaseTool

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Description of what this tool does"
    
    def _run(self, input_text: str) -> str:
        # Tool implementation
        return "Tool result"
```

## Running the Demo

To see the tools in action:

```bash
cd examples
python tool_demo.py
```

This will demonstrate:
- Tool registry functionality
- Agent builder capabilities
- Available tool categories
- Tool descriptions and usage

## Future Enhancements

Planned improvements:
- Integration with real search APIs (Google, Bing, etc.)
- Advanced NLP for resume parsing
- Machine learning for job matching
- Real-time job board integration
- Advanced interview simulation
- Skill assessment tools
- Networking and mentorship tools 