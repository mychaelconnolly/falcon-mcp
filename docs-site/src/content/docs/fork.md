---
title: Fork Notes
description: Purpose and compatibility notes for the mychaelconnolly Falcon MCP fork.
sidebar:
  order: 1
---

This documentation describes `mychaelconnolly/falcon-mcp`, a fork of
CrowdStrike's upstream [`falcon-mcp`](https://github.com/CrowdStrike/falcon-mcp)
project.

## Purpose

This fork keeps the same `falcon-mcp` package, CLI, transports, configuration,
and existing module behavior as upstream. It adds two modules:

- `workflow`: read-only Fusion SOAR Workflow design assistance using live Falcon
  Workflow catalog data.
- `dashboards`: NGSIEM dashboard read/create support using LogScale dashboard
  YAML templates.

The Workflow module helps AI assistants recommend triggers, actions, conditions,
fields, and values for a stated SOAR automation goal. It is advisory only. It
does not create, import, update, execute, enable, disable, cancel, or delete
workflows.

This fork is designed for teams that want AI-assisted Fusion SOAR workflow
planning without giving the MCP server authority to mutate workflows, plus
AI-assisted NGSIEM dashboard discovery and creation from reviewed LogScale YAML
templates. Its Workflow support helps users produce better workflow plans, but
leaves workflow creation and change control to humans and existing Falcon
processes.

## Compatibility

All other functionality is intended to remain the same as upstream
`CrowdStrike/falcon-mcp`.

The fork does not rename:

- package name: `falcon-mcp`
- CLI command: `falcon-mcp`
- Python package: `falcon_mcp`
- environment variables: `FALCON_*`
- supported transports: `stdio`, `sse`, `streamable-http`

Use upstream `falcon-mcp` for official CrowdStrike releases and published PyPI
or container artifacts. Use this fork when you need the added read-only Workflow
advisory module or NGSIEM dashboard read/create tooling.

Unlike broader Workflow lifecycle forks that expose write and execution
operations, this fork is intentionally scoped to read-only Workflow design
support.

## Install From This Fork

Until fork-specific PyPI or container artifacts exist, install directly from the
fork repository:

```bash
uv tool install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

Run without permanent installation:

```bash
uvx --from git+https://github.com/mychaelconnolly/falcon-mcp.git falcon-mcp
```

Install with pip:

```bash
pip install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

## Workflow API Scope

The Workflow module requires:

```text
workflow:read
```

To load only the Workflow module:

```bash
falcon-mcp --modules workflow
```

To combine it with other modules:

```bash
falcon-mcp --modules workflow,detections,hosts,intel
```

## Dashboards API Scope

The Dashboards module requires:

```text
ngsiem-dashboards:read
ngsiem-dashboards:write
```

To load only the Dashboards module:

```bash
falcon-mcp --modules dashboards
```
