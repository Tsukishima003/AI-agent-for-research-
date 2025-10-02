import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerTools } from "./tools/index.js";

export async function startStdioServer() {
  const server = new Server(
    { name: "mcp-research-agent", version: "0.1.0" },
    {
      capabilities: {
        tools: {},
      },
    }
  );
  
  registerTools(server);

  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("MCP Research Agent stdio server started");
}