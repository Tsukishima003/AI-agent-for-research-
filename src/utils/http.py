import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class HttpClient:
    def __init__(self, timeout: float = 20.0):
        self._client = httpx.AsyncClient(timeout=timeout, headers={"User-Agent": "research-agent-mcp/0.1"})

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), retry=retry_if_exception_type(httpx.HTTPError))
    async def get_json(self, url: str, params: dict | None = None, headers: dict | None = None):
        resp = await self._client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4), retry=retry_if_exception_type(httpx.HTTPError))
    async def get_text(self, url: str, params: dict | None = None, headers: dict | None = None):
        resp = await self._client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.text

    async def close(self):
        await self._client.aclose()


