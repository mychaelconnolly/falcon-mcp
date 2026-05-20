# Falcon MCP Workflow and Dashboards Fork

This repository is a fork of CrowdStrike's `falcon-mcp` project prepared for
publication at `https://github.com/mychaelconnolly/falcon-mcp`.

## Purpose

The fork adds two capabilities:

- a read-only Workflow module for Fusion SOAR workflow design assistance
- an NGSIEM Dashboards module for reading dashboards and creating dashboards
  from reviewed LogScale YAML templates

The Workflow module lets an AI assistant query live Falcon Workflow catalog
data, existing workflow definitions, executions, execution results, and human
input records so it can recommend triggers, actions, conditions, fields, and
values for a stated SOAR automation goal.

The Workflow module is advisory only. It does not create, import, update,
execute, enable, disable, cancel, delete, or otherwise mutate workflows.

This fork is designed for teams that want AI-assisted Fusion SOAR workflow
planning without giving the MCP server authority to mutate workflows. Its
defining characteristic is least-privilege design assistance: it helps users
produce better workflow plans, but leaves workflow creation and change control to
humans and existing Falcon processes.

## Upstream Compatibility

All other functionality is intended to remain the same as upstream
`CrowdStrike/falcon-mcp`. The package name, CLI command, Python import path,
transports, configuration environment variables, and existing modules remain
`falcon-mcp` compatible.

Use the upstream project for official CrowdStrike Falcon MCP releases and
published PyPI / container artifacts:

https://github.com/CrowdStrike/falcon-mcp

Use this fork when you need the additional read-only Fusion SOAR Workflow design
module or NGSIEM dashboard read/create tooling.

Unlike broader Workflow lifecycle forks that expose write and execution
operations, this fork is intentionally scoped to read-only Workflow design
support.

## Installation From Fork

Until this fork has its own PyPI or container release, install it directly from
GitHub:

```bash
uv tool install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

Or run it without a permanent install:

```bash
uvx --from git+https://github.com/mychaelconnolly/falcon-mcp.git falcon-mcp
```

Pip users can install from GitHub:

```bash
pip install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

## Workflow Scope

To use the fork's Workflow module, grant the API client this CrowdStrike Falcon
scope:

```text
workflow:read
```

For focused use, load only the Workflow module:

```bash
falcon-mcp --modules workflow
```

For mixed use, include it in the normal module list:

```bash
falcon-mcp --modules workflow,detections,hosts,intel
```

## Dashboards Scope

To use the fork's Dashboards module, grant the API client these CrowdStrike
Falcon scopes:

```text
ngsiem-dashboards:read
ngsiem-dashboards:write
```

For focused use, load only the Dashboards module:

```bash
falcon-mcp --modules dashboards
```

## Publication Status

This fork is published at:

https://github.com/mychaelconnolly/falcon-mcp

The `main` branch is synced with upstream `v0.10.0` while preserving the
read-only Workflow module and adding NGSIEM dashboard read/create support.

The GitHub Pages documentation site is enabled at:

https://mychaelconnolly.github.io/falcon-mcp/

No PyPI release or container publication exists for this fork. The published
`falcon-mcp` PyPI package and public `quay.io/crowdstrike/falcon-mcp` image are
still upstream CrowdStrike artifacts.
