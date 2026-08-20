#!/bin/bash
# Penpot MCP Server - Start Script

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

SERVER_DIR="/root/.pi/penpot-mcp"
SERVER_BIN="$SERVER_DIR/node_modules/@penpot/mcp/packages/server/dist/index.js"
PID_FILE="$SERVER_DIR/mcp.pid"
LOG_DIR="$SERVER_DIR/logs"
PORT="${PENPOT_MCP_PORT:-4401}"
WS_PORT="${PENPOT_MCP_WEBSOCKET_PORT:-4405}"

mkdir -p "$LOG_DIR"

# Already running?
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    exit 0
fi

# Port in use by something else?
fuser -k "$PORT/tcp" "$WS_PORT/tcp" 2>/dev/null
sleep 1

[ ! -f "$SERVER_BIN" ] && echo -e "${RED}❌ Server not built${NC}" && exit 1

cd "$SERVER_DIR"
PENPOT_MCP_WEBSOCKET_PORT="$WS_PORT" \
nohup node "$SERVER_BIN" > "$LOG_DIR/mcp-server.log" 2>&1 &
echo $! > "$PID_FILE"
disown

sleep 2
kill -0 "$(cat $PID_FILE)" 2>/dev/null && echo -e "${GREEN}✅ Penpot MCP: http://localhost:$PORT/mcp${NC}" || {
    echo -e "${RED}❌ Failed${NC}"
    tail -5 "$LOG_DIR/mcp-server.log"
}
