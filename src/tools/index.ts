import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { spawn } from "child_process";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

export function registerTools(server: Server): void {
  // List all available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: "search_web",
        description: "Search the web for information",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query"
            },
            num_results: {
              type: "number",
              description: "Number of results to return",
              default: 5
            }
          },
          required: ["query"]
        }
      },
      {
        name: "fetch_content",
        description: "Fetch and extract content from a URL",
        inputSchema: {
          type: "object",
          properties: {
            url: {
              type: "string",
              description: "URL to fetch content from"
            }
          },
          required: ["url"]
        }
      },
      {
        name: "search_academic",
        description: "Search for academic papers and research",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Academic search query"
            },
            num_results: {
              type: "number",
              description: "Number of papers to return",
              default: 5
            }
          },
          required: ["query"]
        }
      },
      {
        name: "analyze_content",
        description: "Analyze content for key insights and themes",
        inputSchema: {
          type: "object",
          properties: {
            content: {
              type: "string",
              description: "Content to analyze"
            }
          },
          required: ["content"]
        }
      },
      {
        name: "save_research_note",
        description: "Save a research note or finding",
        inputSchema: {
          type: "object",
          properties: {
            title: {
              type: "string",
              description: "Note title"
            },
            content: {
              type: "string",
              description: "Note content"
            },
            tags: {
              type: "array",
              items: { type: "string" },
              description: "Tags for the note"
            }
          },
          required: ["title", "content"]
        }
      },
      {
        name: "synthesize_findings",
        description: "Synthesize multiple research findings into a coherent summary",
        inputSchema: {
          type: "object",
          properties: {
            findings: {
              type: "array",
              items: { type: "string" },
              description: "List of findings to synthesize"
            }
          },
          required: ["findings"]
        }
      },
      {
        name: "generate_report",
        description: "Generate a comprehensive research report",
        inputSchema: {
          type: "object",
          properties: {
            topic: {
              type: "string",
              description: "Research topic"
            },
            sections: {
              type: "array",
              items: { type: "string" },
              description: "Sections to include in the report"
            }
          },
          required: ["topic"]
        }
      }
    ]
  }));

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
    const { name, arguments: args } = request.params;
    
    try {
      const result = await callPythonBridge(name, args);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`
          }
        ],
        isError: true
      };
    }
  });
}

async function callPythonBridge(tool: string, params: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const python = spawn("python", ["src/bridge.py"], {
      cwd: process.cwd()
    });

    const input = JSON.stringify({ tool, params });
    let output = "";
    let errorOutput = "";

    python.stdout.on("data", (data) => {
      output += data.toString();
    });

    python.stderr.on("data", (data) => {
      errorOutput += data.toString();
      console.error("Python stderr:", data.toString());
    });

    python.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`Python bridge failed with code ${code}: ${errorOutput}`));
        return;
      }

      try {
        const result = JSON.parse(output);
        if (result.ok) {
          resolve(result.data);
        } else {
          reject(new Error(result.error || "Unknown error from Python bridge"));
        }
      } catch (e) {
        reject(new Error(`Failed to parse Python output: ${output}`));
      }
    });

    python.stdin.write(input);
    python.stdin.end();
  });
}