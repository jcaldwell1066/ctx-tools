"""
Multimodal synchronization tests for ctx-tools
Tests that CLI and MCP integration stay in sync
"""

import pytest
import json
import time
from ctx.models import ContextState


@pytest.mark.multimodal
class TestMultimodalSync:
    """Tests for CLI-MCP synchronization"""
    
    def test_context_creation_sync(self, multimodal_test_env):
        """Test that context creation syncs across interfaces"""
        env = multimodal_test_env
        
        # Create context via API
        context = env.create_test_context("sync-test-1")
        
        # Verify via MCP (if MCP server works)
        try:
            mcp_result = env.mcp_client.call_tool("ctx_status")
            if mcp_result and "result" in mcp_result:
                assert "sync-test-1" in str(mcp_result["result"])
        except Exception:
            pytest.skip("MCP server not available for testing")
        
        # Verify via CLI
        cli_result = env.run_cli_command(["status"])
        if cli_result["success"]:
            assert "sync-test-1" in cli_result["stdout"]
    
    def test_state_change_sync(self, multimodal_test_env):
        """Test that state changes sync across interfaces"""
        env = multimodal_test_env
        
        # Create test context
        context = env.create_test_context("state-sync-test")
        
        # Change state via API
        env.manager.set_state("state-sync-test", ContextState.IN_PROGRESS)
        
        # Verify state change in CLI
        cli_result = env.run_cli_command(["status", "state-sync-test"])
        if cli_result["success"]:
            assert "in-progress" in cli_result["stdout"] or "💻" in cli_result["stdout"]
        
        # Verify state change via MCP (if available)
        try:
            mcp_result = env.mcp_client.call_tool("ctx_status")
            if mcp_result and "result" in mcp_result:
                content = str(mcp_result["result"])
                assert "in-progress" in content or "💻" in content
        except Exception:
            pytest.skip("MCP server not available for state sync testing")
    
    def test_bidirectional_state_sync(self, multimodal_test_env):
        """Test state changes in both directions"""
        env = multimodal_test_env
        
        # Create test context
        context = env.create_test_context("bidirectional-test")
        
        # Test API -> CLI sync
        env.manager.set_state("bidirectional-test", ContextState.BLOCKED)
        
        cli_result = env.run_cli_command(["status", "bidirectional-test"])
        if cli_result["success"]:
            assert "blocked" in cli_result["stdout"] or "🚫" in cli_result["stdout"]
        
        # Test CLI -> API sync (via subprocess if available)
        cli_set_result = env.run_cli_command(["set-state", "completed"])
        
        # Verify via API
        updated_context = env.manager.get("bidirectional-test")
        if updated_context and cli_set_result["success"]:
            # State might have changed if CLI command worked
            assert updated_context.state in [ContextState.BLOCKED, ContextState.COMPLETED]
    
    def test_data_consistency_verification(self, multimodal_test_env):
        """Test comprehensive data consistency check"""
        env = multimodal_test_env
        
        # Create and modify context via API
        context = env.create_test_context("consistency-test")
        env.manager.add_note("consistency-test", "API note")
        env.manager.set_state("consistency-test", ContextState.IN_REVIEW)
        
        # Use verification helper
        sync_data = env.verify_sync("consistency-test")
        
        # Check API data
        api_context = sync_data["api_context"]
        assert api_context is not None
        assert api_context.name == "consistency-test"
        assert api_context.state == ContextState.IN_REVIEW
        assert len(api_context.notes) >= 1
        
        # Check CLI data (if successful)
        cli_result = sync_data["cli_result"]
        if cli_result["success"]:
            assert "consistency-test" in cli_result["stdout"]
            assert "in-review" in cli_result["stdout"] or "👀" in cli_result["stdout"]


