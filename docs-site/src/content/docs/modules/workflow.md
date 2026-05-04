---
title: Workflow
description: Fusion SOAR workflow design assistance using live Workflow catalog data.
sidebar:
  order: 10
---

Fusion SOAR workflow design assistance using live Workflow catalog data.

## API Scopes

- `workflow:read`

## Tools

### `falcon_export_workflow_definition`

**Required scopes:** `workflow:read`

Export a workflow definition as YAML for advisory design reference.

This is read-only and should be used to inspect existing workflow
structure, field mappings, and action sequences. It does not import or
modify any workflow.

**Example prompts:**

- "Export workflow definition abc123 as a sanitized reference"

### `falcon_get_workflow_execution_results`

**Required scopes:** `workflow:read`

Get execution results for one or more workflow executions.

**Example prompts:**

- "Get results for workflow execution abc123"

### `falcon_get_workflow_human_inputs`

**Required scopes:** `workflow:read`

Get one or more workflow human input records.

This is read-only. It does not approve, decline, escalate, or otherwise
answer a human input request.

**Example prompts:**

- "Show human input details for request abc123"

### `falcon_query_workflow_child_executions`

**Required scopes:** `workflow:read`

Search child workflow executions by FQL filter and paging details.

**Example prompts:**

- "Find child executions for parent workflow execution abc123"

### `falcon_search_workflow_activities`

**Required scopes:** `workflow:read`

Search supported Fusion SOAR workflow activities.

Use this when designing a workflow to find candidate action nodes.
For action fields and allowed values, call
`falcon_search_workflow_activity_content`.

**Example prompts:**

- "Find workflow actions for notifying an analyst"

### `falcon_search_workflow_activity_content`

**Required scopes:** `workflow:read`

Search activity content for Fusion SOAR workflow design.

Use this to discover action configuration fields, parameter schemas,
operators, and allowed values before recommending a workflow step.

**Example prompts:**

- "Show me the fields required for a host containment workflow action"

### `falcon_search_workflow_definitions`

**Required scopes:** `workflow:read`

Search existing Fusion SOAR workflow definitions.

Use matching definitions as tenant-specific examples before recommending
a new workflow design.

**Example prompts:**

- "Find existing workflows related to host containment"

### `falcon_search_workflow_executions`

**Required scopes:** `workflow:read`

Search Fusion SOAR workflow executions.

Use this to understand recent workflow behavior and execution patterns
before recommending changes or a new workflow design.

**Example prompts:**

- "Show recent executions for workflow abc123"

### `falcon_search_workflow_triggers`

**Required scopes:** `workflow:read`

Search Fusion SOAR workflow triggers.

Start workflow design here to identify the event source and trigger field
mappings that fit the user's SOAR goal.

**Example prompts:**

- "Find the workflow trigger for new detections"

## Resources

- **`falcon://workflow/builder-guide`**: Advisory guide for designing Fusion SOAR workflows from live catalog data.
- **`falcon://workflow/fql-guide`**: FQL guide for Falcon Workflow search tools.
