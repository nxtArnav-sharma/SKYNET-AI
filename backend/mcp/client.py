import httpx

class MCPClient:
    async def call_tool(self, tool_name: str, args: dict = None):
        if args is None:
            args = {}
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(
                    f"http://127.0.0.1:8000/tools/{tool_name}",
                    json=args,
                    timeout=30.0
                )
                if res.status_code == 200:
                    return res.json()
                else:
                    return f"Error: {res.status_code} - {res.text}"
            except Exception as e:
                return f"MCP Client Error: {str(e)}"

mcp_client = MCPClient()
