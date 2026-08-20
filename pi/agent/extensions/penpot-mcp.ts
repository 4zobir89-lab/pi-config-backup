import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { execSync, spawn, exec } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MCP_DIR = "/root/.pi/penpot-mcp";
const PID_FILE = join(MCP_DIR, "mcp.pid");
const LOG_DIR = join(MCP_DIR, "logs");
const PORT = 4401;
const WS_PORT = 4405;

function isRunning(): boolean {
  try {
    if (!existsSync(PID_FILE)) return false;
    const pid = readFileSync(PID_FILE, "utf-8").trim();
    execSync(`kill -0 ${pid} 2>/dev/null`);
    return true;
  } catch {
    return false;
  }
}

function startServer(): Promise<boolean> {
  return new Promise((resolve) => {
    if (isRunning()) {
      resolve(true);
      return;
    }

    const serverBin = join(MCP_DIR, "node_modules/@penpot/mcp/packages/server/dist/index.js");
    if (!existsSync(serverBin)) {
      resolve(false);
      return;
    }

    // Kill any existing process on the port
    try {
      execSync(`fuser -k ${PORT}/tcp ${WS_PORT}/tcp 2>/dev/null`);
    } catch {}

    setTimeout(() => {
      const child = spawn("node", [serverBin], {
        cwd: MCP_DIR,
        detached: true,
        stdio: ["ignore", "pipe", "pipe"],
        env: {
          ...process.env,
          PENPOT_MCP_WEBSOCKET_PORT: String(WS_PORT),
        },
      });

      child.unref();

      // Wait for server to start
      setTimeout(() => {
        try {
          if (child.pid) {
            writeFileSync(PID_FILE, String(child.pid));
            resolve(true);
          } else {
            resolve(false);
          }
        } catch {
          resolve(false);
        }
      }, 2000);
    }, 1000);
  });
}

function stopServer(): void {
  try {
    if (existsSync(PID_FILE)) {
      const pid = readFileSync(PID_FILE, "utf-8").trim();
      execSync(`kill ${pid} 2>/dev/null`);
      execSync(`rm -f ${PID_FILE}`);
    }
    execSync(`fuser -k ${PORT}/tcp ${WS_PORT}/tcp 2>/dev/null`);
  } catch {}
}

export default function (pi: ExtensionAPI) {
  let serverStarted = false;

  // Auto-start on session start
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.setStatus("penpot", "🔄 Starting Penpot MCP...");

    const started = await startServer();
    serverStarted = started;

    if (started) {
      ctx.ui.setStatus("penpot", `🟢 Penpot MCP: http://localhost:${PORT}/mcp`);
    } else {
      ctx.ui.setStatus("penpot", "🔴 Penpot MCP: Failed to start");
    }
  });

  // Cleanup on shutdown
  pi.on("session_shutdown", async () => {
    // Don't stop the server on shutdown - keep it running for next session
    // stopServer();
  });

  // Register /penpot command
  pi.registerCommand("penpot", {
    description: "Penpot MCP server control (start/status/stop)",
    handler: async (args, ctx) => {
      const action = args?.trim().toLowerCase() || "status";

      switch (action) {
        case "start": {
          ctx.ui.notify("Starting Penpot MCP...", "info");
          const started = await startServer();
          serverStarted = started;
          if (started) {
            ctx.ui.setStatus("penpot", `🟢 Penpot MCP: http://localhost:${PORT}/mcp`);
            ctx.ui.notify(`Penpot MCP started!\nEndpoint: http://localhost:${PORT}/mcp\nPlugin: http://localhost:4400`, "success");
          } else {
            ctx.ui.notify("Failed to start Penpot MCP server", "error");
          }
          break;
        }
        case "stop": {
          stopServer();
          serverStarted = false;
          ctx.ui.setStatus("penpot", "🔴 Penpot MCP: Stopped");
          ctx.ui.notify("Penpot MCP stopped", "info");
          break;
        }
        case "status":
        default: {
          const running = isRunning();
          const status = running ? "🟢 Running" : "🔴 Stopped";
          ctx.ui.notify(
            `Penpot MCP Status: ${status}\n` +
            `Endpoint: http://localhost:${PORT}/mcp\n` +
            `Plugin: http://localhost:4400\n` +
            `PID File: ${PID_FILE}`,
            "info"
          );
          break;
        }
      }
    },
  });

  // Register /penpot-connect command for easy setup instructions
  pi.registerCommand("penpot-connect", {
    description: "Show Penpot connection instructions",
    handler: async (_args, ctx) => {
      ctx.ui.notify(
        "🎨 Penpot MCP Connection Guide\n\n" +
        "1. Open Penpot in browser:\n" +
        "   - https://design.penpot.app (SaaS)\n" +
        "   - or your self-hosted instance\n\n" +
        "2. Open a design file\n\n" +
        "3. Go to Plugins menu\n\n" +
        "4. Load plugin:\n" +
        "   http://localhost:4400/manifest.json\n\n" +
        "5. Click 'Connect to MCP server'\n\n" +
        "6. Status should change to 'Connected'\n\n" +
        "⚠️ Keep plugin UI open during use!",
        "info"
      );
    },
  });
}
