"""
Pytest configuration and shared fixtures for ctx-tools testing
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import json
import subprocess
import sys
import os

# Add the project root to the path so we can import ctx modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctx.core import ContextManager
from ctx.models import Context, ContextState
from ctx.storage import JsonStorage


@pytest.fixture
def temp_storage_dir():
    """Create a temporary directory for test storage"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture  
def ctx_manager(temp_storage_dir):
    """Create a ContextManager with temporary storage"""
    manager = ContextManager(storage_path=temp_storage_dir)
    return manager


@pytest.fixture
def sample_context():
    """Create a sample context for testing"""
    return Context(
        name="test-context",
        description="A test context",
        state=ContextState.ACTIVE,
        tags=["test", "sample"]
    )


@pytest.fixture
def populated_manager(ctx_manager):
    """Create a manager with some test contexts"""
    # Create test contexts
    ctx_manager.create("context-1", "First test context", tags=["test"])
    ctx_manager.create("context-2", "Second test context", tags=["test", "demo"])
    ctx_manager.create("completed-context", "Completed context")
    ctx_manager.set_state("completed-context", ContextState.COMPLETED)
    
    # Add some notes
    ctx_manager.add_note("context-1", "First note")
    ctx_manager.add_note("context-1", "Second note", tags=["important"])
    
    return ctx_manager


@pytest.fixture
def cli_runner():
    """Create a CLI test runner"""
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for CLI testing"""
    with patch('subprocess.run') as mock_run:
        yield mock_run


@pytest.fixture
def mcp_test_client():
    """Create a test client for MCP integration testing"""
    import sys
    import subprocess
    from pathlib import Path
    
    class MCPTestClient:
        def __init__(self):
            self.script_path = Path(__file__).parent.parent / "cursor_ctx_integration.py"
            
        def send_request(self, method, params=None, request_id=1):
            """Send a JSON-RPC request to the MCP server"""
            request = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method
            }
            if params:
                request["params"] = params
                
            try:
                result = subprocess.run(
                    [sys.executable, str(self.script_path)],
                    input=json.dumps(request),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.stdout:
                    return json.loads(result.stdout)
                return None
                
            except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
                pytest.fail(f"MCP server communication failed: {e}")
                
        def initialize(self):
            """Initialize the MCP server"""
            return self.send_request("initialize", {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            })
            
        def list_tools(self):
            """Get available tools"""
            return self.send_request("tools/list")
            
        def call_tool(self, tool_name, arguments=None):
            """Call a specific tool"""
            return self.send_request("tools/call", {
                "name": tool_name,
                "arguments": arguments or {}
            })
    
    return MCPTestClient()


@pytest.fixture
def multimodal_test_env(temp_storage_dir, mcp_test_client):
    """Set up environment for multimodal testing"""
    # Set up environment variables for consistent storage
    os.environ['CTX_STORAGE_PATH'] = str(temp_storage_dir)
    
    class MultimodalTestEnv:
        def __init__(self, storage_dir, mcp_client):
            self.storage_dir = storage_dir
            self.mcp_client = mcp_client
            self.manager = ContextManager(storage_path=storage_dir)
            
        def create_test_context(self, name="test-context"):
            """Create a test context via API"""
            return self.manager.create(name, f"Test context {name}")
            
        def run_cli_command(self, command):
            """Run a CLI command and return the result"""
            try:
                result = subprocess.run(
                    ["ctx"] + command.split() if isinstance(command, str) else ["ctx"] + command,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env={**os.environ, 'CTX_STORAGE_PATH': str(self.storage_dir)}
                )
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": "Command timed out",
                    "returncode": -1
                }
                
        def verify_sync(self, context_name):
            """Verify that CLI and MCP show consistent data"""
            # Get data via API
            api_context = self.manager.get(context_name)
            
            # Get data via MCP
            mcp_result = self.mcp_client.call_tool("ctx_status")
            
            # Get data via CLI
            cli_result = self.run_cli_command(["status", context_name])
            
            return {
                "api_context": api_context,
                "mcp_result": mcp_result,
                "cli_result": cli_result
            }
    
    yield MultimodalTestEnv(temp_storage_dir, mcp_test_client)
    
    # Cleanup
    if 'CTX_STORAGE_PATH' in os.environ:
        del os.environ['CTX_STORAGE_PATH']


# Test markers
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests for core functionality")
    config.addinivalue_line("markers", "integration: Integration tests for CLI and components")
    config.addinivalue_line("markers", "mcp: MCP server integration tests")
    config.addinivalue_line("markers", "multimodal: Tests for CLI-MCP synchronization")
    config.addinivalue_line("markers", "slow: Tests that take longer to run")