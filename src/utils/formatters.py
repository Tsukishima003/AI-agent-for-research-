from typing import Dict


def format_citation_apa(meta: Dict) -> str:
    title = meta.get("title", "Untitled")
    year = meta.get("year", "n.d.")
    authors = ", ".join(meta.get("authors", [])) or "Anon."
    return f"{authors} ({year}). {title}."


def format_citation_mla(meta: Dict) -> str:
    title = meta.get("title", "Untitled")
    authors = ", ".join(meta.get("authors", [])) or "Anon."
    year = meta.get("year")
    year_part = f" {year}." if year else "."
    return f"{authors}. {title}.{year_part}"


def format_citation_chicago(meta: Dict) -> str:
    title = meta.get("title", "Untitled")
    authors = ", ".join(meta.get("authors", [])) or "Anon."
    year = meta.get("year", "n.d.")
    return f"{authors}. {year}. {title}."


def format_citation(style: str, meta: Dict) -> str:
    s = (style or "apa").lower()
    if s == "mla":
        return format_citation_mla(meta)
    if s == "chicago":
        return format_citation_chicago(meta)
    return format_citation_apa(meta)


