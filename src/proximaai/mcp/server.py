import contextlib
from fastapi import FastAPI
from .math_server import mcp as math_mcp
import os


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/math", math_mcp.streamable_http_app())


if __name__ == "__main__":
    import uvicorn

    PORT = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
