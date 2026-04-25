import json
import webbrowser
import re
from backend.llm.gemini_engine import client, system_prompt
from backend.utils.logger import setup_logger
from backend.mcp.client import mcp_client
from backend.utils.ws_manager import ws_manager

logger = setup_logger("brain")

SKYNET_PERSONALITY = """You are SKYNET. 
You are a highly intelligent, analytical system. 
You do not behave like a chatbot or assistant. 
You do not use casual or overly friendly language.
Your tone is calm, confident, and concise. 
Avoid filler phrases (e.g., "Hey", "Sure", "Of course").
You communicate in a smooth, natural, human-understandable way, but never informal.
Confidence is high. Emotion is low.
"""

class Brain:
    def _apply_skynet_style(self, text: str) -> str:
        replacements = {
            "Hey": "", "Hi": "", "Sure": "", "Of course": "", "No problem": "",
            "Certainly": "", "Absolutely": "", "Haha": "", "I think": "Analysis indicates",
            "maybe": "potentially", "I guess": "data suggests"
        }
        for k, v in replacements.items():
            text = re.sub(rf'\b{k}\b', v, text, flags=re.IGNORECASE)
        text = text.replace("!", ".").strip()
        text = re.sub(r'^[,\s\.]+', '', text)
        if text: text = text[0].upper() + text[1:]
        return text

    def _extract_search_text(self, data: str) -> str:
        """Improve extraction of useful text from search results."""
        # Simple extraction from our search_web output format
        snippets = re.findall(r"Summary: (.*?)\n", data)
        return " ".join(snippets)

    def _clean_headline(self, text: str) -> str:
        unwanted = ["Global Situation Update:", "Breaking News:", "Latest Update:", "World News:", "BCCI:", "BBC:", "CNBC:", "NYTIMES:", "ALJAZEERA:", "["]
        text = re.sub(r"<.*?>", "", text)
        for p in unwanted:
            if text.upper().startswith(p.upper()):
                if p == "[": text = re.sub(r"\[.*?\]", "", text).strip()
                else: text = text[len(p):].strip()
        return re.sub(r"^[:\-\s]+", "", text).strip()

    def _deduplicate_headlines(self, headlines: list) -> list:
        seen = set()
        clean = []
        for h in headlines:
            normalized = h.lower().strip()
            if normalized not in seen and len(normalized) > 15:
                seen.add(normalized)
                clean.append(h)
        return clean

    def _score_headline(self, text: str) -> int:
        text_lower = text.lower()
        score = 0
        HIGH = ["war", "conflict", "attack", "military", "china", "usa", "russia", "nato", "nuclear", "sanctions"]
        MEDIUM = ["economy", "inflation", "stock", "market", "ai", "technology", "government", "policy"]
        LOW = ["celebrity", "sports", "entertainment", "fashion", "hollywood"]
        for w in HIGH:
            if w in text_lower: score += 5
        for w in MEDIUM:
            if w in text_lower: score += 3
        for w in LOW:
            if w in text_lower: score -= 15
        return score

    def _rank_news(self, headlines: list) -> list:
        scored = sorted([(h, self._score_headline(h)) for h in headlines], key=lambda x: x[1], reverse=True)
        return [h for h, s in scored if s > -5][:3]

    def _generate_briefing(self, headlines: list) -> str:
        if not headlines: return "No critical global developments detected. Monitoring continues."
        body = " ".join([f"Update {i}. {h}." for i, h in enumerate(headlines, 1)])
        return f"Here are the most critical global developments at this time. {body} Monitoring continues."

    async def generate_response(self, text: str, tools: list = None, available_functions: dict = None) -> str:
        try:
            text_lower = text.lower()
            if any(text_lower.strip() == k or text_lower.startswith(k) for k in ["stop", "quiet", "abort", "cancel"]):
                import backend.utils.state as global_state
                from backend.tts.tts_engine import stop_audio
                global_state.stop_speaking = True
                stop_audio()
                await ws_manager.broadcast({"event": "stop_speaking"})
                return ""

            # 1. NEWS OVERRIDE
            if any(x in text_lower for x in ["news", "world news", "global news", "current events", "what's happening"]):
                if any(x in text_lower for x in ["show", "open", "display"]):
                    webbrowser.open("https://worldmonitor.app/")
                    await ws_manager.broadcast({"event": "tool_called", "tool": "open_world_monitor"})
                await ws_manager.broadcast({"event": "tool_called", "tool": "get_world_news"})
                tool_res = await mcp_client.call_tool("get_world_news")
                data = tool_res.get("result", str(tool_res))
                raw = re.findall(r"\*\*\[.*?\]\*\* (.*)", data) or [line.strip() for line in data.split("\n") if line.strip() and "Link:" not in line]
                headlines = self._deduplicate_headlines([self._clean_headline(h) for h in raw])
                return self._generate_briefing(self._rank_news(headlines))

            # 2. CLASSIFICATION
            # Bonus Fix: "trending", "best", "top" -> CHAT
            if any(x in text_lower for x in ["trending", "best", "top", "most popular", "most trending"]):
                intent = "CHAT"
                query = text
            else:
                decision_response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=text, config={'system_instruction': system_prompt}
                )
                try:
                    decision = json.loads(re.sub(r'```json\n?|\n?```', '', decision_response.text).strip())
                    intent = decision.get("intent", "CHAT")
                    query = decision.get("query", text)
                except:
                    intent = "CHAT"; query = text

            # 3. EXECUTION
            if intent == "CHAT":
                res = client.models.generate_content(
                    model='gemini-2.5-flash', contents=text, config={'system_instruction': SKYNET_PERSONALITY}
                )
                return self._apply_skynet_style(res.text)

            elif intent == "SEARCH_VISIBLE":
                await ws_manager.broadcast({"event": "tool_called", "tool": "search_web"})
                tool_res = await mcp_client.call_tool("search_web", {"query": query})
                data = tool_res.get("result", str(tool_res))
                url = re.search(r'Link:\s*(https?://[^\s]+)', data)
                webbrowser.open(url.group(1) if url else f"https://www.google.com/search?q={query}")
                return "Opening requested intelligence feed."

            elif intent == "SEARCH_HIDDEN":
                await ws_manager.broadcast({"event": "tool_called", "tool": "search_web"})
                tool_res = await mcp_client.call_tool("search_web", {"query": query})
                raw_results = tool_res.get('result', '')
                
                # Result Validation Layer
                cleaned_text = self._extract_search_text(raw_results)
                if not cleaned_text or len(cleaned_text.strip()) < 50:
                    return "Search results were insufficient to form a reliable analysis."

                report = client.models.generate_content(
                    model='gemini-2.5-flash', contents=f"Summarize concisely based on these results: {cleaned_text}",
                    config={'system_instruction': SKYNET_PERSONALITY}
                )
                return self._apply_skynet_style(report.text)

            return "Classification failed."

        except Exception as e:
            logger.error(f"Brain Error: {e}")
            return "System logic failure."

brain = Brain()
