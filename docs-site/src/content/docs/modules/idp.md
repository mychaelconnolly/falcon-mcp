---
title: Identity Protection
description: Accessing and managing CrowdStrike Falcon Identity Protection capabilities
sidebar:
  order: 10
---

Accessing and managing CrowdStrike Falcon Identity Protection capabilities

## API Scopes

- `Identity Protection Assessment:read`
- `Identity Protection Detections:read`
- `Identity Protection Entities:read`
- `Identity Protection Timeline:read`
- `Identity Protection GraphQL:write`

## Tools

### `falcon_investigate_entity`

**Required scopes:** `Identity Protection Assessment:read`, `Identity Protection Detections:read`, `Identity Protection Entities:read`, `Identity Protection Timeline:read`, `Identity Protection GraphQL:write`

Investigate Identity Protection entities by ID, name, email, IP, or domain.
