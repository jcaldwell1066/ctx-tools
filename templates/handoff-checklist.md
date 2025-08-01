# Team Handoff Checklist Template

## Development → QA Handoff

### Pre-Handoff Requirements ✅
- [ ] **Code Review**: All PR comments addressed
- [ ] **Tests**: Unit test coverage ≥95%
- [ ] **Integration**: Payment gateway validation complete
- [ ] **Documentation**: Technical changes documented
- [ ] **Branch**: Feature branch up-to-date with main

### Handoff Information Package 📦
```
CONTEXT: [context-name]
JIRA: [ticket-id]
BRANCH: [branch-name]
PR: [pr-number]
REVIEWERS: [@reviewer1, @reviewer2]
```

### Test Guidance for QA 🧪
- [ ] **Functional Tests**: [List specific scenarios]
- [ ] **Regression Tests**: [Critical payment flows to verify]
- [ ] **Performance Tests**: [SLA requirements]
- [ ] **Edge Cases**: [Known edge cases to test]

### Context Commands for QA Team
```bash
# Switch to work context
ctx switch [context-name]

# Review development notes
ctx notes | grep -E "(IMPL:|TEST:|HANDOFF:)"

# Add QA findings
ctx note "QA: [finding description]"

# Update state when testing complete
ctx set-state in-review  # or completed
```

---

## QA → DevOps Handoff

### QA Validation Complete ✅
- [ ] **Functional**: All payment flows working
- [ ] **Regression**: No disruption to existing features
- [ ] **Performance**: Transaction times within SLA
- [ ] **Security**: Payment data handling validated

### Deployment Package 🚀
```
STAGING_VALIDATED: [timestamp]
ROLLBACK_PLAN: [documented procedure]
MONITORING: [alerts configured]
DEPLOYMENT_WINDOW: [scheduled time]
```

### Post-Deployment Monitoring 📊
- [ ] **Payment Success Rate**: Maintain >99.5%
- [ ] **Response Times**: <500ms average
- [ ] **Error Rates**: <0.1% 4xx/5xx errors
- [ ] **Gateway Health**: All integrations stable

---

## Emergency Handoff Protocol 🚨

### For Critical Issues
1. **Immediate**: Set context state to `blocked` 🚫
2. **Escalate**: Add note with `URGENT:` prefix
3. **Notify**: Include stakeholder tags
4. **Document**: Clear problem description and impact

```bash
ctx set-state blocked
ctx note "URGENT: [critical issue description]"
ctx note "IMPACT: [business/technical impact]"
ctx note "STAKEHOLDERS: [@oncall, @team-lead, @product]"
```