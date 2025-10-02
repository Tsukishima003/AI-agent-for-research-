import { startServer } from "./server.js";
import { startHealthServer } from "./health.js";

async function main() {
  // Check if we should use stdio mode (for Claude Desktop)
  const useStdio = process.env.MCP_TRANSPORT === "stdio" || process.argv.includes("--stdio");

  if (useStdio) {
    const { startStdioServer } = await import("./stdio-server.js");
    await startStdioServer();
  } else {
    const port = Number(process.env.PORT ?? 7800);
    startServer();
    startHealthServer(port);
  }
}

main().catch((error) => {
  console.error("Failed to start:", error);
  process.exit(1);
});