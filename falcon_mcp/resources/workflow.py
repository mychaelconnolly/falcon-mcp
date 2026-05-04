"""Fusion SOAR Workflow design guidance resources."""

WORKFLOW_BUILDER_GUIDE = """# Fusion SOAR Workflow Builder Guide

This module is advisory. Use it to recommend workflow designs from live Falcon
Workflow catalog data. Do not claim that a workflow has been created, imported,
updated, executed, enabled, disabled, or deleted.

## Recommended design process

1. Restate the user's SOAR goal, including the triggering event, target entities,
   desired outcome, and any stated safety limits.
2. Use `falcon_search_workflow_triggers` to find candidate trigger identifiers.
3. Use `falcon_search_workflow_activities` and
   `falcon_search_workflow_activity_content` to discover supported actions,
   fields, parameter names, operators, and allowed values.
4. Use `falcon_search_workflow_definitions` and, when useful,
   `falcon_export_workflow_definition` to inspect existing workflows as examples.
5. Recommend a draft workflow design with:
   - trigger and trigger field mappings
   - conditions and operators
   - actions in execution order
   - field/value mappings for each action
   - assumptions and values that need tenant-specific confirmation
   - validation notes and expected test cases
6. Keep recommendations implementation-ready, but stop before any write action.

## Output checklist

- Goal summary
- Recommended trigger
- Recommended conditions
- Recommended actions
- Required field/value mappings
- Existing workflow examples used
- Assumptions and unresolved tenant-specific values
- Validation and mock-test suggestions
"""

WORKFLOW_FQL_DOCUMENTATION = """# Fusion SOAR Workflow FQL Guide

Workflow catalog tools accept Falcon Query Language (FQL) filters where the
underlying Workflow endpoint supports them.

## Common patterns

- Exact match: `name:'Detection'`
- Namespace prefix: `name:'FalconAudit/Detection'`
- Boolean/status match: `enabled:true`
- Timestamp comparison: `created_on:>'2026-01-01T00:00:00Z'`
- Combine with AND: `enabled:true+name:'Detection'`
- Multiple values when supported: `id:['id1','id2']`

## Workflow design tips

- Search triggers first for the event source.
- Search activity content for field names, parameter schemas, and allowed values.
- Search definitions to find similar existing workflows before recommending a new design.
- Export definitions with `sanitize=true` when using them as examples.
"""
