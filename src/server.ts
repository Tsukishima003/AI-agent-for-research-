import "dotenv/config";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { WebSocketServer } from "ws";
import { registerTools } from "./tools/index.js";

export function startServer(): void {
  const port = Number(process.env.PORT ?? process.env.MCP_PORT ?? 7800);
  const wss = new WebSocketServer({ port });

  const server = new Server({ name: "mcp-research-agent", version: "0.1.0" });
  registerTools(server);

  const anyServer = server as any;
  wss.on("connection", (socket) => {
    if (typeof anyServer.connectWebSocket === "function") {
      anyServer.connectWebSocket(socket as any);
    } else if (typeof anyServer.connect === "function") {
      anyServer.connect(socket as any);
    }
  });

  console.log(`MCP Research Agent server listening on ws://0.0.0.0:${port}`);
}


