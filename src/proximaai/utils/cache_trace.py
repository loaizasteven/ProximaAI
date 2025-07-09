from typing import Any

from langsmith.run_helpers import traceable
from langgraph.store.base import BaseStore

@traceable(name="store.aput")
async def traced_aput(
    store: BaseStore, 
    /,
    *,
    namespace: tuple[str, ...], 
    key: str, 
    value: Any
    ):
    return await store.aput(namespace=namespace, key=key, value=value)

@traceable(name="store.asearch")
async def traced_asearch(
    store: BaseStore, 
    /, 
    *, 
    namespace: tuple[str, ...], 
    query: str | None = None, 
    filter: dict[str, Any] | None = None, 
    limit: int = 10, 
    offset: int = 0, 
    refresh_ttl: bool | None = None
    ):
    return await store.asearch(
        namespace, 
        query=query, 
        filter=filter, 
        limit=limit, 
        offset=offset, 
        refresh_ttl=refresh_ttl
    )