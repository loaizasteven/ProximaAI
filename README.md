# ProximaAI: Multi-Agent Job Search & Resume Assistant

ProximaAI is an AI-powered job search and resume assistant inspired by Anthropic's multi-agent research system. It leverages multi-agent technology and the Lang ecosystem to accelerate your career journey.

## Project Vision
- **AI-powered job search**: Automate job discovery, matching, and application.
- **Resume assistant**: Optimize and tailor your resume for each opportunity.
- **Multi-agent system**: Specialized agents collaborate to deliver results.

## Architecture Overview
ProximaAI mirrors the architecture described in Anthropic's "How we built our multi-agent research system":

- **Agents**: Specialized AI agents (e.g., Job Finder, Resume Optimizer, Application Tracker).
- **Orchestrator**: Manages agent communication, task assignment, and workflow.
- **Tools**: Integrations with external APIs (job boards, resume parsers, LangChain, etc.).
- **Interface**: User-facing CLI or web interface.
- **Data**: Storage, models, and evaluation utilities.

```mermaid
graph TD;
  UI["User Interface (CLI/Web)"] -->|"User Input"| ORCH["Orchestrator"]
  ORCH -->|"Assigns Tasks"| AGENTS["Agents"]
  AGENTS -->|"Use Tools"| TOOLS["Tools & Integrations"]
  AGENTS -->|"Store/Retrieve"| DATA["Data & Evaluation"]
  ORCH -->|"Coordinates"| AGENTS
```

## Directory Structure
```plaintext
src/
  proximaai/
    agents/         # Agent definitions and logic
    orchestrator/   # Multi-agent orchestration and communication
    tools/          # Integrations (LangChain, job APIs, resume parsers, etc.)
    interface/      # User interfaces (CLI, web, etc.)
    data/           # Data models, storage, and evaluation
    utils/          # Shared utilities/helpers
    __init__.py
  tests/
    agents/
    orchestrator/
    tools/
    interface/
    data/
    utils/
scripts/            # Dev scripts, data importers, etc.
```

**Why `src/`?**
- Keeps the root clean and avoids import issues.
- Follows modern Python best practices for applications.
- Scales well for research and production.

## Quickstart
1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/ProximaAI.git
   cd ProximaAI
   ```
2. **Install dependencies:**
   ```bash
   pip install -e .
   ```
3. **Run the app (placeholder):**
   ```bash
   python -m src.proximaai.interface.cli
   ```

## Next Steps
- Implement agent classes in `src/proximaai/agents/`
- Build the orchestrator in `src/proximaai/orchestrator/`
- Integrate tools and APIs in `src/proximaai/tools/`
- Develop the user interface in `src/proximaai/interface/`
- Add tests in `src/tests/`

---
Inspired by Anthropic's [multi-agent research system](https://www.anthropic.com/research/how-we-built-our-multi-agent-research-system).
