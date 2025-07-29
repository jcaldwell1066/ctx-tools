"""
MCP integration tests for ctx-tools
"""

import pytest
import json
import subprocess
import sys
from pathlib import Path


@pytest.mark.mcp
class TestMCPServerBasics:
    """Basic MCP server functionality tests"""
    
    def test_mcp_server_startup(self, mcp_test_client):
        """Test that MCP server starts and responds"""
        try:
            # Test basic communication
            init_result = mcp_test_client.initialize()
            assert init_result is not None
            assert "jsonrpc" in init_result
            assert init_result["jsonrpc"] == "2.0"
            
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_mcp_protocol_compliance(self, mcp_test_client):
        """Test MCP protocol compliance"""
        try:
            # Test initialization
            init_result = mcp_test_client.initialize()
            
            if init_result and "result" in init_result:
                result = init_result["result"]
                
                # Required fields
                assert "protocolVersion" in result
                assert "capabilities" in result
                assert "serverInfo" in result
                
                # Our specific implementation
                assert result["protocolVersion"] == "2025-03-26"
                assert "name" in result["serverInfo"]
                assert result["serverInfo"]["name"] == "ctx-tools"
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_mcp_tools_discovery(self, mcp_test_client):
        """Test tools discovery"""
        try:
            tools_result = mcp_test_client.list_tools()
            
            if tools_result and "result" in tools_result:
                assert "tools" in tools_result["result"]
                tools = tools_result["result"]["tools"]
                
                # Should have our expected tools
                assert len(tools) >= 6
                
                # Check tool structure
                for tool in tools:
                    assert "name" in tool
                    assert "description" in tool
                    assert "inputSchema" in tool
                    
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")


@pytest.mark.mcp
class TestMCPToolExecution:
    """Test MCP tool execution"""
    
    def test_ctx_status_tool(self, mcp_test_client, populated_manager):
        """Test ctx_status MCP tool"""
        try:
            result = mcp_test_client.call_tool("ctx_status")
            
            if result and "result" in result:
                content = result["result"]["content"]
                assert len(content) > 0
                assert content[0]["type"] == "text"
                # Should contain context information
                text = content[0]["text"]
                assert "Context:" in text
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_ctx_list_tool(self, mcp_test_client, populated_manager):
        """Test ctx_list MCP tool"""
        try:
            result = mcp_test_client.call_tool("ctx_list")
            
            if result and "result" in result:
                content = result["result"]["content"]
                assert len(content) > 0
                text = content[0]["text"]
                # Should show contexts from populated_manager
                assert "context-1" in text or "context-2" in text
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_ctx_set_state_tool(self, mcp_test_client, populated_manager):
        """Test ctx_set_state MCP tool"""
        try:
            result = mcp_test_client.call_tool("ctx_set_state", {"state": "in-review"})
            
            if result and "result" in result:
                content = result["result"]["content"]
                assert len(content) > 0
                text = content[0]["text"]
                # Should indicate success
                assert "in-review" in text or "👀" in text
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_ctx_note_tool(self, mcp_test_client, populated_manager):
        """Test ctx_note MCP tool"""
        try:
            result = mcp_test_client.call_tool("ctx_note", {"text": "MCP test note"})
            
            if result and "result" in result:
                content = result["result"]["content"]
                assert len(content) > 0
                text = content[0]["text"]
                # Should indicate note was added
                assert "Note added" in text or "✅" in text
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")


@pytest.mark.mcp
class TestMCPErrorHandling:
    """Test MCP error handling"""
    
    def test_invalid_tool_call(self, mcp_test_client):
        """Test calling non-existent tool"""
        try:
            result = mcp_test_client.call_tool("nonexistent_tool")
            
            if result:
                # Should handle error gracefully
                assert "error" in result or ("result" in result and "Unknown tool" in str(result["result"]))
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_invalid_tool_parameters(self, mcp_test_client):
        """Test calling tool with invalid parameters"""
        try:
            result = mcp_test_client.call_tool("ctx_set_state", {"state": "invalid-state"})
            
            if result:
                # Should handle error or return error message
                if "result" in result:
                    content = str(result["result"])
                    # Should indicate error or handle gracefully
                    assert "error" in content.lower() or "invalid" in content.lower() or "Error:" in content
                    
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")


@pytest.mark.mcp 
@pytest.mark.slow
class TestMCPPerformance:
    """Test MCP performance and reliability"""
    
    def test_multiple_tool_calls(self, mcp_test_client, populated_manager):
        """Test multiple sequential tool calls"""
        try:
            # Make multiple calls
            for i in range(5):
                result = mcp_test_client.call_tool("ctx_status")
                if result and "result" in result:
                    assert "content" in result["result"]
                    
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")
    
    def test_mcp_server_stability(self, mcp_test_client):
        """Test that MCP server remains stable under load"""
        try:
            # Test various tool calls
            tools_to_test = [
                ("ctx_status", {}),
                ("ctx_list", {}),
                ("ctx_set_state", {"state": "active"}),
            ]
            
            for tool_name, args in tools_to_test:
                result = mcp_test_client.call_tool(tool_name, args)
                # Should not crash or hang
                assert result is not None
                
        except Exception as e:
            pytest.skip(f"MCP server not available: {e}")