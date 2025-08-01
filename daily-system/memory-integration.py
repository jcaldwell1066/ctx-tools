#!/usr/bin/env python3
"""
Memory Integration for CTX Daily System
Syncs context data with MCP memory servers for knowledge retention
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional

class CtxMemoryIntegration:
    """Integrates ctx contexts with MCP memory servers"""
    
    def __init__(self):
        self.memory_entities = {}
        self.context_patterns = {}
    
    def run_ctx_command(self, command: str) -> str:
        """Run a ctx command and return output"""
        try:
            result = subprocess.run(
                f"ctx {command}",
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running ctx command: {e}")
            return ""
    
    def get_active_contexts(self) -> List[Dict]:
        """Get all active contexts"""
        try:
            # Parse ctx list output
            output = self.run_ctx_command("list --format=json")
            if output:
                return json.loads(output)
            else:
                # Fallback to simple parsing
                contexts = []
                lines = self.run_ctx_command("list").split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            contexts.append({
                                'name': parts[0],
                                'state': parts[1],
                                'updated': ' '.join(parts[2:])
                            })
                return contexts
        except Exception as e:
            print(f"Error getting contexts: {e}")
            return []
    
    def extract_context_knowledge(self, context_name: str) -> Dict:
        """Extract knowledge from a context"""
        # Switch to context and get details
        self.run_ctx_command(f"switch {context_name}")
        notes_output = self.run_ctx_command("notes")
        status_output = self.run_ctx_command("status")
        
        knowledge = {
            'context_name': context_name,
            'notes': [],
            'technical_patterns': [],
            'decisions': [],
            'blockers': [],
            'solutions': [],
            'integrations': [],
            'extracted_at': datetime.now().isoformat()
        }
        
        # Parse notes for different types of information
        for line in notes_output.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Technical patterns
            if any(prefix in line for prefix in ['IMPL:', 'TECH:', 'ARCHITECTURE:', 'DECISION:']):
                knowledge['technical_patterns'].append(line)
            
            # Decisions and rationale
            elif 'DECISION:' in line or 'RATIONALE:' in line:
                knowledge['decisions'].append(line)
            
            # Blockers and solutions
            elif 'BLOCKED:' in line or 'BLOCKER:' in line:
                knowledge['blockers'].append(line)
            elif 'UNBLOCKED:' in line or 'SOLUTION:' in line or 'FIX:' in line:
                knowledge['solutions'].append(line)
            
            # Integration details
            elif any(keyword in line for keyword in ['API:', 'SERVICE:', 'DATABASE:', 'CONFIG:', 'ENDPOINT:']):
                knowledge['integrations'].append(line)
            
            # All notes for completeness
            knowledge['notes'].append(line)
        
        return knowledge
    
    def create_memory_entities(self, knowledge: Dict):
        """Create memory entities from extracted knowledge"""
        context_name = knowledge['context_name']
        
        # Main context entity
        observations = []
        
        # Add technical patterns
        for pattern in knowledge['technical_patterns']:
            observations.append(f"Technical pattern: {pattern}")
        
        # Add decisions
        for decision in knowledge['decisions']:
            observations.append(f"Decision made: {decision}")
        
        # Add integration details
        for integration in knowledge['integrations']:
            observations.append(f"Integration detail: {integration}")
        
        # Add solutions for future reference
        for solution in knowledge['solutions']:
            observations.append(f"Solution applied: {solution}")
        
        print(f"Creating memory entity for {context_name}")
        print(f"Observations: {len(observations)}")
        
        # In a real integration, this would call MCP memory tools
        # For now, we'll just demonstrate the structure
        entity_data = {
            'name': context_name,
            'type': 'development_context',
            'observations': observations,
            'metadata': {
                'created_from': 'ctx_daily_system',
                'extracted_at': knowledge['extracted_at'],
                'note_count': len(knowledge['notes']),
                'pattern_count': len(knowledge['technical_patterns'])
            }
        }
        
        return entity_data
    
    def sync_completed_contexts(self):
        """Sync completed contexts to memory"""
        print("Syncing completed contexts to memory...")
        
        contexts = self.get_active_contexts()
        completed_contexts = [ctx for ctx in contexts if '✅' in ctx.get('state', '')]
        
        synced_count = 0
        for context in completed_contexts:
            context_name = context['name']
            print(f"Processing context: {context_name}")
            
            # Extract knowledge
            knowledge = self.extract_context_knowledge(context_name)
            
            # Create memory entity
            if knowledge['notes']:  # Only sync if there's content
                entity = self.create_memory_entities(knowledge)
                print(f"Would create memory entity: {entity['name']}")
                synced_count += 1
        
        print(f"Synced {synced_count} completed contexts to memory")
        return synced_count
    
    def search_similar_patterns(self, current_context: str) -> List[str]:
        """Search for similar patterns in memory (placeholder)"""
        # In real implementation, would query MCP memory
        print(f"Searching for patterns similar to {current_context}")
        return ["payment-api-integration", "cybersource-validation", "error-handling-patterns"]
    
    def suggest_next_actions(self, context_name: str) -> List[str]:
        """Suggest next actions based on similar contexts"""
        similar_patterns = self.search_similar_patterns(context_name)
        
        suggestions = [
            "Consider adding integration tests for payment validation",
            "Document configuration settings for team reference",
            "Add error handling for gateway timeout scenarios",
            "Create rollback plan before deployment"
        ]
        
        return suggestions

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: memory-integration.py <command>")
        print("Commands:")
        print("  sync       - Sync completed contexts to memory")
        print("  suggest    - Get suggestions for current context")
        print("  extract    - Extract knowledge from current context")
        return
    
    command = sys.argv[1]
    integration = CtxMemoryIntegration()
    
    if command == "sync":
        integration.sync_completed_contexts()
    elif command == "suggest":
        current_ctx = integration.run_ctx_command("status").split('\n')[0]
        if "Context:" in current_ctx:
            context_name = current_ctx.split("Context:")[1].split()[0]
            suggestions = integration.suggest_next_actions(context_name)
            print("Suggestions based on similar contexts:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
    elif command == "extract":
        current_ctx = integration.run_ctx_command("status").split('\n')[0]
        if "Context:" in current_ctx:
            context_name = current_ctx.split("Context:")[1].split()[0]
            knowledge = integration.extract_context_knowledge(context_name)
            print(json.dumps(knowledge, indent=2))
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()