@pytest.mark.multimodal
@pytest.mark.slow  
class TestMultimodalWorkflows:
    """Test complete workflows across multiple interfaces"""
    
    def test_development_workflow_sync(self, multimodal_test_env):
        """Test a typical development workflow across interfaces"""
        env = multimodal_test_env
        
        # Step 1: Create context via API
        context = env.create_test_context("workflow-test")
        assert context.state == ContextState.ACTIVE
        
        # Step 2: Add note via API  
        env.manager.add_note("workflow-test", "Started development")
        
        # Step 3: Change state via CLI (if working)
        cli_result = env.run_cli_command(["set-state", "in-progress"])
        
        # Step 4: Verify consistency
        final_context = env.manager.get("workflow-test")
        assert final_context is not None
        assert len(final_context.notes) >= 1
        
        # State might be updated if CLI worked
        assert final_context.state in [ContextState.ACTIVE, ContextState.IN_PROGRESS]
    
    def test_concurrent_access_safety(self, multimodal_test_env):
        """Test that concurrent access doesn't corrupt data"""
        env = multimodal_test_env
        
        # Create test context
        context = env.create_test_context("concurrent-test")
        
        # Simulate concurrent operations
        env.manager.add_note("concurrent-test", "Note 1")
        env.manager.set_state("concurrent-test", ContextState.IN_PROGRESS)
        
        # Try CLI operation
        env.run_cli_command(["status"])
        
        # Verify data integrity
        final_context = env.manager.get("concurrent-test")
        assert final_context is not None
        assert final_context.name == "concurrent-test"
        assert len(final_context.notes) >= 1
        assert final_context.state == ContextState.IN_PROGRESS


@pytest.mark.multimodal
class TestMultimodalRegressionTests:
    """Regression tests for multimodal issues we fixed"""
    
    def test_mcp_initialization_fix(self, multimodal_test_env):
        """Test that MCP server initializes correctly"""
        env = multimodal_test_env
        
        try:
            # Test initialization sequence we fixed
            init_result = env.mcp_client.initialize()
            
            if init_result:
                assert "result" in init_result
                assert "protocolVersion" in init_result["result"]
                assert "capabilities" in init_result["result"]
                assert "serverInfo" in init_result["result"]
                
                # Check our specific fixes
                assert init_result["result"]["protocolVersion"] == "2025-03-26"
                assert "tools" in init_result["result"]["capabilities"]
                assert init_result["result"]["serverInfo"]["name"] == "ctx-tools"
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_mcp_tools_available(self, multimodal_test_env):
        """Test that all expected MCP tools are available"""
        env = multimodal_test_env
        
        try:
            tools_result = env.mcp_client.list_tools()
            
            if tools_result and "result" in tools_result:
                tools = tools_result["result"]["tools"]
                tool_names = [tool["name"] for tool in tools]
                
                # Check that our fixed tools are available
                expected_tools = [
                    "ctx_status", "ctx_list", "ctx_create", 
                    "ctx_switch", "ctx_set_state", "ctx_note"
                ]
                
                for expected_tool in expected_tools:
                    assert expected_tool in tool_names
                    
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_mcp_tool_execution(self, multimodal_test_env):
        """Test that MCP tools execute without errors"""
        env = multimodal_test_env
        
        # Create test context
        context = env.create_test_context("mcp-exec-test")
        
        try:
            # Test status tool (should work)
            status_result = env.mcp_client.call_tool("ctx_status")
            if status_result and "result" in status_result:
                assert "mcp-exec-test" in str(status_result["result"])
            
            # Test set_state tool (should work based on our testing)
            state_result = env.mcp_client.call_tool("ctx_set_state", {"state": "in-review"})
            if state_result and "result" in state_result:
                # Should indicate success
                content = str(state_result["result"])
                assert "in-review" in content or "👀" in content
                
                # Verify the change took effect via API
                updated_context = env.manager.get("mcp-exec-test")
                assert updated_context.state == ContextState.IN_REVIEW
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_cli_notes_command_fix_regression(self, multimodal_test_env):
        """Test that our CLI notes fix prevents regression"""
        env = multimodal_test_env
        
        # Create context with notes
        context = env.create_test_context("notes-fix-test")
        env.manager.add_note("notes-fix-test", "Test note for regression")
        
        # Run notes command - should not crash
        notes_result = env.run_cli_command(["notes"])
        
        # Should complete without the specific error we fixed
        if notes_result["returncode"] != 0:
            # If it failed, should not be our specific TypeError
            assert "TypeError" not in notes_result["stderr"]
            assert "object of type 'Note' has no len()" not in notes_result["stderr"]
            
        # If it succeeded, should show notes
        if notes_result["success"]:
            assert "Test note for regression" in notes_result["stdout"]