import { spawn } from 'child_process';

const server = spawn('node', ['dist/index.js', '--stdio'], {
  cwd: 'C:\\Users\\DELL\\Documents\\HTON\\mcp-research-agent'
});

let output = '';
let errorOutput = '';

server.stdout.on('data', (data) => {
  output += data.toString();
  console.log('STDOUT:', data.toString());
});

server.stderr.on('data', (data) => {
  errorOutput += data.toString();
  console.log('STDERR:', data.toString());
});

server.on('close', (code) => {
  console.log('Server exited with code:', code);
  console.log('Full output:', output);
  console.log('Full errors:', errorOutput);
});

// Send initialize message
const initMessage = JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "test", version: "1.0.0" }
  }
}) + '\n';

setTimeout(() => {
  console.log('Sending initialize message...');
  server.stdin.write(initMessage);
}, 1000);

setTimeout(() => {
  server.kill();
}, 5000);