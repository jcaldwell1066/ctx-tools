#!/bin/bash
# Backend Developer Agent Example

echo "=== Backend Developer Agent Workflow ==="

# Initialize context for new service
ctx create PAYMENT-5320-refund-service
ctx set-status 💻
ctx add-note "SERVICE: RefundService | ENDPOINT: /api/v1/refunds"
ctx add-note "BRANCH: feature/PAYMENT-5320 | TARGET: dev-env"
ctx add-note "DEPENDENCIES: PaymentGateway, UserService, NotificationService"

# Simulate development progress
echo -e "\n📝 Development Progress:"
ctx add-note "IMPL: Database schema - COMPLETE"
ctx add-note "IMPL: Service layer - IN_PROGRESS"
ctx add-note "DECISION: Using event-driven architecture for async processing"

# Error encountered
ctx add-note "ERROR: Connection timeout to PaymentGateway - ConnectionPool exhausted"
ctx add-note "FIX: Increased pool size from 10 to 50 - commit: abc123"

# Test development
echo -e "\n🧪 Test Development:"
ctx add-note "TEST: refund.service.test.js - 95% coverage - 18 tests"
ctx add-note "MOCK: PaymentGateway - Using WireMock for integration tests"

# Integration documentation
ctx add-note "INTEGRATION: PaymentGateway - REST - OAuth2"
ctx add-note "CONFIG: PAYMENT_GATEWAY_URL = https://api.payment.com/v2"
ctx add-note "CONFIG: PAYMENT_GATEWAY_TIMEOUT = 30s"

# Ready for review
echo -e "\n👀 Code Review:"
ctx set-status 👀
ctx add-note "PR: #1091 - https://github.com/org/repo/pull/1091"
ctx add-note "CHANGES: 12 files, +847/-123"

# Show current status
echo -e "\n📊 Current Context Status:"
ctx status 