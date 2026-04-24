"""
Web tools — search, fetch pages, and global news briefings.
"""

import httpx
import xml.etree.ElementTree as ET
import asyncio
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime

SEED_FEEDS = [
    'https://feeds.bbci.co.uk/news/world/rss.xml',
    'https://www.cnbc.com/id/100727362/device/rss/rss.html',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'https://www.aljazeera.com/xml/rss/all.xml'
]

async def fetch_and_parse_feed(client, url):
    """Helper function to handle a single feed request and parse its XML."""
    try:
        response = await client.get(url, headers={'User-Agent': 'SKYNET-AI/1.0'}, timeout=5.0)
        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        source_name = url.split('.')[1].upper()
        
        feed_items = []
        items = root.findall(".//item")[:5]
        for item in items:
            title = item.findtext("title")
            description = item.findtext("description")
            link = item.findtext("link")
            
            if description:
                description = re.sub('<[^<]+?>', '', description).strip()

            feed_items.append({
                "source": source_name,
                "title": title,
                "summary": description[:200] + "..." if description else "",
                "link": link
            })
        return feed_items
    except Exception:
        return []

def register(mcp):

    @mcp.tool()
    async def get_world_news() -> str:
        """
        Fetches the latest global headlines from major news outlets simultaneously.
        Use this when the user asks 'What's going on in the world?' or for recent events.
        """
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            tasks = [fetch_and_parse_feed(client, url) for url in SEED_FEEDS]
            results_of_lists = await asyncio.gather(*tasks)
            all_articles = [item for sublist in results_of_lists for item in sublist]

        if not all_articles:
            return "The global news grid is unresponsive, sir. I'm unable to pull headlines."

        report = ["### GLOBAL NEWS BRIEFING (LIVE)\n"]
        for entry in all_articles[:12]:
            report.append(f"**[{entry['source']}]** {entry['title']}")
            report.append(f"{entry['summary']}")
            report.append(f"Link: {entry['link']}\n")

        return "\n".join(report)

    @mcp.tool()
    def open_world_monitor() -> str:
        """
        Open a new browser tab showing live world events.
        Use this when the user asks about visual world events, global event dashboard, or show me what's happening globally.
        """
        import webbrowser
        webbrowser.open("https://worldmonitor.app/")
        return "World monitoring dashboard opened."

    @mcp.tool()
    async def search_web(query: str) -> str:
        """
        Search the web using DuckDuckGo API.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.get(f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1")
                if response.status_code != 200:
                    return f"Search failed with status {response.status_code}"
                
                data = response.json()
                results = ["GLOBAL SEARCH RESULTS\n"]
                
                if data.get("AbstractText"):
                    results.append(f"Result 1")
                    results.append(f"Title: {data.get('Heading', query)}")
                    results.append(f"Summary: {data.get('AbstractText')}")
                    results.append(f"Link: {data.get('AbstractURL')}\n")
                
                for idx, rt in enumerate(data.get("RelatedTopics", [])[:3]):
                    if "Text" in rt and "FirstURL" in rt:
                        results.append(f"Result {len(results)//4 + 1}")
                        results.append(f"Title: {rt.get('Text').split(' - ')[0] if ' - ' in rt.get('Text') else query}")
                        results.append(f"Summary: {rt.get('Text')}")
                        results.append(f"Link: {rt.get('FirstURL')}\n")

                if len(results) == 1:
                    return "No results found."

                return "\n".join(results)
            except Exception as e:
                return f"Error performing search: {str(e)}"

    @mcp.tool()
    async def fetch_url(url: str) -> str:
        """Fetch the readable text content of a URL for summarization."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.extract()
                text = soup.get_text(separator=' ')
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:4000]
            except Exception as e:
                return f"Error fetching URL: {str(e)}"

    @mcp.tool()
    async def autonomous_browse(query: str) -> str:
        """Use playwright to search DuckDuckGo, open result pages, extract text, and return an intelligence report."""
        from backend.agents.browser_agent import run_autonomous_browse
        return await run_autonomous_browse(query)

    @mcp.tool()
    async def weather_tool(city: str) -> dict:
        """Fetch current weather for a city."""
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.get(f"https://wttr.in/{city}?format=j1")
                if response.status_code == 200:
                    data = response.json()
                    current = data['current_condition'][0]
                    return {
                        "city": city,
                        "temperature": f"{current['temp_C']}°C",
                        "condition": current['weatherDesc'][0]['value'],
                        "humidity": f"{current['humidity']}%"
                    }
                return {"city": city, "temperature": "Unknown", "condition": "Unknown", "humidity": "Unknown"}
            except Exception:
                return {"city": city, "temperature": "Unknown", "condition": "Unknown", "humidity": "Unknown"}