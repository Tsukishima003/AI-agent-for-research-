import { createServer } from 'http';

export function startHealthServer(port: number) {
  const server = createServer((req, res) => {
    if (req.url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
    } else {
      res.writeHead(404);
      res.end('Not Found');
    }
  });

  server.listen(port + 1, () => {
    console.log(`Health check server listening on port ${port + 1}`);
  });

  return server;
}
