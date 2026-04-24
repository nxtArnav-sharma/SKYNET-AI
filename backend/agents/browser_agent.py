import asyncio
import urllib.parse
import re
from playwright.async_api import async_playwright
from backend.llm.gemini_engine import client

async def run_autonomous_browse(query: str) -> str:
    """Uses playwright to search DuckDuckGo, open top 3 links, extract text, and return report."""
    results = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            await page.goto(search_url, wait_until='domcontentloaded')
            
            links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('.result__url')).slice(0, 3).map(a => a.href);
            }''')
            
            if not links:
                await browser.close()
                return "INTELLIGENCE REPORT\n\nTopic: " + query + "\n\nSummary:\nNo valid results found."
            
            extracted_texts = []
            for link in links:
                try:
                    p2 = await context.new_page()
                    await p2.goto(link, timeout=10000, wait_until='domcontentloaded')
                    text = await p2.evaluate('document.body.innerText')
                    text = re.sub(r'\s+', ' ', text).strip()
                    extracted_texts.append(text[:1500])
                    await p2.close()
                except Exception:
                    pass
            
            await browser.close()
            
            combined_text = "\n---\n".join(extracted_texts)
            if not combined_text:
                return "INTELLIGENCE REPORT\n\nTopic: " + query + "\n\nSummary:\nFailed to extract content from results."
            
            try:
                summary_prompt = f"Format exactly as an INTELLIGENCE REPORT.\nTopic: {query}\n\nSummarize this raw data:\n{combined_text}"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=summary_prompt,
                )
                summary = response.text
                if "INTELLIGENCE REPORT" not in summary:
                    summary = f"INTELLIGENCE REPORT\n\nTopic: {query}\n\nSummary:\n{summary}"
                return summary
            except Exception as e:
                return f"INTELLIGENCE REPORT\n\nTopic: {query}\n\nSummary:\nExtracted data: {combined_text[:500]}..."
            
    except Exception as e:
        return f"INTELLIGENCE REPORT\n\nTopic: {query}\n\nSummary:\nError during autonomous browsing: {str(e)}"
