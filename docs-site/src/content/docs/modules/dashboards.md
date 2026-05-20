---
title: Dashboards
description: Reading and creating NGSIEM dashboards from LogScale dashboard YAML templates
sidebar:
  order: 10
---

Reading and creating NGSIEM dashboards from LogScale dashboard YAML templates

## API Scopes

- `ngsiem-dashboards:read`
- `ngsiem-dashboards:write`

## Tools

### `falcon_create_dashboard_from_template`

:::note
This tool modifies data.
:::

**Required scopes:** `ngsiem-dashboards:write`

Create NGSIEM dashboard from YAML.

**Example prompts:**

- "Create an NGSIEM dashboard named Endpoint Overview from this YAML template"

### `falcon_get_dashboard_template`

**Required scopes:** `ngsiem-dashboards:read`

Export NGSIEM dashboard YAML.

**Example prompts:**

- "Export dashboard abc123 as a LogScale YAML template"

### `falcon_list_dashboards`

**Required scopes:** `ngsiem-dashboards:read`

List NGSIEM dashboards.

**Example prompts:**

- "List NGSIEM dashboards matching Windows"
- "Show me dashboards in the Falcon search domain"

## Resources

- **`falcon://dashboards/search/fql-guide`**: FQL guide for `falcon_list_dashboards` filter syntax.
