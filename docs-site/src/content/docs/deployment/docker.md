---
title: Docker
description: Deploy the Falcon MCP Server using Docker containers.
---

The upstream Falcon MCP Server is available as a pre-built container image at
`quay.io/crowdstrike/falcon-mcp`. That image does not include this fork's
Workflow and Dashboards modules unless a fork-specific image is published later.

## Building This Fork Locally (Recommended)

Build the image from this fork checkout:

```bash
docker build -t falcon-mcp-fork .
```

Run with stdio transport (requires -i flag):

```bash
docker run -i --rm --env-file /path/to/.env falcon-mcp-fork
```

Run with SSE transport:

```bash
docker run --rm -p 8000:8000 --env-file /path/to/.env \
  falcon-mcp-fork --transport sse --host 0.0.0.0
```

Run with streamable-http transport:

```bash
docker run --rm -p 8000:8000 --env-file /path/to/.env \
  falcon-mcp-fork --transport streamable-http --host 0.0.0.0
```

Run with custom port:

```bash
docker run --rm -p 8080:8080 --env-file /path/to/.env \
  falcon-mcp-fork --transport streamable-http --host 0.0.0.0 --port 8080
```

Run with specific modules (stdio transport):

```bash
docker run -i --rm --env-file /path/to/.env \
  falcon-mcp-fork --modules workflow,dashboards,detections,hosts,spotlight,idp
```

## Upstream Pre-built Image

Use `quay.io/crowdstrike/falcon-mcp` only when you want the upstream
CrowdStrike image. It keeps upstream behavior and does not include fork-only
modules unless this fork has been merged upstream or a
fork-specific image has been published.

## Using Individual Environment Variables

Instead of a `.env` file, pass variables directly:

```bash
docker run -i --rm \
  -e FALCON_CLIENT_ID=your_client_id \
  -e FALCON_CLIENT_SECRET=your_secret \
  -e FALCON_BASE_URL=https://api.crowdstrike.com \
  falcon-mcp-fork
```

:::note
When using HTTP transports in Docker, always set `--host 0.0.0.0` to allow external connections to the container.

The `-i` flag is required when using the default stdio transport.
:::

## MCP Client Configuration

To use the Docker image with Claude Desktop or similar clients, add to your MCP config:

```json
{
  "mcpServers": {
    "falcon-mcp-docker": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/full/path/to/.env",
        "falcon-mcp-fork"
      ]
    }
  }
}
```
