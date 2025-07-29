#!/usr/bin/env python3
"""
Demo script showcasing the new ctx functionality
"""

from ctx.core import ContextManager
from ctx.models import ContextState
import time

def demo():
    print("=== CTX Demo ===\n")
    
    # Create manager
    manager = ContextManager()
    
    # Create a feature context
    print("1. Creating feature context...")
    feature_ctx = manager.create(
        "feature-auth",
        description="Implementing authentication system",
        tags=["backend", "security"]
    )
    print(f"✅ Created: {feature_ctx.name}")
    
    # Add some notes
    print("\n2. Adding notes...")
    manager.add_note("feature-auth", "Started implementing JWT tokens")
    time.sleep(0.5)
    manager.add_note("feature-auth", "Added user model and migrations")
    time.sleep(0.5)
    manager.add_note("feature-auth", "Implemented login endpoint", tags=["api"])
    print("✅ Added 3 notes")
    
    # Create a sprint context
    print("\n3. Creating sprint context...")
    sprint_ctx = manager.create(
        "PROJECT-123",
        description="Implement new API endpoint"
    )
    print(f"✅ Created: {sprint_ctx.name}")
    
    # The sprint plugin should auto-initialize
    if "sprint" in sprint_ctx.plugin_data:
        print("✅ Sprint plugin auto-initialized!")
    
    # Update state
    print("\n4. Updating states...")
    manager.set_state("feature-auth", ContextState.IN_PROGRESS)
    manager.set_state("PROJECT-123", ContextState.IN_REVIEW)
    print("✅ States updated")
    
    # List contexts
    print("\n5. Listing all contexts:")
    print("-" * 60)
    print(f"{'NAME':<20} {'STATE':<15} {'NOTES':<10} {'TAGS'}")
    print("-" * 60)
    
    for ctx in manager.list():
        state_display = f"{ctx.emoji} {ctx.state.value}"
        tags = ", ".join(ctx.tags) if ctx.tags else "-"
        active = " ← active" if ctx.name == manager.data.get("active") else ""
        print(f"{ctx.name:<20} {state_display:<15} {ctx.note_count:<10} {tags}{active}")
    
    # Show active context details
    print("\n6. Active context details:")
    active_ctx = manager.get_active()
    if active_ctx:
        print(f"Name: {active_ctx.name}")
        print(f"State: {active_ctx.state.value} {active_ctx.emoji}")
        print(f"Description: {active_ctx.description}")
        print(f"Notes: {active_ctx.note_count}")
        
        # Show sprint info if available
        sprint_data = active_ctx.plugin_data.get("sprint")
        if sprint_data:
            print(f"\nSprint Info:")
            print(f"  Phase: {sprint_data.get('phase')}")
            print(f"  JIRA: {sprint_data.get('jira_url')}")
            print(f"  Branch: {sprint_data.get('branch')}")
    
    # Context switching with stack
    print("\n7. Context switching with stack...")
    print(f"Current: {manager.data.get('active')}")
    manager.push("feature-auth")
    print(f"Pushed and switched to: {manager.data.get('active')}")
    
    ctx = manager.pop()
    if ctx:
        print(f"Popped back to: {ctx.name}")
    
    # Search functionality
    print("\n8. Search demonstration...")
    results = manager.search("auth")
    print(f"Found {len(results)} contexts matching 'auth':")
    for ctx in results:
        print(f"  - {ctx.name}: {ctx.description}")
    
    # Export/Import
    print("\n9. Export context...")
    export_data = manager.export_context("feature-auth")
    print(f"✅ Exported context with {len(export_data['notes'])} notes")
    
    # Show PS1 format
    print("\n10. PS1 Integration:")
    active = manager.get_active()
    if active:
        ps1 = f"{active.name} {active.emoji}"
        print(f"PS1 format: [{ps1}]")
        print(f"Add to bashrc: export PS1='[$(ctx ps1)] \\u@\\h:\\w\\$ '")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo() 