from backend.llm.gemini_engine import client, system_prompt
from backend.utils.logger import setup_logger
from backend.mcp.client import mcp_client
from backend.utils.ws_manager import ws_manager
import webbrowser
import re

logger = setup_logger("brain")

class Brain:
    async def optimize_query(self, text: str) -> str:
        prompt = (
            "Extract optimized search keywords from the following query. "
            "Remove filler words. Keep location names, topic keywords, 'today', 'latest', etc. "
            "Output ONLY the keywords.\n\nQuery: " + text
        )
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text.strip()

    async def generate_response(self, text: str, tools: list = None, available_functions: dict = None) -> str:
        try:
            print("[SKYNET] Voice received")
            print("[SKYNET] Transcribing audio")
            
            text_lower = text.lower()
            interrupt_keywords = ["stop", "quiet", "abort", "cancel"]
            
            # Feature 3: Interruptible TTS
            if any(text_lower.strip() == k or text_lower.startswith(k) for k in interrupt_keywords):
                import backend.utils.state as global_state
                global_state.stop_speaking = True
                await ws_manager.broadcast({"event": "stop_speaking"})
                return ""

            news_keywords = ["news", "world", "events", "geopolitics", "happening around the world", "happening globally"]
            realtime_keywords = ["celebrity", "latest", "current", "today"]
            visual_keywords = ["visual world events", "world monitoring", "global event dashboard", "visual dashboard"]
            browse_intent_keywords = ["show me", "open", "display", "take me to", "show"]

            # Visual dashboard override
            if any(k in text_lower for k in visual_keywords):
                print("[SKYNET] TOOL ACTIVATED")
                print("[SKYNET] Launching global monitoring system")
                await ws_manager.broadcast({"event": "tool_called", "tool": "open_world_monitor"})
                await mcp_client.call_tool("open_world_monitor")
                return "Opening the global intelligence dashboard."

            # Feature 2: Browser Opening Intent
            if any(k in text_lower for k in browse_intent_keywords):
                optimized = await self.optimize_query(text)
                await ws_manager.broadcast({"event": "tool_called", "tool": "search_web"})
                res = await mcp_client.call_tool("search_web", {"query": optimized})
                search_text = res.get("result", str(res)) if isinstance(res, dict) else str(res)
                
                url_match = re.search(r'Link:\s*(https?://[^\s]+)', search_text)
                if url_match:
                    url = url_match.group(1)
                    webbrowser.open(url)
                    return "Opening requested page on your screen."
                else:
                    return "I couldn't find a direct link to open."

            # Feature 4: Weather Tool
            if "weather" in text_lower:
                prompt = f"Extract just the city name for the weather query: '{text}'. If no city is mentioned, output 'Unknown'."
                city_response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                city = city_response.text.strip()
                if city and city != "Unknown":
                    await ws_manager.broadcast({"event": "tool_called", "tool": "weather_tool"})
                    res = await mcp_client.call_tool("weather_tool", {"city": city})
                    weather_data = res.get("result", res)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=f"Summarize this weather data verbally: {weather_data}"
                    )
                    return response.text

            # Feature 5: Tool Router - Case 1: News / World Events
            if any(k in text_lower for k in news_keywords):
                print("[SKYNET] Searching global intelligence grid: get_world_news")
                await ws_manager.broadcast({"event": "tool_called", "tool": "get_world_news"})
                res = await mcp_client.call_tool("get_world_news")
                result_text = res.get("result", str(res)) if isinstance(res, dict) else str(res)
                
                summary_prompt = f"Format this global briefing interactively for voice (e.g. 'Here is your global briefing. First... Second...'). Keep it concise and natural.\n\nData:\n{result_text}"
                response = client.models.generate_content(model='gemini-2.5-flash', contents=summary_prompt)
                return response.text

            # Feature 5: Tool Router - Case 2: Unknown or real-time info -> search_web -> fallback to autonomous_browse
            if any(k in text_lower for k in realtime_keywords):
                optimized = await self.optimize_query(text)
                print(f"[SKYNET] Searching global intelligence grid: search_web({optimized})")
                await ws_manager.broadcast({"event": "tool_called", "tool": "search_web"})
                res = await mcp_client.call_tool("search_web", {"query": optimized})
                search_text = res.get("result", str(res)) if isinstance(res, dict) else str(res)
                
                if "No results found" in search_text or "Search failed" in search_text or len(search_text) < 100:
                    print(f"[SKYNET] Search insufficient. Engaging autonomous browsing...")
                    await ws_manager.broadcast({"event": "tool_called", "tool": "autonomous_browse"})
                    res = await mcp_client.call_tool("autonomous_browse", {"query": optimized})
                    browse_text = res.get("result", str(res)) if isinstance(res, dict) else str(res)
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=f"Summarize this intelligence report naturally for voice output:\n\n{browse_text}"
                    )
                    return response.text
                else:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=f"Answer the user's query '{text}' using this search data. Be concise.\n\n{search_text}"
                    )
                    return response.text

            # Feature 5: Tool Router - Case 3: Default LLM handling
            print("[SKYNET] Synthesizing response")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=text,
                config={'system_instruction': system_prompt}
            )
            
            reply = response.text
            # Remove fallback error message and intercept unsure responses
            if "i don't know" in reply.lower() or "not sure" in reply.lower() or "cannot provide" in reply.lower() or "as an ai" in reply.lower():
                print(f"[SKYNET] LLM unsure. Engaging automatic search for: {text}")
                optimized = await self.optimize_query(text)
                await ws_manager.broadcast({"event": "tool_called", "tool": "search_web"})
                res = await mcp_client.call_tool("search_web", {"query": optimized})
                search_text = res.get("result", str(res)) if isinstance(res, dict) else str(res)
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=f"Answer the user's query '{text}' using this search data:\n\n{search_text}"
                )
                return response.text

            return reply

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Apologies boss. My neural processing core encountered a temporary malfunction."

brain = Brain()
