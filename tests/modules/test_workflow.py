"""Tests for the Workflow module."""

import unittest

from falcon_mcp.modules.base import READ_ONLY_ANNOTATIONS
from falcon_mcp.modules.workflow import WorkflowModule
from tests.modules.utils.test_modules import TestModules


class TestWorkflowModule(TestModules):
    """Test cases for the Fusion SOAR Workflow module."""

    def setUp(self):
        """Set up test fixtures."""
        self.setup_module(WorkflowModule)

    def test_register_tools(self):
        """Test registering Workflow tools with the server."""
        expected_tools = [
            "falcon_search_workflow_activities",
            "falcon_search_workflow_activity_content",
            "falcon_search_workflow_triggers",
            "falcon_search_workflow_definitions",
            "falcon_export_workflow_definition",
            "falcon_search_workflow_executions",
            "falcon_get_workflow_execution_results",
            "falcon_get_workflow_human_inputs",
            "falcon_query_workflow_child_executions",
        ]
        self.assert_tools_registered(expected_tools)

    def test_register_resources(self):
        """Test registering Workflow resources with the server."""
        expected_resources = [
            "falcon_workflow_builder_guide",
            "falcon_workflow_fql_guide",
        ]
        self.assert_resources_registered(expected_resources)

    def test_all_tools_have_read_only_annotations(self):
        """Test all Workflow tools are registered as read-only."""
        expected_tools = [
            "falcon_search_workflow_activities",
            "falcon_search_workflow_activity_content",
            "falcon_search_workflow_triggers",
            "falcon_search_workflow_definitions",
            "falcon_export_workflow_definition",
            "falcon_search_workflow_executions",
            "falcon_get_workflow_execution_results",
            "falcon_get_workflow_human_inputs",
            "falcon_query_workflow_child_executions",
        ]
        self.module.register_tools(self.mock_server)
        for tool_name in expected_tools:
            self.assert_tool_annotations(tool_name, READ_ONLY_ANNOTATIONS)

    def test_search_workflow_activities_success(self):
        """Test searching workflow activities."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "activity-1", "name": "Send notification"}]},
        }

        result = self.module.search_workflow_activities(
            filter="name:'notification'",
            limit=25,
            offset=5,
            sort="name.asc",
        )

        self.mock_client.command.assert_called_once_with(
            "WorkflowActivitiesCombined",
            parameters={
                "filter": "name:'notification'",
                "limit": 25,
                "offset": 5,
                "sort": "name.asc",
            },
        )
        self.assertEqual(result[0]["id"], "activity-1")

    def test_search_workflow_activity_content_success(self):
        """Test searching workflow activity content."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "activity-1", "fields": [{"name": "message"}]}]},
        }

        result = self.module.search_workflow_activity_content(filter="name:'notification'")

        self.mock_client.command.assert_called_once_with(
            "WorkflowActivitiesContentCombined",
            parameters={
                "filter": "name:'notification'",
                "limit": 50,
            },
        )
        self.assertEqual(result[0]["id"], "activity-1")

    def test_search_workflow_triggers_success(self):
        """Test searching workflow triggers."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "trigger-1", "name": "Detection"}]},
        }

        result = self.module.search_workflow_triggers(
            filter="name:'Detection'",
            limit=10,
            offset=0,
        )

        self.mock_client.command.assert_called_once_with(
            "WorkflowTriggersCombined",
            parameters={
                "filter": "name:'Detection'",
                "limit": 10,
                "offset": 0,
            },
        )
        self.assertEqual(result[0]["name"], "Detection")

    def test_search_workflow_definitions_success(self):
        """Test searching workflow definitions."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "definition-1", "name": "Contain host"}]},
        }

        result = self.module.search_workflow_definitions(
            filter="name:'Contain host'",
            limit=5,
            sort="name.asc",
        )

        self.mock_client.command.assert_called_once_with(
            "WorkflowDefinitionsCombined",
            parameters={
                "filter": "name:'Contain host'",
                "limit": 5,
                "sort": "name.asc",
            },
        )
        self.assertEqual(result[0]["id"], "definition-1")

    def test_export_workflow_definition_bytes(self):
        """Test exporting workflow definition YAML returned as bytes."""
        self.mock_client.command.return_value = b"name: Example Workflow\n"

        result = self.module.export_workflow_definition(id="definition-1")

        self.mock_client.command.assert_called_once_with(
            "WorkflowDefinitionsExport",
            parameters={"id": "definition-1", "sanitize": True},
        )
        self.assertIsInstance(result, str)
        self.assertIn("Example Workflow", result)

    def test_export_workflow_definition_api_error(self):
        """Test export workflow definition API errors are formatted."""
        self.mock_client.command.return_value = {
            "status_code": 403,
            "body": {"errors": [{"message": "Access denied"}]},
        }

        result = self.module.export_workflow_definition(id="definition-1")

        self.assertIn("error", result)
        self.assertIn("required_scopes", result)
        self.assertEqual(result["required_scopes"], ["workflow:read"])

    def test_search_workflow_executions_success(self):
        """Test searching workflow executions."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "execution-1", "status": "completed"}]},
        }

        result = self.module.search_workflow_executions(
            filter="status:'completed'",
            limit=5,
            offset=1,
            sort="created_on.desc",
        )

        self.mock_client.command.assert_called_once_with(
            "WorkflowExecutionsCombined",
            parameters={
                "filter": "status:'completed'",
                "limit": 5,
                "offset": 1,
                "sort": "created_on.desc",
            },
        )
        self.assertEqual(result[0]["id"], "execution-1")

    def test_get_workflow_execution_results_success(self):
        """Test retrieving workflow execution results by ID."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "execution-1", "result": "ok"}]},
        }

        result = self.module.get_workflow_execution_results(ids=["execution-1"])

        self.mock_client.command.assert_called_once_with(
            "WorkflowExecutionResults",
            parameters={"ids": ["execution-1"]},
        )
        self.assertEqual(result[0]["result"], "ok")

    def test_get_workflow_human_inputs_normalizes_single_id(self):
        """Test retrieving human inputs normalizes a single ID to a list."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": [{"id": "human-input-1", "status": "pending"}]},
        }

        result = self.module.get_workflow_human_inputs(ids="human-input-1")

        self.mock_client.command.assert_called_once_with(
            "WorkflowGetHumanInputV1",
            parameters={"ids": ["human-input-1"]},
        )
        self.assertEqual(result[0]["id"], "human-input-1")

    def test_query_workflow_child_executions_success(self):
        """Test querying child workflow executions."""
        self.mock_client.command.return_value = {
            "status_code": 200,
            "body": {"resources": ["child-execution-1"]},
        }

        result = self.module.query_workflow_child_executions(
            filter="parent_execution_id:'execution-1'",
            limit=20,
            sort="created_on.desc",
        )

        self.mock_client.command.assert_called_once_with(
            "v1_child_executions_query",
            parameters={
                "filter": "parent_execution_id:'execution-1'",
                "limit": 20,
                "sort": "created_on.desc",
            },
        )
        self.assertEqual(result, ["child-execution-1"])

    def test_search_error_returns_fql_guide(self):
        """Test search errors include Workflow FQL guide context."""
        self.mock_client.command.return_value = {
            "status_code": 400,
            "body": {"errors": [{"message": "Invalid filter"}]},
        }

        result = self.module.search_workflow_definitions(filter="bad filter")

        self.assertIsInstance(result, dict)
        self.assertIn("results", result)
        self.assertIn("fql_guide", result)
        self.assertIn("error", result["results"][0])


if __name__ == "__main__":
    unittest.main()
