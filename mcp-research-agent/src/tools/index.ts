import { Server } from "@modelcontextprotocol/sdk/server/index.js";

export function registerTools(server: Server): void {
  // Placeholder: register tool handlers here
  server.tool("ping", {
    description: "Health check",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    async handler() {
      return { ok: true } as any;
    },
  });
}


