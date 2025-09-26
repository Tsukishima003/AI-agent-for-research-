import asyncio
from typing import Any, Dict, List, Optional

from utils.rate_limiters import AsyncRateLimiter
from utils.http import HttpClient


class AcademicTools:
    def __init__(self, settings: Dict[str, Any], sources):
        self.settings = settings
        self.sources = sources
        rps = settings.get("rate_limits", {}).get("academic", 1.0)
        self.rate_limiter = AsyncRateLimiter(rps=float(rps))
        self.http = HttpClient()

    async def _search_arxiv(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        params = {"search_query": f"all:{query}", "start": 0, "max_results": min(num_results, 10)}
        text = await self.http.get_text("http://export.arxiv.org/api/query", params=params)
        # Very light parsing to extract entries (avoid heavy deps for scaffold)
        results: List[Dict[str, Any]] = []
        for chunk in text.split("<entry>")[1:]:
            title = (chunk.split("<title>")[1].split("</title>")[0]).strip() if "<title>" in chunk else None
            link = None
            if "<id>" in chunk:
                link = chunk.split("<id>")[1].split("</id>")[0].strip()
            summary = (chunk.split("<summary>")[1].split("</summary>")[0].strip() if "<summary>" in chunk else None)
            if link:
                results.append({
                    "title": title,
                    "url": link,
                    "abstract": summary,
                    "database": "arxiv",
                })
        return results[:num_results]

    async def _search_pubmed(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": min(num_results, 10)}
        data = await self.http.get_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params=params)
        ids = data.get("esearchresult", {}).get("idlist", [])
        results: List[Dict[str, Any]] = []
        for pmid in ids:
            results.append({
                "title": f"PubMed PMID {pmid}",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "database": "pubmed",
            })
        return results

    async def search_academic(self, query: str, databases: List[str], publication_years: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        await self.rate_limiter.acquire()
        results: List[Dict[str, Any]] = []
        dbs = [d.lower() for d in databases] if databases else ["arxiv", "pubmed"]
        if "arxiv" in dbs:
            results.extend(await self._search_arxiv(query, 10))
        if "pubmed" in dbs:
            results.extend(await self._search_pubmed(query, 10))
        for item in results:
            if item.get("url"):
                self.sources.add_source(item["url"], metadata=item)
        return results


