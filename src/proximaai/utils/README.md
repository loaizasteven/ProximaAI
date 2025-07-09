# Utility Functions
This directory hosts utility functions used throughout the project.

## LangSmith Traceables
LangSmith is a powerful tracing and observability tool for LLM applications, allowing you to monitor, debug, and analyze the execution of your language model pipelines. By default, LangSmith traces model invocations, tool calls, and agent steps, providing visibility into the flow and performance of your system.

However, in complex agent graphs, there are often additional operations—such as cache lookups, database queries, or custom logic—that are not automatically traced. To ensure full observability, it's important to create custom traces for these steps.

For example, in this project, we define custom traceable wrappers in `cache_trace.py` for key `BaseStore` operations (such as `aput` and `asearch`) that interact with Postgres. By decorating these methods with `@traceable`, we capture and log these database interactions in LangSmith, making it easier to debug and optimize the data layer of the agent graph.
