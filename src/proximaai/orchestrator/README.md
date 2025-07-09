# Longterm Memory and Node Caching

We use Supabase to host our Postgres database, connecting via an `AsyncPostgresStore` object. The connection string is provided as an environment variable.

ENV:
- Set connection string as `DB_URI`.

**Note:** The recommended pattern in [LangGraph's memory documentation][1]—using a content manager at the top of the graph and passing the store as a graph attribute—does not work in our setup. Instead, we must explicitly create and use the store *inside* each node function for it to work reliably.

For caching, LangGraph only documents the use of `InMemoryCache`, which is suitable for single-threaded or development environments. There is no official support or documentation for using Postgres or Redis as a cache backend. As a result, `InMemoryCache` is not recommended for concurrent or production systems.

To determine if a message was returned from cache, check for the `__metadata__` attribute in the graph's response. This attribute is only present when the graph is run with `stream="updates"`.

To demonstrate Node Cache with `ainvoke` or `astream`, run:
```python
uv run main_agent.py
```

**Cache Policy Examples:**

1. **TTL=5 seconds**: First run executes normally, second run uses cached results (no logging in stdout), third run with streaming shows cache metadata.

2. **TTL=1 second**: First run may use existing cache or execute normally, second run behaves same as first (logs show up in stdout), third run with streaming shows cache metadata.

[1]: https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/#trim-messages
[2]: https://langchain-ai.github.io/langgraph/concepts/low_level/?_gl=1*770lt4*_gcl_au*MzU0ODI5Mjk5LjE3NTE4NDQzOTE.*_ga*MTUxNTcwMjM0MC4xNzUxOTE2NTQy*_ga_47WX3HKKY2*czE3NTE5OTE4OTEkbzQkZzAkdDE3NTE5OTE4OTIkajU5JGwwJGgw#node-caching
