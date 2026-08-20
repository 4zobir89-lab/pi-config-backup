#!/bin/bash
# Penpot MCP Server - Stop Script

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PID_FILE="/root/.pi/penpot-mcp/mcp.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo -e "${YELLOW}Stopping Penpot MCP Server (PID: $PID)...${NC}"
        kill "$PID"
        sleep 2
        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID"
        fi
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Penpot MCP Server stopped${NC}"
    else
        rm -f "$PID_FILE"
        echo -e "${YELLOW}⚠️  Server was not running (stale PID file removed)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No PID file found. Server may not be running.${NC}"
fi
