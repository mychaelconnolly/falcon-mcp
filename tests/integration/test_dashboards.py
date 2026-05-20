"""Integration tests for the Dashboards module."""

import os
from uuid import uuid4

import pytest

from falcon_mcp.modules.dashboards import DashboardsModule
from tests.integration.utils.base_integration_test import BaseIntegrationTest


@pytest.mark.integration
class TestDashboardsIntegration(BaseIntegrationTest):
    """Integration tests for NGSIEM dashboard operations with real API calls."""

    @pytest.fixture(autouse=True)
    def setup_module(self, falcon_client):
        """Set up the Dashboards module with a real client."""
        self.module = DashboardsModule(falcon_client)

    def test_list_dashboards_operation_name(self):
        """Validate ListDashboards operation name and response shape."""
        result = self.call_method(
            self.module.list_dashboards,
            limit=1,
            offset=0,
            search_domain="all",
        )

        self.assert_no_error(result, context="ListDashboards")
        self.assert_valid_list_response(result, min_length=0, context="ListDashboards")

    def test_get_dashboard_template_operation_name_when_dashboard_exists(self):
        """Validate GetDashboardTemplate when a dashboard ID is available."""
        dashboards = self.call_method(
            self.module.list_dashboards,
            limit=1,
            offset=0,
            search_domain="all",
        )
        self.assert_no_error(dashboards, context="ListDashboards for template lookup")
        self.assert_valid_list_response(dashboards, min_length=0, context="dashboards")

        dashboard_id = self.get_first_id(dashboards)
        if not dashboard_id:
            self.skip_with_warning(
                "No dashboards available to validate GetDashboardTemplate",
                context="dashboards integration",
            )

        result = self.call_method(
            self.module.get_dashboard_template,
            ids=dashboard_id,
            search_domain="all",
        )

        self.assert_no_error(result, context="GetDashboardTemplate")
        self.assert_valid_list_response(result, min_length=0, context="GetDashboardTemplate")

    def test_create_dashboard_from_template_skipped_by_default(self):
        """Validate CreateDashboardFromTemplate only when explicitly enabled."""
        if os.getenv("FALCON_MCP_RUN_DASHBOARD_CREATE_TEST") != "1":
            self.skip_with_warning(
                "Dashboard create integration test requires FALCON_MCP_RUN_DASHBOARD_CREATE_TEST=1",
                context="mutating NGSIEM dashboard create",
            )

        name = f"falcon-mcp-integration-test-{uuid4().hex[:8]}"
        yaml_template = f"name: {name}\ndescription: Created by falcon-mcp integration tests\nwidgets: []\n"
        result = self.call_method(
            self.module.create_dashboard_from_template,
            name=name,
            yaml_template=yaml_template,
            search_domain="falcon",
        )

        self.assert_no_error(result, context="CreateDashboardFromTemplate")
        self.assert_valid_list_response(result, min_length=0, context="CreateDashboardFromTemplate")

        dashboard_id = self.get_first_id(result)
        if dashboard_id:
            self.module.client.command(
                operation="DeleteDashboard",
                ids=dashboard_id,
                search_domain="falcon",
            )
