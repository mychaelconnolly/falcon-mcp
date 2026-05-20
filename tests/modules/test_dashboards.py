"""Tests for the Dashboards module."""

from mcp.types import ToolAnnotations

from falcon_mcp.modules.base import READ_ONLY_ANNOTATIONS
from falcon_mcp.modules.dashboards import DashboardsModule
from tests.modules.utils.test_modules import TestModules


class TestDashboardsModule(TestModules):
    """Test cases for the NGSIEM Dashboards module."""

    def setUp(self):
        """Set up test fixtures."""
        self.setup_module(DashboardsModule)

    def test_register_tools(self):
        """Test registering dashboard tools with the server."""
        expected_tools = [
            "falcon_list_dashboards",
            "falcon_get_dashboard_template",
            "falcon_create_dashboard_from_template",
        ]
        self.assert_tools_registered(expected_tools)

    def test_register_resources(self):
        """Test registering dashboard resources with the server."""
        expected_resources = [
            "falcon_search_dashboards_fql_guide",
        ]
        self.assert_resources_registered(expected_resources)

    def test_tool_annotations(self):
        """Test dashboard tool annotations."""
        self.module.register_tools(self.mock_server)

        self.assert_tool_annotations("falcon_list_dashboards", READ_ONLY_ANNOTATIONS)
        self.assert_tool_annotations("falcon_get_dashboard_template", READ_ONLY_ANNOTATIONS)
        self.assert_tool_annotations(
            "falcon_create_dashboard_from_template",
            ToolAnnotations(
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )

    def test_list_dashboards_success(self):
        """Test listing dashboards."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {
                "resources": [
                    {"id": "dashboard-1", "name": "Windows Overview"},
                    {"id": "dashboard-2", "name": "Identity Overview"},
                ]
            },
        }

        result = self.module.list_dashboards(
            filter="name:~'Overview'",
            limit=25,
            offset=5,
            search_domain="dashboards",
        )

        self.mock_client.command.assert_called_once_with(
            operation="ListDashboards",
            filter="name:~'Overview'",
            limit=25,
            offset=5,
            search_domain="dashboards",
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "dashboard-1")

    def test_list_dashboards_filters_none_values(self):
        """Test list_dashboards omits optional None values."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": []},
        }

        result = self.module.list_dashboards()

        self.mock_client.command.assert_called_once_with(
            operation="ListDashboards",
            limit=50,
            offset=0,
            search_domain="all",
        )
        self.assertEqual(result, [])

    def test_get_dashboard_template_success(self):
        """Test exporting a dashboard template."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {
                "resources": [
                    {
                        "id": "dashboard-1",
                        "yaml_template": "name: Windows Overview\nwidgets: []\n",
                    }
                ]
            },
        }

        result = self.module.get_dashboard_template(
            ids="dashboard-1",
            search_domain="falcon",
        )

        self.mock_client.command.assert_called_once_with(
            operation="GetDashboardTemplate",
            ids="dashboard-1",
            search_domain="falcon",
        )
        self.assertEqual(result[0]["id"], "dashboard-1")
        self.assertIn("yaml_template", result[0])

    def test_create_dashboard_from_template_success(self):
        """Test creating a dashboard from YAML template content."""
        yaml_template = "name: Falcon MCP Test\nwidgets: []\n"
        self.mock_client.command.return_value = {
            "status_code": 201,
            "body": {
                "resources": [
                    {
                        "id": "dashboard-created",
                        "name": "Falcon MCP Test",
                    }
                ]
            },
        }

        result = self.module.create_dashboard_from_template(
            name="Falcon MCP Test",
            yaml_template=yaml_template,
            search_domain="falcon",
        )

        self.mock_client.command.assert_called_once_with(
            operation="CreateDashboardFromTemplate",
            search_domain="falcon",
            name="Falcon MCP Test",
            yaml_template=yaml_template,
        )
        call_kwargs = self.mock_client.command.call_args.kwargs
        self.assertNotIn("body", call_kwargs)
        self.assertNotIn("parameters", call_kwargs)
        self.assertEqual(result[0]["id"], "dashboard-created")

    def test_permission_error_includes_dashboard_scopes(self):
        """Test dashboard scope appears in 403 error responses."""
        self.mock_client.command.return_value = {
            "status_code": 403,
            "body": {"errors": [{"message": "Forbidden"}]},
        }

        result = self.module.create_dashboard_from_template(
            name="Forbidden Dashboard",
            yaml_template="name: Forbidden Dashboard\nwidgets: []\n",
        )

        self.assertIn("error", result)
        self.assertEqual(result["required_scopes"], ["ngsiem-dashboards:write"])
