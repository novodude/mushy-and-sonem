"""
core/web_tools.py — search the web and read a page's content. Same libraries MVV
uses (ddgs, crawl4ai) so there's nothing new to install if you've already got MVV
running on this box.
"""

import asyncio
from ddgs import DDGS
from crawl4ai import AsyncWebCrawler

MAX_RESULTS = 5


async def h_search(params: dict, ctx) -> str:
    query = params.get("query")
    if not query:
        return "Need a query."

    try:
        results = await asyncio.to_thread(
            lambda: list(DDGS().text(query, max_results=MAX_RESULTS))
        )
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return f"No results for '{query}'."

    lines = []
    for r in results:
        title = r.get("title", "untitled")
        url = r.get("href") or r.get("url", "")
        snippet = r.get("body", "")
        lines.append(f"- {title} ({url})\n  {snippet}")
    return "\n".join(lines)


async def h_fetch_page(params: dict, ctx) -> str:
    url = params.get("url")
    if not url:
        return "Need a url."

    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
        content = result.markdown or result.cleaned_html or ""
        if not content.strip():
            return f"Fetched '{url}' but got no readable content."
        return content
    except Exception as e:
        return f"Couldn't fetch '{url}': {e}"


TOOLS = {
    "search": h_search,
    "fetch_page": h_fetch_page,
}
