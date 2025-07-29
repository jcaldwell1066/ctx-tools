"""
Sprint management plugin for ctx
"""

from typing import Dict, Any, Optional
from datetime import datetime

from ctx.plugins import Plugin
from ctx.models import Context, ContextState, Note


class SprintPlugin(Plugin):
    """Plugin for managing sprint-based development workflows"""
    
    name = "sprint"
    description = "Sprint lifecycle management for agile development"
    version = "1.0.0"
    
    # Sprint phases with emojis
    PHASES = {
        "new": ("New Item", "🆕"),
        "refinement": ("Refinement", "📋"),
        "planning": ("Planning", "📅"),
        "development": ("Development", "💻"),
        "review": ("Code Review", "🔍"),
        "qa-handoff": ("QA Handoff", "🧪"),
        "qa-testing": ("QA Testing", "✅"),
        "stage": ("Stage Deploy", "🚀"),
        "production": ("Production", "🎯"),
    }
    
    def get_commands(self) -> Dict[str, Any]:
        """Get sprint-specific commands"""
        return {
            "sprint-init": {
                "help": "Initialize sprint tracking for a context",
                "handler": self.init_sprint
            },
            "sprint-phase": {
                "help": "Update sprint phase",
                "handler": self.update_phase
            },
            "sprint-info": {
                "help": "Show sprint information",
                "handler": self.show_info
            }
        }
    
    def on_context_created(self, context: Context):
        """Initialize sprint data when context is created"""
        # Check if this looks like a sprint item (e.g., PROJECT-123)
        if self._is_sprint_item(context.name):
            context.plugin_data[self.name] = {
                "phase": "new",
                "jira_url": f"https://jira.example.com/browse/{context.name}",
                "branch": f"feature/{context.name}",
                "pr_number": None,
                "pr_url": None,
                "test_results": [],
                "handoff_generated": False,
                "phase_history": [
                    {
                        "phase": "new",
                        "timestamp": datetime.now().isoformat(),
                        "note": "Sprint item initialized"
                    }
                ]
            }
            
            # Set appropriate emoji
            context.set_state(ContextState.ACTIVE, self.PHASES["new"][1])
    
    def on_state_changed(self, context: Context, new_state: ContextState):
        """Update sprint phase based on state changes"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return
        
        # Map states to phases
        state_to_phase = {
            ContextState.IN_PROGRESS: "development",
            ContextState.IN_REVIEW: "review",
            ContextState.PENDING: "qa-handoff",
            ContextState.COMPLETED: "production"
        }
        
        if new_state in state_to_phase:
            phase = state_to_phase[new_state]
            self._update_phase(context, phase, f"Auto-updated from state change to {new_state.value}")
    
    def get_status_info(self, context: Context) -> Optional[str]:
        """Get sprint-specific status information"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return None
        
        phase = sprint_data.get("phase", "unknown")
        phase_info = self.PHASES.get(phase, ("Unknown", "❓"))
        
        info_parts = [f"Sprint Phase: {phase_info[0]}"]
        
        if sprint_data.get("pr_number"):
            info_parts.append(f"PR: #{sprint_data['pr_number']}")
        
        test_count = len(sprint_data.get("test_results", []))
        if test_count > 0:
            passed = sum(1 for t in sprint_data["test_results"] if t["result"] == "pass")
            info_parts.append(f"Tests: {passed}/{test_count} passed")
        
        return " | ".join(info_parts)
    
    def get_ps1_info(self, context: Context) -> Optional[str]:
        """Get sprint PS1 information"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return None
        
        phase = sprint_data.get("phase", "unknown")
        if phase in self.PHASES:
            return self.PHASES[phase][1]
        
        return None
    
    # Command handlers
    
    def init_sprint(self, context: Context, jira_url: str = None, branch: str = None):
        """Initialize sprint tracking for a context"""
        if self.name in context.plugin_data:
            return "Sprint tracking already initialized"
        
        sprint_data = {
            "phase": "new",
                            "jira_url": jira_url or f"https://jira.example.com/browse/{context.name}",
            "branch": branch or f"feature/{context.name}",
            "pr_number": None,
            "pr_url": None,
            "test_results": [],
            "handoff_generated": False,
            "phase_history": [
                {
                    "phase": "new",
                    "timestamp": datetime.now().isoformat(),
                    "note": "Sprint tracking initialized"
                }
            ]
        }
        
        context.plugin_data[self.name] = sprint_data
        context.add_note(f"Sprint tracking initialized - Jira: {sprint_data['jira_url']}")
        
        return "Sprint tracking initialized successfully"
    
    def update_phase(self, context: Context, phase: str, note: str = ""):
        """Update the sprint phase"""
        if phase not in self.PHASES:
            return f"Invalid phase. Valid phases: {', '.join(self.PHASES.keys())}"
        
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return "Sprint tracking not initialized. Use 'sprint-init' first."
        
        old_phase = sprint_data.get("phase", "unknown")
        if old_phase == phase:
            return f"Already in phase: {phase}"
        
        self._update_phase(context, phase, note or f"Phase updated from {old_phase} to {phase}")
        
        # Update context emoji
        context.set_state(context.state, self.PHASES[phase][1])
        
        return f"Phase updated to: {self.PHASES[phase][0]} {self.PHASES[phase][1]}"
    
    def show_info(self, context: Context) -> str:
        """Show detailed sprint information"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return "No sprint tracking data available"
        
        lines = ["Sprint Information:", "-" * 40]
        
        phase = sprint_data.get("phase", "unknown")
        phase_info = self.PHASES.get(phase, ("Unknown", "❓"))
        lines.append(f"Current Phase: {phase_info[0]} {phase_info[1]}")
        
        lines.append(f"JIRA: {sprint_data.get('jira_url', 'Not set')}")
        lines.append(f"Branch: {sprint_data.get('branch', 'Not set')}")
        
        if sprint_data.get("pr_number"):
            lines.append(f"PR: #{sprint_data['pr_number']} - {sprint_data.get('pr_url', '')}")
        
        # Test results
        test_results = sprint_data.get("test_results", [])
        if test_results:
            lines.append(f"\nTest Results ({len(test_results)} total):")
            for test in test_results[-5:]:  # Show last 5
                result_emoji = "✅" if test["result"] == "pass" else "❌"
                lines.append(f"  {result_emoji} {test['type']}: {test.get('details', '')}")
        
        # Phase history
        history = sprint_data.get("phase_history", [])
        if len(history) > 1:
            lines.append(f"\nPhase History (last 5):")
            for entry in history[-5:]:
                timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
                phase_emoji = self.PHASES.get(entry["phase"], ("", ""))[1]
                lines.append(f"  [{timestamp}] {entry['phase']} {phase_emoji}")
                if entry.get("note"):
                    lines.append(f"    {entry['note']}")
        
        return "\n".join(lines)
    
    # Helper methods
    
    def _is_sprint_item(self, name: str) -> bool:
        """Check if a context name looks like a sprint item"""
        # Simple heuristic: contains hyphen and number
        import re
        return bool(re.match(r'^[A-Z]+-\d+', name))
    
    def _update_phase(self, context: Context, phase: str, note: str):
        """Internal method to update phase"""
        sprint_data = context.plugin_data[self.name]
        
        sprint_data["phase"] = phase
        sprint_data["phase_history"].append({
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "note": note
        })
        
        # Add note to context
        phase_info = self.PHASES[phase]
        context.add_note(f"Sprint phase: {phase_info[0]} {phase_info[1]} - {note}")
    
    def add_test_result(self, context: Context, test_type: str, 
                       result: str, details: str = ""):
        """Add a test result to the sprint"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return "Sprint tracking not initialized"
        
        test_result = {
            "type": test_type,
            "result": result,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        sprint_data.setdefault("test_results", []).append(test_result)
        
        result_emoji = "✅" if result == "pass" else "❌"
        context.add_note(f"Test [{test_type}]: {result} {result_emoji} - {details}")
        
        return f"Test result added: {test_type} - {result}"
    
    def set_pr_info(self, context: Context, pr_number: int, pr_url: str):
        """Set pull request information"""
        sprint_data = context.plugin_data.get(self.name)
        if not sprint_data:
            return "Sprint tracking not initialized"
        
        sprint_data["pr_number"] = pr_number
        sprint_data["pr_url"] = pr_url
        
        context.add_note(f"PR created: #{pr_number} - {pr_url}")
        
        # Auto-update phase to review if in development
        if sprint_data.get("phase") == "development":
            self._update_phase(context, "review", "PR created, moving to review")
        
        return f"PR information updated: #{pr_number}" 