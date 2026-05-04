![CrowdStrike Logo (Light)](https://raw.githubusercontent.com/CrowdStrike/.github/main/assets/cs-logo-light-mode.png#gh-light-mode-only)
![CrowdStrike Logo (Dark)](https://raw.githubusercontent.com/CrowdStrike/.github/main/assets/cs-logo-dark-mode.png#gh-dark-mode-only)

# falcon-mcp

[![PyPI version](https://badge.fury.io/py/falcon-mcp.svg)](https://badge.fury.io/py/falcon-mcp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/falcon-mcp)](https://pypi.org/project/falcon-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://mychaelconnolly.github.io/falcon-mcp/)

**falcon-mcp** is a Model Context Protocol (MCP) server that connects AI agents with the CrowdStrike Falcon platform, powering intelligent security analysis in your agentic workflows. It delivers programmatic access to essential security capabilities—including detections, incidents, and behaviors—establishing the foundation for advanced security operations and automation.

> [!NOTE]
> This is a fork of [`CrowdStrike/falcon-mcp`](https://github.com/CrowdStrike/falcon-mcp). It keeps the same `falcon-mcp` package, CLI, transports, configuration, and existing module behavior as upstream, with one addition: a read-only Workflow module for advisory Fusion SOAR workflow design. The Workflow module helps recommend triggers, actions, conditions, fields, and values from live Falcon Workflow catalog data. It does not create, import, update, execute, enable, disable, cancel, or delete workflows.
>
> This fork is designed for teams that want AI-assisted Fusion SOAR workflow planning without giving the MCP server authority to mutate workflows. Unlike broader Workflow lifecycle forks that expose write and execution operations, this fork is intentionally scoped to least-privilege, read-only design support.

> [!IMPORTANT]
> **🚧 Public Preview**: This project is currently in public preview and under active development. Features and functionality may change before the stable 1.0 release. While we encourage exploration and testing, please avoid production deployments. We welcome your feedback through [GitHub Issues](https://github.com/mychaelconnolly/falcon-mcp/issues) to help shape the final release.

## Documentation

Full fork docs are available at **[mychaelconnolly.github.io/falcon-mcp](https://mychaelconnolly.github.io/falcon-mcp/)**.

See [FORK.md](FORK.md) for the fork purpose, upstream compatibility statement, and fork-specific install notes.

## Modules

| Module | Description |
|--------|-------------|
| Core | Basic connectivity and system information |
| [Cloud Security](https://mychaelconnolly.github.io/falcon-mcp/modules/cloud/) | Kubernetes containers, image vulnerabilities, and CSPM asset inventory |
| [Custom IOA](https://mychaelconnolly.github.io/falcon-mcp/modules/custom-ioa/) | Create and manage Custom IOA behavioral detection rules and rule groups |
| [Detections](https://mychaelconnolly.github.io/falcon-mcp/modules/detections/) | Find and analyze detections to understand malicious activity |
| [Discover](https://mychaelconnolly.github.io/falcon-mcp/modules/discover/) | Search application inventory and discover unmanaged assets |
| [Firewall Management](https://mychaelconnolly.github.io/falcon-mcp/modules/firewall/) | Search and manage firewall rules and rule groups |
| [Hosts](https://mychaelconnolly.github.io/falcon-mcp/modules/hosts/) | Manage and query host/device information |
| [Identity Protection](https://mychaelconnolly.github.io/falcon-mcp/modules/idp/) | Entity investigation and identity protection analysis |
| [Incidents](https://mychaelconnolly.github.io/falcon-mcp/modules/incidents/) | Analyze security incidents and coordinated activities |
| [Intel](https://mychaelconnolly.github.io/falcon-mcp/modules/intel/) | Research threat actors, IOCs, and intelligence reports |
| [IOC](https://mychaelconnolly.github.io/falcon-mcp/modules/ioc/) | Search, create, and remove custom indicators of compromise |
| [NGSIEM](https://mychaelconnolly.github.io/falcon-mcp/modules/ngsiem/) | Execute CQL queries against Next-Gen SIEM |
| [Real Time Response](https://mychaelconnolly.github.io/falcon-mcp/modules/rtr/) | Initialize RTR sessions and execute read-only triage commands |
| [Scheduled Reports](https://mychaelconnolly.github.io/falcon-mcp/modules/scheduled-reports/) | Manage scheduled reports and download report files |
| [Sensor Usage](https://mychaelconnolly.github.io/falcon-mcp/modules/sensor-usage/) | Access and analyze sensor usage data |
| [Serverless](https://mychaelconnolly.github.io/falcon-mcp/modules/serverless/) | Search for vulnerabilities in serverless functions |
| [Shield](https://mychaelconnolly.github.io/falcon-mcp/modules/shield/) | SaaS security posture, checks, alerts, and app inventory |
| [Spotlight](https://mychaelconnolly.github.io/falcon-mcp/modules/spotlight/) | Manage and analyze vulnerability data and security assessments |
| [Workflow](https://mychaelconnolly.github.io/falcon-mcp/modules/workflow/) | Advisory Fusion SOAR workflow design using live Workflow catalog data |

See the [Module Overview](https://mychaelconnolly.github.io/falcon-mcp/modules/overview/) for required API scopes, available tools, and FQL resources.

## Quick Start

### Install

#### Using uv (recommended)

```bash
uv tool install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

#### Using pip

```bash
pip install git+https://github.com/mychaelconnolly/falcon-mcp.git
```

> [!NOTE]
> `uv tool install falcon-mcp`, `pip install falcon-mcp`, and the public `quay.io/crowdstrike/falcon-mcp` container install upstream artifacts. Use the GitHub install commands above for this fork until fork-specific package or container artifacts exist.

### Configure

Set the required environment variables (or use a `.env` file — see the [Configuration Guide](https://mychaelconnolly.github.io/falcon-mcp/getting-started/configuration/)):

```bash
export FALCON_CLIENT_ID="your-client-id"
export FALCON_CLIENT_SECRET="your-client-secret"
export FALCON_BASE_URL="https://api.crowdstrike.com"
```

### Run

```bash
falcon-mcp
```

See the [Getting Started guide](https://mychaelconnolly.github.io/falcon-mcp/getting-started/installation/) for full installation and configuration details.

## Editor Integration

### Using `uvx` (recommended)

```json
{
  "mcpServers": {
    "falcon-mcp": {
      "command": "uvx",
      "args": [
        "--env-file",
        "/path/to/.env",
        "--from",
        "git+https://github.com/mychaelconnolly/falcon-mcp.git",
        "falcon-mcp"
      ]
    }
  }
}
```

### With Module Selection

```json
{
  "mcpServers": {
    "falcon-mcp": {
      "command": "uvx",
      "args": [
        "--env-file",
        "/path/to/.env",
        "--from",
        "git+https://github.com/mychaelconnolly/falcon-mcp.git",
        "falcon-mcp",
        "--modules",
        "workflow,detections,incidents,intel"
      ]
    }
  }
}
```

### Docker

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
        "falcon-mcp-workflow"
      ]
    }
  }
}
```

Build `falcon-mcp-workflow` locally from this fork before using the Docker configuration. The upstream `quay.io/crowdstrike/falcon-mcp` image does not include fork-only Workflow tools.

See the [Usage guide](https://mychaelconnolly.github.io/falcon-mcp/usage/cli/) for all command line options, module configuration, and library usage.

## Container Usage

No fork-specific container image is published yet. Build locally to include the Workflow module:

```bash
# Build this fork locally
docker build -t falcon-mcp-workflow .

# Run with .env file (stdio transport)
docker run -i --rm --env-file /path/to/.env falcon-mcp-workflow

# Run with streamable-http transport
docker run --rm -p 8000:8000 --env-file /path/to/.env \
  falcon-mcp-workflow --transport streamable-http --host 0.0.0.0
```

See the [Docker Deployment guide](https://mychaelconnolly.github.io/falcon-mcp/deployment/docker/) for building locally, custom ports, and advanced configurations.

## Deployment Options

- [Amazon Bedrock AgentCore](https://mychaelconnolly.github.io/falcon-mcp/deployment/amazon-bedrock/)
- [Google Cloud (Cloud Run / Vertex AI)](./examples/adk/README.md)

## Contributing

```bash
# Clone and install
git clone https://github.com/mychaelconnolly/falcon-mcp.git
cd falcon-mcp
uv sync --all-extras

# Run tests
uv run pytest
```

> [!IMPORTANT]
> This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated releases. Please follow the commit message format outlined in our [Contributing Guide](docs/CONTRIBUTING.md).

### Developer Documentation

- [Docs Site Guide](docs/development/docs_site.md): Architecture and development guide for the documentation site
- [Module Development Guide](docs/development/module_development.md): Instructions for implementing new modules
- [Resource Development Guide](docs/development/resource_development.md): Instructions for implementing resources
- [End-to-End Testing Guide](docs/development/e2e_testing.md): Guide for running and understanding E2E tests
- [Integration Testing Guide](docs/development/integration_testing.md): Guide for running integration tests with real API calls

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

This fork is community-maintained and is not an official CrowdStrike product. The upstream `falcon-mcp` project is maintained by CrowdStrike and supported in collaboration with the open source developer community.

For more information, please see our [SUPPORT](SUPPORT.md) file.
