from langgraph_sdk import Auth
from typing import Any

import os
from supabase import AsyncClient, acreate_client

from gotrue.types import User

auth = Auth()
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_KEY")


async def is_valid_key(auth_header: Any,):
    if isinstance(auth_header, bytes):
        auth_header = auth_header.decode()

    scheme, token = auth_header.split(" ")
    user: User | None = None
    if url and key:
        supabase: AsyncClient | None = await acreate_client(url, key)
    else:
        supabase = None
    if not supabase:
        raise Auth.exceptions.HTTPException(
            status_code=500,
            detail="Supabase client not initialized"
        )
    elif scheme != "Bearer":
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )
    
    try:
        data = await supabase.auth.get_user(jwt=token)
        if data:
            user = data.user
            return user.aud=="authenticate", user.id
    except BaseException as e:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return False, None

@auth.authenticate
async def authenticate(method: str,
        path: str,
        headers: dict[bytes, bytes]) -> Auth.types.MinimalUserDict:
    # Validate credentials (e.g., API key, JWT token)
    if method == 'OPTIONS':
         return {
        "identity": 'anonymous',        
        "is_authenticated": False,      
    }
    auth_header = headers.get(b'x-api-key')
    valid, user_id = await is_valid_key(auth_header)

    # Return user info - only identity and is_authenticated are required
    # Add any additional fields you need for authorization
    return {
        "identity": user_id or 'unknown',        # Required: unique user identifier
        "is_authenticated": True if valid else False,      # Optional: assumed True by default
        "permissions": ["read", "write"], # Optional: for permission-based auth
    }

@auth.on
async def add_owner(
    ctx: Auth.types.AuthContext,  # Contains info about the current user
    value: dict,  # The resource being created/accessed
):
    """Make resources private to their creator."""
    # Examples:
    # ctx: AuthContext(
    #     permissions=[],
    #     user=ProxyUser(
    #         identity='user1',
    #         is_authenticated=True,
    #         display_name='user1'
    #     ),
    #     resource='threads',
    #     action='create_run'
    # )
    # value: 
    # {
    #     'thread_id': UUID('1e1b2733-303f-4dcd-9620-02d370287d72'),
    #     'assistant_id': UUID('fe096781-5601-53d2-b2f6-0d3403f7e9ca'),
    #     'run_id': UUID('1efbe268-1627-66d4-aa8d-b956b0f02a41'),
    #     'status': 'pending',
    #     'metadata': {},
    #     'prevent_insert_if_inflight': True,
    #     'multitask_strategy': 'reject',
    #     'if_not_exists': 'reject',
    #     'after_seconds': 0,
    #     'kwargs': {
    #         'input': {'messages': [{'role': 'user', 'content': 'Hello!'}]},
    #         'command': None,
    #         'config': {
    #             'configurable': {
    #                 'langgraph_auth_user': ... Your user object...
    #                 'langgraph_auth_user_id': 'user1'
    #             }
    #         },
    #         'stream_mode': ['values'],
    #         'interrupt_before': None,
    #         'interrupt_after': None,
    #         'webhook': None,
    #         'feedback_keys': None,
    #         'temporary': False,
    #         'subgraphs': False
    #     }
    # }
    raise Auth.exceptions.HTTPException(
        status_code=403,
        detail="User lacks the required permissions.",
    )

# Matches the "thread" resource and all actions - create, read, update, delete, search
# Since this is **more specific** than the generic @auth.on handler, it will take precedence
# over the generic handler for all actions on the "threads" resource
@auth.on.threads
async def on_thread_create(
    ctx: Auth.types.AuthContext,
    value: dict
):
    if "write" not in ctx.permissions:
        raise Auth.exceptions.HTTPException(
            status_code=403,
            detail="User lacks the required permissions."
        )
    # Setting metadata on the thread being created
    # will ensure that the resource contains an "owner" field
    # Then any time a user tries to access this thread or runs within the thread,
    # we can filter by owner
    metadata = value.setdefault("metadata", {})
    metadata["owner"] = ctx.user.identity
    return {"owner": ctx.user.identity}
        
# Assumes you organize information in store like (user_id, resource_type, resource_id)
# TODO: Currently not passing the store object to the graph state, explicitly creating client per node
@auth.on.store()
async def authorize_store(ctx: Auth.types.AuthContext, value: dict):
    # The "namespace" field for each store item is a tuple you can think of as the directory of an item.
    namespace: tuple = value["namespace"]
    print('yerrr', namespace)
    assert namespace[0] == ctx.user.identity, "Not authorized"
