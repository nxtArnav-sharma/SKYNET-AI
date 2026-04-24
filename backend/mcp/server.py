import logging
import uvicorn
from fastapi import FastAPI, Request
from backend.mcp.tools import web
from backend.mcp.tools import system
from backend.mcp.tools import utils
from backend.utils.logger import setup_logger

logger = setup_logger("mcp-server")

app = FastAPI(title="SKYNET MCP Server")

class DummyMCP:
    def __init__(self):
        self._tools = {}
    
    def tool(self):
        def decorator(func):
            self._tools[func.__name__] = func
            return func
        return decorator

# Initialize and register tools
mcp = DummyMCP()
web.register(mcp)
system.register(mcp)
utils.register(mcp)

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    try:
        args = await request.json() if await request.body() else {}
        if tool_name not in mcp._tools:
            return {"error": f"Tool '{tool_name}' not found"}
            
        func = mcp._tools[tool_name]
        
        import inspect
        if inspect.iscoroutinefunction(func):
            result = await func(**args)
        else:
            result = func(**args)
            
        return {"result": result}
    except Exception as e:
        logger.error(f"Error calling tool {tool_name}: {str(e)}")
        return {"error": str(e)}

def main():
    logger.info("Starting FastMCP REST Server on 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
