# Forguncy Plugin MCP Server

This MCP server provides access to the Forguncy Plugin Master Skill documentation and templates.

## Capabilities

- List and read documentation.
- List and read code templates.
- Access the main SKILL.md guide.

## Usage

Run the server:

```bash
python server.py
```

## Configuration

### Option 1: Local Stdio Mode (Recommended for Local Use)

Use this configuration for local MCP clients like Claude Desktop. It runs the script directly via standard input/output.

Add to your config file (e.g., `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "forguncy-helper": {
      "command": "python",
      "args": [
        "D:\\Code\\Funguncy-Plugin-Builder\\forguncy-plugin-mcp\\server.py"
      ]
    }
  }
}
```

> **Note**: Ensure `python` is in your system PATH, or use the full path to your python executable.

### Option 2: SSE Mode (For Remote/Web Access)

Use this configuration if your client connects via HTTP (Server-Sent Events).

1. **Start the Server**:
   ```bash
   python server.py --transport sse --port 8000 --host 0.0.0.0
   ```

2. **Configure Client**:
   ```json
   {
     "mcpServers": {
       "forguncy-helper-sse": {
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```
