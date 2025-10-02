import asyncio
import os
from typing import Any, Dict, List, Optional

from utils.rate_limiters import AsyncRateLimiter
from utils.http import HttpClient
from utils.cache import TTLCache


class WebSearchTools:
    def __init__(self, settings: Dict[str, Any], sources):
        self.settings = settings
        self.sources = sources
        rps = settings.get("rate_limits", {}).get("web", 1.0)
        self.rate_limiter = AsyncRateLimiter(rps=float(rps))
        self.http = HttpClient()
        self.cache = TTLCache(ttl_seconds=300)

    async def _google_cse(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        api_key = os.getenv("GOOGLE_API_KEY") or self.settings.get("providers", {}).get("google", {}).get("api_key")
        cse_id = os.getenv("GOOGLE_CSE_ID") or self.settings.get("providers", {}).get("google", {}).get("cse_id")
        if not api_key or not cse_id:
            return []
        params = {"key": api_key, "cx": cse_id, "q": query, "num": min(num_results, 10)}
        data = await self.http.get_json("https://www.googleapis.com/customsearch/v1", params=params)
        items = []
        for it in data.get("items", []):
            item = {
                "title": it.get("title"),
                "url": it.get("link"),
                "snippet": it.get("snippet"),
                "source": "google",
                "date": it.get("pagemap", {}).get("metatags", [{}])[0].get("article:published_time"),
            }
            items.append(item)
        return items

    async def _ddg(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}
        data = await self.http.get_json("https://api.duckduckgo.com/", params=params)
        items: List[Dict[str, Any]] = []
        if data.get("AbstractURL"):
            items.append({
                "title": data.get("Heading"),
                "url": data.get("AbstractURL"),
                "snippet": data.get("AbstractText"),
                "source": "duckduckgo",
                "date": None,
            })
        for r in data.get("RelatedTopics", [])[: max(0, num_results - len(items))]:
            if isinstance(r, dict) and r.get("FirstURL"):
                items.append({
                    "title": r.get("Text"),
                    "url": r.get("FirstURL"),
                    "snippet": r.get("Text"),
                    "source": "duckduckgo",
                    "date": None,
                })
        return items

    async def search_web(self, query: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict[str, Any]]:
        cache_key = f"web:{query}:{num_results}:{date_range}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        await self.rate_limiter.acquire()
        results: List[Dict[str, Any]] = []
        # Prefer Google CSE if configured
        google_items = await self._google_cse(query, num_results)
        results.extend(google_items)
        if len(results) < num_results:
            ddg_items = await self._ddg(query, num_results - len(results))
            results.extend(ddg_items)
        # Track sources
        for item in results[:num_results]:
            if item.get("url"):
                self.sources.add_source(item["url"], metadata=item)
        results = results[:num_results]
        self.cache.set(cache_key, results)
        return results


