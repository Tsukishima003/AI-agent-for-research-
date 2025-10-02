import asyncio
import json
import os
from typing import Any, Dict

from tools.web_search import WebSearchTools
from tools.academic import AcademicTools
from tools.content import ContentTools
from tools.analysis import AnalysisTools
from resources.sources import SourceLibrary
from resources.notes import ResearchNotes
from utils.validators import validate_required_fields


class MCPServer:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.sources = SourceLibrary()
        self.notes = ResearchNotes()
        self.web = WebSearchTools(settings, self.sources)
        self.academic = AcademicTools(settings, self.sources)
        self.content = ContentTools(settings)
        self.analysis = AnalysisTools(settings)

    async def tool_search_web(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["query"]) 
        num_results = int(params.get("num_results", 10))
        date_range = params.get("date_range")
        results = await self.web.search_web(params["query"], num_results=num_results, date_range=date_range)
        return {"results": results}

    async def tool_fetch_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["url"]) 
        extract_text_only = bool(params.get("extract_text_only", True))
        content = await self.content.fetch_content(params["url"], extract_text_only=extract_text_only)
        return {"content": content}

    async def tool_search_academic(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["query"]) 
        databases = params.get("databases", ["arxiv", "pubmed"]) 
        publication_years = params.get("publication_years")
        results = await self.academic.search_academic(params["query"], databases=databases, publication_years=publication_years)
        return {"results": results}

    async def tool_analyze_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["text", "analysis_type"]) 
        return {
            "result": await self.analysis.analyze_content(params["text"], params["analysis_type"]) 
        }

    async def tool_save_research_note(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["content"]) 
        note = self.notes.save_note(params["content"], tags=params.get("tags", []), source_url=params.get("source_url"))
        return {"note": note}

    async def tool_synthesize_findings(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["topic", "sources"]) 
        synthesis = await self.analysis.synthesize_findings(params["topic"], params["sources"]) 
        return {"synthesis": synthesis}

    async def tool_generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        validate_required_fields(params, ["format", "sections"]) 
        report = await self.analysis.generate_report(
            report_format=params["format"],
            sections=params["sections"],
            sources=params.get("sources", []),
        )
        return {"report": report}


def load_settings() -> Dict[str, Any]:
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "settings.json")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def main() -> None:
    settings = load_settings()
    server = MCPServer(settings)

    # Minimal CLI loop for local testing; MCP wiring can be added later or via adapter
    print("Research Agent MCP Server ready. Available tools: search_web, fetch_content, search_academic, analyze_content, save_research_note, synthesize_findings, generate_report")
    await asyncio.sleep(0)  # placeholder to keep loop-friendly signature


if __name__ == "__main__":
    asyncio.run(main())


