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
        