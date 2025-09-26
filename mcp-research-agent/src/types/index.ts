export type SearchEngine = "google" | "bing" | "duckduckgo" | "serpapi";

export interface WebSearchParams {
  query: string;
  engine: SearchEngine;
  numResults?: number;
  lang?: string;
  timeRange?: string;
}

export interface SearchResult {
  title: string;
  url: string;
  snippet?: string;
  source?: string;
}

export interface FetchedContent {
  url: string;
  contentType: string;
  text: string;
  html?: string;
  metadata?: Record<string, unknown>;
}

export interface Citation {
  id: string;
  title?: string;
  authors?: string[];
  journal?: string;
  year?: number;
  doi?: string;
  url?: string;
}


