# Falcon MCP Workflow Fork

This repository is a fork of CrowdStrike's `falcon-mcp` project prepared for
publication at `https://github.com/mychaelconnolly/falcon-mcp`.

## Purpose

The fork adds one capability: a read-only Workflow module for Fusion SOAR
workflow design assistance. The module lets an AI assistant query live Falcon
Workflow catalog data, existing workflow definitions, executions, execution
results, and human input records so it can recommend triggers, actions,
conditions, fields, and values for a stated SOAR automation goal.

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
module.

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
falcon-mcp --modules workflow,detections,incidents,intel
```

## Publication Status

This branch is prepared for a fork, but no push, release, PyPI publication, or
container publication is implied by these docs.
