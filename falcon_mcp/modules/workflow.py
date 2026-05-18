"""
Workflow module for Falcon MCP Server.

This module provides read-only tools for Fusion SOAR workflow design assistance
using live Workflow catalog, definition, execution, and human input data.
"""

from typing import Any

from mcp.server import FastMCP
from mcp.server.fastmcp.resources import TextResource
from pydantic import AnyUrl, Field

from falcon_mcp.common.errors import _format_error_response, handle_api_response
from falcon_mcp.common.utils import prepare_api_parameters
from falcon_mcp.modules.base import BaseModule
from falcon_mcp.resources.workflow import (
    WORKFLOW_BUILDER_GUIDE,
    WORKFLOW_FQL_DOCUMENTATION,
)


class WorkflowModule(BaseModule):
    """Module for Fusion SOAR workflow design assistance."""

    def register_tools(self, server: FastMCP) -> None:
        """Register read-only Workflow tools with the MCP server."""
        self._add_tool(
            server=server,
            method=self.search_workflow_activities,
            name="search_workflow_activities",
        )
        self._add_tool(
            server=server,
            method=self.search_workflow_activity_content,
            name="search_workflow_activity_content",
        )
        self._add_tool(
            server=server,
            method=self.search_workflow_triggers,
            name="search_workflow_triggers",
        )
        self._add_tool(
            server=server,
            method=self.search_workflow_definitions,
            name="search_workflow_definitions",
        )
        self._add_tool(
            server=server,
            method=self.export_workflow_definition,
            name="export_workflow_definition",
        )
        self._add_tool(
            server=server,
            method=self.search_workflow_executions,
            name="search_workflow_executions",
        )
        self._add_tool(
            server=server,
            method=self.get_workflow_execution_results,
            name="get_workflow_execution_results",
        )
        self._add_tool(
            server=server,
            method=self.get_workflow_human_inputs,
            name="get_workflow_human_inputs",
        )
        self._add_tool(
            server=server,
            method=self.query_workflow_child_executions,
            name="query_workflow_child_executions",
        )

    def register_resources(self, server: FastMCP) -> None:
        """Register Workflow design resources with the MCP server."""
        builder_resource = TextResource(
            uri=AnyUrl("falcon://workflow/builder/design-guide"),
            name="falcon_workflow_builder_guide",
            description="Advisory guide for designing Fusion SOAR workflows from live catalog data.",
            text=WORKFLOW_BUILDER_GUIDE,
        )
        fql_resource = TextResource(
            uri=AnyUrl("falcon://workflow/catalog/fql-guide"),
            name="falcon_workflow_fql_guide",
            description="FQL guide for Falcon Workflow search tools.",
            text=WORKFLOW_FQL_DOCUMENTATION,
        )

        self._add_resource(server, builder_resource)
        self._add_resource(server, fql_resource)

    def _search_workflow_catalog(
        self,
        operation: str,
        search_params: dict[str, Any],
        error_message: str,
        filter_used: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        result = self._base_search_api_call(
            operation=operation,
            search_params=search_params,
            error_message=error_message,
            default_result=[],
        )
        if self._is_error(result):
            return self._format_fql_error_response(
                [result],
                filter_used,
                WORKFLOW_FQL_DOCUMENTATION,
            )
        return result

    def _get_workflow_by_ids(
        self,
        operation: str,
        ids: str | list[str],
        error_message: str,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        normalized_ids = [ids] if isinstance(ids, str) else ids
        response = self.client.command(
            operation,
            parameters=prepare_api_parameters({"ids": normalized_ids}),
        )
        return handle_api_response(
            response,
            operation=operation,
            error_message=error_message,
            default_result=[],
        )

    def _export_workflow_yaml(
        self,
        operation: str,
        id: str,
        sanitize: bool,
    ) -> str | list[dict[str, Any]] | dict[str, Any]:
        response = self.client.command(
            operation,
            parameters=prepare_api_parameters({"id": id, "sanitize": sanitize}),
        )

        if isinstance(response, bytes):
            return response.decode("utf-8")

        if isinstance(response, str):
            return response

        if isinstance(response, dict):
            status_code = response.get("status_code")
            if status_code is None or status_code >= 300:
                return handle_api_response(
                    response,
                    operation=operation,
                    error_message="Failed to export workflow definition",
                    default_result=[],
                )

            body = response.get("body")
            if isinstance(body, str):
                return body
            if isinstance(body, dict):
                resources = body.get("resources")
                if resources:
                    return resources
                return body

        return _format_error_response(
            f"Unexpected response type: {type(response).__name__}",
            operation=operation,
        )

    def search_workflow_activities(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for workflow activities. Use `falcon://workflow/catalog/fql-guide` for examples.",
        ),
        limit: int = Field(
            default=50,
            ge=1,
            description="Maximum number of workflow activities to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
        sort: str | None = Field(
            default=None,
            description="Sort expression such as `name.asc` or `name.desc`.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search supported Fusion SOAR workflow activities.

        Use this when designing a workflow to find candidate action nodes.
        For action fields and allowed values, call
        `falcon_search_workflow_activity_content`.
        """
        return self._search_workflow_catalog(
            operation="WorkflowActivitiesCombined",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
            },
            error_message="Failed to search workflow activities",
            filter_used=filter,
        )

    def search_workflow_activity_content(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for workflow activity content. Use `falcon://workflow/catalog/fql-guide` for examples.",
        ),
        limit: int = Field(
            default=50,
            ge=1,
            description="Maximum number of workflow activity content records to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
        sort: str | None = Field(
            default=None,
            description="Sort expression such as `name.asc` or `name.desc`.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search activity content for Fusion SOAR workflow design.

        Use this to discover action configuration fields, parameter schemas,
        operators, and allowed values before recommending a workflow step.
        """
        return self._search_workflow_catalog(
            operation="WorkflowActivitiesContentCombined",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
            },
            error_message="Failed to search workflow activity content",
            filter_used=filter,
        )

    def search_workflow_triggers(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for workflow triggers. Examples include `name:'Detection'` or `name:'FalconAudit/Detection/Status'`.",
        ),
        limit: int = Field(
            default=50,
            ge=1,
            description="Maximum number of workflow triggers to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search Fusion SOAR workflow triggers.

        Start workflow design here to identify the event source and trigger field
        mappings that fit the user's SOAR goal.
        """
        return self._search_workflow_catalog(
            operation="WorkflowTriggersCombined",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
            },
            error_message="Failed to search workflow triggers",
            filter_used=filter,
        )

    def search_workflow_definitions(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for workflow definitions. Use this to find existing workflows similar to the requested goal.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            description="Maximum number of workflow definitions to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
        sort: str | None = Field(
            default=None,
            description="Sort expression such as `updated_on.desc` or `name.asc`.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search existing Fusion SOAR workflow definitions.

        Use matching definitions as tenant-specific examples before recommending
        a new workflow design.
        """
        return self._search_workflow_catalog(
            operation="WorkflowDefinitionsCombined",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
            },
            error_message="Failed to search workflow definitions",
            filter_used=filter,
        )

    def export_workflow_definition(
        self,
        id: str = Field(
            description="Workflow definition ID to export. Find IDs with `falcon_search_workflow_definitions`.",
        ),
        sanitize: bool = Field(
            default=True,
            description="Sanitize PII from the workflow before export. Defaults to true.",
        ),
    ) -> str | list[dict[str, Any]] | dict[str, Any]:
        """Export a workflow definition as YAML for advisory design reference.

        This is read-only and should be used to inspect existing workflow
        structure, field mappings, and action sequences. It does not import or
        modify any workflow.
        """
        return self._export_workflow_yaml(
            operation="WorkflowDefinitionsExport",
            id=id,
            sanitize=sanitize,
        )

    def search_workflow_executions(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for workflow executions.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            description="Maximum number of workflow executions to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
        sort: str | None = Field(
            default=None,
            description="Sort expression such as `created_on.desc` or `updated_on.desc`.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search Fusion SOAR workflow executions.

        Use this to understand recent workflow behavior and execution patterns
        before recommending changes or a new workflow design.
        """
        return self._search_workflow_catalog(
            operation="WorkflowExecutionsCombined",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
            },
            error_message="Failed to search workflow executions",
            filter_used=filter,
        )

    def get_workflow_execution_results(
        self,
        ids: str | list[str] = Field(
            description="Workflow execution ID or IDs to retrieve results for.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Get execution results for one or more workflow executions."""
        return self._get_workflow_by_ids(
            operation="WorkflowExecutionResults",
            ids=ids,
            error_message="Failed to get workflow execution results",
        )

    def get_workflow_human_inputs(
        self,
        ids: str | list[str] = Field(
            description="Human input ID or IDs to retrieve.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Get one or more workflow human input records.

        This is read-only. It does not approve, decline, escalate, or otherwise
        answer a human input request.
        """
        return self._get_workflow_by_ids(
            operation="WorkflowGetHumanInputV1",
            ids=ids,
            error_message="Failed to get workflow human inputs",
        )

    def query_workflow_child_executions(
        self,
        filter: str | None = Field(
            default=None,
            description="FQL filter for child workflow executions.",
        ),
        limit: int = Field(
            default=10,
            ge=1,
            description="Maximum number of child execution IDs to return.",
        ),
        offset: int | None = Field(
            default=None,
            description="Starting pagination offset.",
        ),
        sort: str | None = Field(
            default=None,
            description="Sort expression such as `created_on.desc`.",
        ),
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Search child workflow executions by FQL filter and paging details."""
        return self._search_workflow_catalog(
            operation="v1_child_executions_query",
            search_params={
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "sort": sort,
            },
            error_message="Failed to query child workflow executions",
            filter_used=filter,
        )
