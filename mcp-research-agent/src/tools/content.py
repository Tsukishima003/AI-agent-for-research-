import asyncio
from typing import Any, Dict

from utils.rate_limiters import AsyncRateLimiter
from utils.http import HttpClient

try:
    import trafilatura  # type: ignore
except Exception:
    trafilatura = None  # fallback

try:
    from pdfminer.high_level import extract_text as pdf_extract_text  # type: ignore
except Exception:
    pdf_extract_text = None


class ContentTools:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        rps = settings.get("rate_limits", {}).get("content", 2.0)
        self.rate_limiter = AsyncRateLimiter(rps=float(rps))
        self.http = HttpClient()

    async def fetch_content(self, url: str, extract_text_only: bool = True) -> Dict[str, Any]:
        await self.rate_limiter.acquire()
        # Simple handling: PDFs vs HTML
        is_pdf = url.lower().endswith(".pdf")
        if is_pdf and pdf_extract_text is not None:
            # Download to memory then extract
            # For simplicity, pdfminer needs a file path or bytes via io.BytesIO
            import io
            resp_bytes = await self.http._client.get(url)
            resp_bytes.raise_for_status()
            with io.BytesIO(resp_bytes.content) as bio:
                text = pdf_extract_text(bio)
            return {"url": url, "text": text or "", "html": None, "metadata": {"content_type": "application/pdf"}}

        # HTML/text
        html = await self.http.get_text(url)
        text = None
        if trafilatura is not None:
            text = trafilatura.extract(html) or None
        content = {
            "url": url,
            "text": text if extract_text_only else (text or ""),
            "html": None if extract_text_only else html,
            "metadata": {"content_type": "text/html"},
        }
        return content


