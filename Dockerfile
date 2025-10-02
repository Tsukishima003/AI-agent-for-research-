FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev) for the build step
RUN npm install

# Copy source files
COPY . .

# Build TypeScript
RUN npm run build

# Remove dev dependencies after build
RUN npm prune --production

# Expose WebSocket port
EXPOSE 7800

# Start server in WebSocket mode
CMD ["npm", "start"]