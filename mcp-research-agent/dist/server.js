import "dotenv/config";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { WebSocketServer } from "ws";
import { registerTools } from "./tools/index.js";
export function startServer() {
    const port = Number(process.env.MCP_PORT ?? 7800);
    const wss = new WebSocketServer({ port });
    const server = new Server({ name: "mcp-research-agent", version: "0.1.0" });
    registerTools(server);
    wss.on("connection", (socket) => {
        server.connectWebSocket(socket);
    });
    console.log(`MCP Research Agent server listening on ws://localhost:${port}`);
}
//# sourceMappingURL=server.js.map