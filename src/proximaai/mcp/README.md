# MCP Tools (Model Context Protocol)

## What are MCP Tools?
MCP tools are external tools or services that communicate with your main application via the Model Context Protocol, often using subprocesses and stdio for communication. They can be written in any language and are typically launched as separate server processes.

## How Were MCP Tools Used?
- Previously, tools like Perplexity search were implemented as MCP servers (e.g., `ppl-mcp-server.py`) or using `docker`/`npx` commands.
- The main app would launch these as subprocesses and communicate over stdio using the MCP protocol.
- This allowed for language-agnostic, modular tool development.

## Issues Faced When Deploying to LangGraph Studio
- **Subprocesses and custom servers did not seem to have support in the platform.**
