import contextlib
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from proximaai.utils.auth import is_valid_key
from starlette.responses import JSONResponse

from proximaai.mcp.llama_parse_server import llama_parse_mcp
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(llama_parse_mcp.session_manager.run())
        yield


class SupabaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("What the Helly")
        auth_header = request.headers.get("x-api-key")
        if not auth_header:
            return JSONResponse({"detail": "Missing API key"}, status_code=401)
        valid, user_id = await is_valid_key(auth_header)
        if not valid:
            return JSONResponse({"detail": "Invalid API key"}, status_code=401)
        # Optionally attach user_id to request.state
        request.state.user_id = user_id
        return await call_next(request)

app = FastAPI(lifespan=lifespan)
llama_app = llama_parse_mcp.streamable_http_app()
llama_app.add_middleware(SupabaseAuthMiddleware)
app.mount("/parse_document", llama_app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    PORT = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
