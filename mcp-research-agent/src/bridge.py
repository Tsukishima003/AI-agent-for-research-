import asyncio
import json
import sys

from server import MCPServer, load_settings


async def main() -> None:
    raw = sys.stdin.read()
    req = json.loads(raw) if raw else {}
    tool = req.get("tool")
    params = req.get("params", {})
    settings = load_settings()
    server = MCPServer(settings)

    mapping = {
        "search_web": server.tool_search_web,
        "fetch_content": server.tool_fetch_content,
        "search_academic": server.tool_search_academic,
        "analyze_content": server.tool_analyze_content,
        "save_research_note": server.tool_save_research_note,
        "synthesize_findings": server.tool_synthesize_findings,
        "generate_report": server.tool_generate_report,
    }
    if tool not in mapping:
        print(json.dumps({"error": f"unknown tool: {tool}"}))
        return
    try:
        result = await mapping[tool](params)
        print(json.dumps({"ok": True, "data": result}))
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))


if __name__ == "__main__":
    asyncio.run(main())


