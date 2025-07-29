#!/usr/bin/env python3
"""
CTX MCP Server for Cursor Integration
Provides ctx functionality as MCP tools for use in Cursor
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class CTXMCPServer:
    """MCP server that exposes ctx functionality"""
    
    def __init__(self):
        self.capabilities = {
            "tools": {
                "ctx_status": {
                    "description": "Get current ctx context status",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                "ctx_list": {
                    "description": "List all ctx contexts",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                "ctx_note": {
                    "description": "Add a note to current ctx context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Note text to add"
                            }
                        },
                        "required": ["text"]
                    }
                },
                "ctx_set_state": {
                    "description": "Set ctx context state",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "state": {
                                "type": "string",
                                "enum": ["active", "in-progress", "on-hold", "in-review", "blocked", "pending", "completed", "cancelled"],
                                "description": "State to set"
                            }
                        },
                        "required": ["state"]
                    }
                },
                "ctx_create": {
                    "description": "Create a new ctx context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Context name"
                            },
                            "description": {
                                "type": "string",
                                "description": "Context description"
                            }
                        },
                        "required": ["name"]
                    }
                },
                "ctx_switch": {
                    "description": "Switch to a different ctx context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Context name to switch to"
                            }
                        },
                        "required": ["name"]
                    }
                }
            }
        }
    
    def run_ctx_command(self, args: List[str]) -> Dict[str, Any]:
        """Run a ctx command and return the result"""
        try:
            result = subprocess.run(
                ["ctx"] + args,
                capture_output=True,
                text=True,
                timeout=30
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
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def handle_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool call"""
        
        if tool_name == "ctx_status":
            result = self.run_ctx_command(["status"])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result["stdout"] if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        elif tool_name == "ctx_list":
            result = self.run_ctx_command(["list"])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result["stdout"] if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        elif tool_name == "ctx_note":
            text = parameters.get("text", "")
            result = self.run_ctx_command(["note", text])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"✅ Note added: {text}" if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        elif tool_name == "ctx_set_state":
            state = parameters.get("state", "active")
            result = self.run_ctx_command(["set-state", state])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result["stdout"] if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        elif tool_name == "ctx_create":
            name = parameters.get("name", "")
            description = parameters.get("description", "")
            args = ["create", name]
            if description:
                args.extend(["-d", description])
            
            result = self.run_ctx_command(args)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"✅ Created context: {name}" if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        elif tool_name == "ctx_switch":
            name = parameters.get("name", "")
            result = self.run_ctx_command(["switch", name])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result["stdout"] if result["success"] else f"Error: {result['stderr']}"
                    }
                ]
            }
        
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}"
                    }
                ],
                "isError": True
            }


def main():
    """Main MCP server loop"""
    server = CTXMCPServer()
    
    for line in sys.stdin:
        try:
            message = json.loads(line.strip())
            
            if message.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": name,
                                "description": tool["description"],
                                "inputSchema": tool["parameters"]
                            }
                            for name, tool in server.capabilities["tools"].items()
                        ]
                    }
                }
                print(json.dumps(response))
                
            elif message.get("method") == "tools/call":
                params = message.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = server.handle_tool_call(tool_name, arguments)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": result
                }
                print(json.dumps(response))
                
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id") if 'message' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))


if __name__ == "__main__":
    main()