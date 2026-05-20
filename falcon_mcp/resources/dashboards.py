"""Resources for the Dashboards module."""

SEARCH_DASHBOARDS_FQL_DOCUMENTATION = """
# NGSIEM Dashboard Search Filter

`falcon_list_dashboards` supports text matching on dashboard names:

```text
name:~'value'
```

Examples:

```text
name:~'Windows'
name:~'Endpoint'
```
""".strip()
