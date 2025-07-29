# QA Test Agent Context Management

## Agent Configuration

```yaml
agent_role: qa_test_engineer
primary_tools:
  - ctx (test execution tracking)
  - mcp_memory_docker (defect patterns)
  - mcp_browser (test automation)
```

## Test Context Initialization

```
Initialize test context:
1. ctx create {JIRA_ID}-qa-{test_type}
2. ctx set-state 🧪
3. Test metadata:
   - ctx note "TEST_SUITE: {suite_name} | ENV: {test_env}"
   - ctx note "BUILD: {build_number} | VERSION: {app_version}"
   - ctx note "SCOPE: {test_scope} | PRIORITY: {P1/P2/P3}"
```

## Test Execution Prompts

### 1. Test Case Execution
```
For each test case:
- ctx note "TC_{id}: {test_name} - {PASS/FAIL/BLOCKED}"
- ctx note "DURATION: {time}ms | DATA: {test_data_set}"
- If failed: ctx note "FAILURE: {reason} | SCREENSHOT: {path}"
- Memory: Create defect pattern entity if new failure type
```

### 2. Regression Testing
```
During regression:
- ctx note "REGRESSION: {suite} - {passed}/{total} passed"
- ctx note "FLAKY: {test_id} - {failure_rate}% over {runs} runs"
- Memory search: "flaky test {test_name}" to check history
- Memory relation: {test_case} -> exhibits -> {flaky_pattern}
```

### 3. Integration Testing
```
API/Integration tests:
- ctx note "API_TEST: {endpoint} - {method} - {status_code}"
- ctx note "RESPONSE_TIME: {avg}ms (min: {min}, max: {max})"
- ctx note "CONTRACT: {validation_status} - {schema_version}"
```

## Defect Tracking

```
When logging defects:
1. ctx set-state 🐛
2. ctx note "DEFECT: {id} - {severity} - {component}"
3. ctx note "REPRO: {steps_to_reproduce}"
4. ctx note "EXPECTED: {expected} | ACTUAL: {actual}"
5. Memory entity: {defect_pattern} (type: defect)
6. Memory relation: {test_case} -> discovered -> {defect_pattern}
```

## Test Status Workflow

```
QA States:
📋 (planning) -> 🧪 (testing) -> 🔍 (investigating) -> 📊 (reporting) -> ✅ (complete)

Issue States:
🐛 (defect found) | 🚫 (blocked) | ⚠️ (warning/flaky)
```

## Test Report Generation

```
Generate test report:
1. ctx notes | grep "TC_" > test_results.tmp
2. Calculate: pass_rate, defect_count, blocked_tests
3. ctx note "SUMMARY: {pass_rate}% pass | {defects} defects | {blocked} blocked"
4. Create: contexts/{JIRA_ID}-test-report.md
```

## Memory Integration for Test Intelligence

```
Intelligent test selection:
1. Memory search: "defects in {component}"
2. Identify high-risk areas from memory
3. ctx note "RISK_BASED: Testing {component} due to {defect_history}"
4. Prioritize test cases based on defect patterns
```

## Performance Testing Context

```
Performance test tracking:
- ctx create {JIRA_ID}-perf-{scenario}
- ctx note "BASELINE: {metric} = {value} {unit}"
- ctx note "LOAD: {users} users, {duration} duration"
- ctx note "RESULT: {metric} = {value} ({percent_change}% from baseline)"
- Memory observation: Performance regression patterns
```

## Automation Handoff

```
For automation candidates:
1. ctx note "AUTOMATE: {test_id} - {priority} - {complexity}"
2. ctx note "SELECTORS: {ui_elements_identified}"
3. ctx note "DATA_DRIVEN: {parameterization_needed}"
4. Export: Test steps and validation points for automation team
```

## Test Environment Issues

```
Environment-related tracking:
- ctx note "ENV_ISSUE: {component} - {issue_type}"
- ctx note "WORKAROUND: {temporary_solution}"
- Memory: Track environment-specific issues for pattern recognition
```
