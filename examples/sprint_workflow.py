#!/usr/bin/env python3
"""
Example: Sprint Workflow Management with ctx

This demonstrates how to track a sprint item through its lifecycle
using ctx contexts with status emojis and metadata tracking.
"""

import subprocess
import json
from datetime import datetime

class SprintWorkflow:
    """Helper class for managing sprint workflows with ctx"""
    
    # Sprint phase mappings
    PHASES = {
        "new": "🆕",          # New item created
        "refinement": "📋",   # In refinement/analysis
        "planning": "📅",     # Sprint planning
        "development": "💻",  # Active development
        "review": "👀",       # Code review
        "deployment": "🚀",   # Deployment phase
        "qa_handoff": "🧪",   # QA handoff
        "qa_testing": "🔍",   # QA testing
        "stage": "🎭",        # Stage deployment
        "production": "✅",   # Production deployed
        "blocked": "🚫",      # Blocked
        "on_hold": "⏸️"      # On hold
    }
    
    def __init__(self, sprint_id):
        self.sprint_id = sprint_id
        self.context_name = f"{sprint_id}-sprint"
    
    def run_ctx(self, command):
        """Run a ctx command and return output"""
        result = subprocess.run(
            f"ctx {command}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def create_sprint_context(self, jira_url=None, pr_number=None):
        """Create a new sprint context"""
        self.run_ctx(f"create {self.context_name}")
        
        # Add initial metadata
        notes = [
            f"SPRINT: {self.sprint_id}",
                            f"JIRA: {jira_url or f'https://jira.example.com/browse/{self.sprint_id}'}",
            f"CREATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ]
        
        if pr_number:
            notes.append(f"PR: #{pr_number}")
        
        for note in notes:
            self.run_ctx(f'add-note "{note}"')
        
        # Set initial status
        self.set_phase("new")
    
    def set_phase(self, phase):
        """Update the sprint phase"""
        if phase in self.PHASES:
            emoji = self.PHASES[phase]
            self.run_ctx(f"set-status {emoji}")
            self.run_ctx(f'add-note "PHASE: {phase.upper()} - {datetime.now().strftime('%H:%M')}"')
    
    def add_technical_note(self, category, content):
        """Add a categorized technical note"""
        self.run_ctx(f'add-note "{category.upper()}: {content}"')
    
    def track_pr_status(self, pr_number, status):
        """Track PR status changes"""
        self.add_technical_note("PR", f"#{pr_number} - {status}")
        
        # Update phase based on PR status
        if "merged" in status.lower():
            self.set_phase("deployment")
        elif "review" in status.lower():
            self.set_phase("review")
    
    def track_deployment(self, environment, status):
        """Track deployment status"""
        self.add_technical_note("DEPLOY", f"{environment} - {status}")
    
    def generate_status_report(self):
        """Generate a status report"""
        output = self.run_ctx("status")
        notes_output = self.run_ctx("show-notes")
        
        return f"""
Sprint Status Report: {self.sprint_id}
{'=' * 50}

{output}

Detailed Notes:
{'-' * 50}
{notes_output}
"""

# Example usage
if __name__ == "__main__":
    # Create sprint workflow for PROJECT-123
    sprint = SprintWorkflow("PROJECT-123")
    
    # Initialize sprint
    sprint.create_sprint_context(
        jira_url="https://jira.example.com/browse/PROJECT-123",
        pr_number=1090
    )
    
    # Track development progress
    sprint.set_phase("development")
    sprint.add_technical_note("BRANCH", "feature/PROJECT-123")
    sprint.add_technical_note("COMMIT", "a7a8b84")
    
    # Track testing
    sprint.add_technical_note("TEST", "7 unit tests written")
    sprint.add_technical_note("TEST", "Mockito happy path verified")
    sprint.add_technical_note("TEST", "API failure case verified")
    
    # Move to review
    sprint.set_phase("review")
    sprint.track_pr_status(1090, "In review - comments addressed")
    
    # Move to deployment
    sprint.track_pr_status(1090, "Merged to master")
    sprint.track_deployment("integration", "Build successful")
    sprint.track_deployment("dev-ecs", "Pending restart")
    
    # Add QA handoff notes
    sprint.set_phase("qa_handoff")
    sprint.add_technical_note("QA", "Test tasks PROJECT-200 to PROJECT-203 ready")
    sprint.add_technical_note("QA", "Test methodology documented in sprint context")
    
    # Generate report
    print(sprint.generate_status_report()) 