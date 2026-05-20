"""
Dashboards module for Falcon MCP Server.

This module provides tools for reading and creating NGSIEM dashboards from
LogScale dashboard YAML templates.
"""

from typing import Any

from mcp.server import FastMCP
from mcp.server.fastmcp.resources import TextResource
from mcp.types import ToolAnnotations
from pydantic import AnyUrl

from falcon_mcp.common.errors import handle_api_response
from falcon_mcp.common.utils import prepare_api_parameters
from falcon_mcp.modules.base import BaseModule
from falcon_mcp.resources.dashboards import SEARCH_DASHBOARDS_FQL_DOCUMENTATION


class DashboardsModule(BaseModule):
    """Module for reading and creating NGSIEM dashboards."""

    def register_tools(self, server: FastMCP) -> None:
        """Register tools."""
        self._add_tool(
            server=server,
            method=self.list_dashboards,
            name="list_dashboards",
        )
        self._add_tool(
            server=server,
            method=self.get_dashboard_template,
            name="get_dashboard_template",
        )
        self._add_tool(
            server=server,
            method=self.create_dashboard_from_template,
            name="create_dashboard_from_template",
            annotations=ToolAnnotations(
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )

    def register_resources(self, server: FastMCP) -> None:
        """Register resources."""
        resource = TextResource(
            uri=AnyUrl("falcon://dashboards/search/fql-guide"),
            name="falcon_search_dashboards_fql_guide",
            description="FQL guide for `falcon_list_dashboards` filter syntax.",
            text=SEARCH_DASHBOARDS_FQL_DOCUMENTATION,
        )
        self._add_resource(server, resource)

    def list_dashboards(
        self,
        filter: str | None = None,
        limit: int = 50,
        offset: int = 0,
        search_domain: str = "all",
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """List NGSIEM dashboards."""
        params = prepare_api_parameters(
            {
                "filter": filter,
                "limit": limit,
                "offset": offset,
                "search_domain": search_domain,
            }
        )
        response = self.client.command(operation="ListDashboards", **params)
        return handle_api_response(
            response,
            operation="ListDashboards",
            error_message="Failed to list NGSIEM dashboards",
            default_result=[],
        )

    def get_dashboard_template(
        self,
        ids: str,
        search_domain: str = "all",
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Export NGSIEM dashboard YAML."""
        params = prepare_api_parameters(
            {
                "ids": ids,
                "search_domain": search_domain,
            }
        )
        response = self.client.command(operation="GetDashboardTemplate", **params)
        return handle_api_response(
            response,
            operation="GetDashboardTemplate",
            error_message="Failed to get NGSIEM dashboard template",
            default_result=[],
        )

    def create_dashboard_from_template(
        self,
        name: str,
        yaml_template: str,
        search_domain: str = "falcon",
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Create NGSIEM dashboard from YAML."""
        response = self.client.command(
            operation="CreateDashboardFromTemplate",
            search_domain=search_domain,
            name=name,
            yaml_template=yaml_template,
        )
        return handle_api_response(
            response,
            operation="CreateDashboardFromTemplate",
            error_message="Failed to create NGSIEM dashboard from template",
            default_result=[],
        )
