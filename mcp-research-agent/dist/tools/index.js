export function registerTools(server) {
    // Placeholder: register tool handlers here
    server.tool("ping", {
        description: "Health check",
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        async handler() {
            return { ok: true };
        },
    });
}
//# sourceMappingURL=index.js.map