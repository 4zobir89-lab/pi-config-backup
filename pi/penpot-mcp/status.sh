#!/bin/bash
# Penpot MCP Server - Status Script

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PID_FILE="/root/.pi/penpot-mcp/mcp.pid"
LOG_DIR="/root/.pi/penpot-mcp/logs"

echo -e "${GREEN}=== Penpot MCP Server Status ===${NC}"
echo ""

# Check if running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo -e "${GREEN}✅ Status: RUNNING${NC} (PID: $PID)"
        echo ""
        echo -e "${GREEN}📡 MCP Endpoint:${NC} http://localhost:4401/mcp"
        echo -e "${GREEN}🔌 Plugin Server:${NC} http://localhost:4400"
        echo ""
        echo -e "${YELLOW}📌 Connect Claude Code:${NC}"
        echo "   claude mcp add penpot -t http http://localhost:4401/mcp"
        echo ""
        echo -e "${YELLOW}📌 Connect Penpot Plugin:${NC}"
        echo "   1. Open Penpot → Design file → Plugins"
        echo "   2. Load: http://localhost:4400/manifest.json"
        echo "   3. Click 'Connect to MCP server'"
    else
        echo -e "${RED}❌ Status: STOPPED${NC} (stale PID file)"
        rm -f "$PID_FILE"
    fi
else
    echo -e "${RED}❌ Status: NOT RUNNING${NC}"
    echo ""
    echo -e "${YELLOW}📌 To start:${NC}"
    echo "   /root/.pi/penpot-mcp/start.sh"
fi

echo ""
echo -e "${YELLOW}📋 Logs:${NC} $LOG_DIR/mcp-server.log"
