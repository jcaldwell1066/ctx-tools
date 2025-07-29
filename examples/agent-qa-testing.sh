#!/bin/bash
# QA Testing Agent Example

echo "=== QA Testing Agent Workflow ==="

# Initialize test context
ctx create PAYMENT-5320-qa-regression
ctx set-status 🧪
ctx add-note "TEST_SUITE: Payment Regression Suite | ENV: staging"
ctx add-note "BUILD: 2025.1.234 | VERSION: 25.10.1"
ctx add-note "SCOPE: Refund endpoints | PRIORITY: P1"

# Test execution
echo -e "\n🧪 Test Execution:"
ctx add-note "TC_001: Create refund - PASS"
ctx add-note "TC_002: Partial refund - PASS"
ctx add-note "TC_003: Duplicate refund prevention - FAIL"
ctx add-note "FAILURE: Expected 409, got 200 | SCREENSHOT: /logs/tc003_fail.png"

# Defect found
echo -e "\n🐛 Defect Tracking:"
ctx set-status 🐛
ctx add-note "DEFECT: BUG-4521 - P2 - RefundService"
ctx add-note "REPRO: 1) Create order 2) Process refund 3) Repeat refund with same ID"
ctx add-note "EXPECTED: 409 Conflict | ACTUAL: 200 OK with duplicate refund"

# Performance testing
echo -e "\n⚡ Performance Results:"
ctx add-note "API_TEST: POST /api/v1/refunds - 201 Created"
ctx add-note "RESPONSE_TIME: 145ms avg (min: 89ms, max: 412ms)"
ctx add-note "LOAD: 100 users, 5 min duration"
ctx add-note "RESULT: CPU = 45% (+15% from baseline)"

# Test summary
echo -e "\n📊 Test Summary:"
ctx add-note "SUMMARY: 85% pass | 2 defects | 1 blocked"
ctx add-note "REGRESSION: Authentication suite - 48/50 passed"
ctx add-note "FLAKY: TC_045 - 30% failure rate over 10 runs"

# Show status
ctx status 