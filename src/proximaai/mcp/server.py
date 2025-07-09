import contextlib
from fastapi import FastAPI
from proximaai.mcp.llama_parse_server import llama_parse_mcp
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(llama_parse_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/parse_document", llama_parse_mcp.streamable_http_app())


if __name__ == "__main__":
    import uvicorn

    PORT = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
