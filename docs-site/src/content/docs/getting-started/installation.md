---
title: Installation
description: Install the Falcon MCP Server using uv or pip.
---

## Prerequisites

- Python 3.11 or higher
- [`uv`](https://docs.astral.sh/uv/) or pip
- CrowdStrike Falcon API credentials ([see API Credentials](/falcon-mcp/getting-started/credentials))

## Install using uv

Install this fork from GitHub:

```bash
uv tool install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

## Install using pip

Install this fork from GitHub:

```bash
pip install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

:::tip
If `falcon-mcp` isn't found after installation, update your shell `PATH`.
:::

:::note
`uv tool install falcon-mcp`, `pip install falcon-mcp`, and the public
`quay.io/crowdstrike/falcon-mcp` container install upstream artifacts. Use the
GitHub install commands on this page for the fork-only Workflow module until
fork-specific package or container artifacts exist.
:::

## Run without installing

You can run the server directly without a permanent install using `uvx`:

```bash
uvx --from git+https://github.com/mychaelconnolly/falcon-mcp.git falcon-mcp
```

This is the recommended approach for editor integrations.

:::note
If you just want to interact with falcon-mcp via an agent chat interface rather than running the server yourself, see the [Deployment](/falcon-mcp/deployment/docker/) options.
:::
