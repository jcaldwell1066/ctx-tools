"""
Sprint handoff document generator extension
"""

from datetime import datetime
from typing import Optional

from ctx.plugins import Plugin
from ctx.models import Context


class SprintHandoffPlugin(Plugin):
    """Plugin for generating sprint handoff documents"""
    
    name = "sprint_handoff"
    description = "Generate Dev-to-QA handoff documents"
    version = "1.0.0"
    
    def get_commands(self):
        return {
            "handoff": {
                "help": "Generate sprint handoff document",
                "handler": self.generate_handoff
            }
        }
    
    def generate_handoff(self, context: Context) -> str:
        """Generate a comprehensive handoff document"""
        
        sprint_data = context.plugin_data.get("sprint", {})
        
        # Build the document
        doc = f"""# Sprint Context Re-Establishment Form - {context.name}

## Purpose
Provide a concise, actionable overview of the Payment Service sprint for seamless Dev-to-QA handoff.

## Work Items

- **Primary Jira**: {sprint_data.get('jira_url', 'N/A')}
- **Pull Request**: {f"#{sprint_data.get('pr_number')} {sprint_data.get('pr_url', '')}" if sprint_data.get('pr_number') else '[TO BE FILLED]'}
- **Due Date**: [TBD post-build]
- **Remaining Estimate**: [TBD]

## Application Details

- **App Name**: Payment Service 25.10
- **Instance**: {context.metadata.get('instance', '[TO BE FILLED]')}
- **Branch**: {sprint_data.get('branch', f'feature/{context.name}')}
- **Latest Commit**: {context.metadata.get('latest_commit', '[TO BE FILLED]')}

## Technical Context

- **Environment**: {context.metadata.get('environment', '[TO BE FILLED]')}
- **Repository**: {context.metadata.get('repository', '[TO BE FILLED]')}
- **External Tools**: Postman Mock
- **Dependencies**: {context.metadata.get('dependencies', '[TO BE FILLED]')}

## Sprint Progress

### Current Phase: {sprint_data.get('phase', 'unknown')}
"""
        
        # Add phase history
        phase_history = sprint_data.get('phase_history', [])
        if phase_history:
            doc += "\n### Phase History:\n"
            for entry in phase_history:
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
                doc += f"- **{entry['phase']}** ({timestamp}): {entry.get('note', '')}\n"
        
        # Add test results
        test_results = sprint_data.get('test_results', [])
        if test_results:
            doc += "\n## Test Results\n\n"
            passed = sum(1 for t in test_results if t['result'] == 'pass')
            doc += f"**Summary**: {passed}/{len(test_results)} tests passed\n\n"
            
            for test in test_results:
                status = "✅" if test['result'] == 'pass' else "❌"
                doc += f"- {status} **{test['type']}**: {test.get('details', 'No details')}\n"
        
        # Add notes as activity log
        doc += "\n## Activity Log\n\n"
        if context.notes:
            for note in context.notes[-10:]:  # Last 10 notes
                timestamp = note.timestamp.strftime("%Y-%m-%d %H:%M")
                doc += f"- [{timestamp}] {note.text}\n"
        else:
            doc += "No activity recorded yet.\n"
        
        # Add testing methodology template
        doc += """
## Testing Methodology

### Example curl request:
```bash
curl --location 'http://localhost:8080/[endpoint]' \\
  --header 'Authorization: Bearer $TOKEN' \\
  --header 'Accept: application/json' \\
  --header 'Content-Type: application/json' \\
  --data '{
    "merchant_id": "[TO BE FILLED]",
    "tender_reference": "[TO BE FILLED]",
    "terminal_id": "[TO BE FILLED]"
  }'
```

### Expected Responses:
- **Success**: `{"status": "OK", ...}`
- **Failure**: `{"status": "FAILED", ...}`

### SQL Setup:
```sql
-- Add required SQL setup here
UPDATE service_config SET api_endpoint = '[URL]' WHERE service_id = [ID];
```

## Next Steps

- [ ] Review and merge PR
- [ ] Verify instance startup
- [ ] Re-verify test cases
- [ ] Execute test plan
- [ ] Monitor results

## Notes

- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- Context manager: CTX v2.0
"""
        
        # Save to file
        filename = f"{context.name}_handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w') as f:
            f.write(doc)
        
        # Mark handoff as generated
        sprint_data['handoff_generated'] = True
        sprint_data['last_handoff'] = datetime.now().isoformat()
        
        return f"✅ Handoff document generated: {filename}" 