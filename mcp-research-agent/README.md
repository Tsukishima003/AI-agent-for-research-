## Research Agent MCP (Python)

Minimal scaffold of an MCP-like server exposing research tools for automated information gathering, analysis, and reporting. This scaffold focuses on modularity, error handling stubs, and extensibility.

### Setup
1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2. Configure API keys via environment variables (preferred) or `config/settings.json`.
   - `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` for Google Custom Search (recommended: do NOT commit keys).
   - You can leave keys empty in `settings.json`; env vars will override.

Security note: avoid committing secrets. If you've placed real keys in `config/settings.json`, rotate them and move them into env vars.

### Run
```bash 
python src/server.py
```

### Tools (preview)
- search_web(query, num_results, date_range)    
- fetch_content(url, extract_text_only)
- search_academic(query, databases, publication_years)
- analyze_content(text, analysis_type)
- save_research_note(content, tags, source_url)
- synthesize_findings(topic, sources)
- generate_report(format, sections, sources)

This scaffold includes rate limiting, simple validators, and in-memory resources. Replace mock logic with real integrations (Google/Bing/DDG, arXiv/PubMed, content extraction libraries) as you expand.

# MCP Research Agent (MCP Server)

TypeScript MCP server providing research tools for AI assistants (Claude, etc.).

## Quick start

1. Create `.env` from `.env.example` and fill keys
2. Install deps: `npm i`
3. Build: `npm run build`
4. Run: `npm start`

Server listens on `ws://localhost:7800` by default. Override with `MCP_PORT`.

## Features (planned)
- Web search & fetch with rate limiting
- Academic sources (arXiv, PubMed, Scholar)
- Citation formatting (APA/MLA/Chicago)
- Summarization, clustering, verification, bias heuristics
- Notes, tagging, provenance, export (Markdown/HTML)
Y