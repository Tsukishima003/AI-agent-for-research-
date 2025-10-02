import asyncio

from server import MCPServer, load_settings


async def run_demo() -> None:
    settings = load_settings()
    server = MCPServer(settings)

    print("== Web Search ==")
    web = await server.tool_search_web({"query": "latest AI alignment overview", "num_results": 3})
    print(web)

    print("== Academic Search ==")
    acad = await server.tool_search_academic({"query": "transformer interpretability", "databases": ["arxiv", "pubmed"]})
    print(acad)

    print("== Analyze ==")
    analysis = await server.tool_analyze_content({"text": "Transformers are powerful models...", "analysis_type": "summarize"})
    print(analysis)

    print("== Report ==")
    sources = (web.get("results") or [])[:2] + (acad.get("results") or [])[:2]
    report = await server.tool_generate_report({
        "format": "markdown",
        "sections": [
            {"title": "Introduction", "content": "This is a demo report."},
            {"title": "Findings", "content": "Summary of initial findings."}
        ],
        "sources": sources,
    })
    print(report["report"]["content"])


if __name__ == "__main__":
    asyncio.run(run_demo())


