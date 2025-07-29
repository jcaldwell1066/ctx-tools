# Example Sprint Context

## Status: 🚀 Active Development

## Sprint Overview
- **Primary Task**: PROJECT-123
- **Related Tasks**: PROJECT-124 (dev), PROJECT-125 (testing)
- **Pull Request**: PR #42
- **Branch**: `feature/PROJECT-123`
- **Latest Commit**: `abc123`

## Current Phase: Implementation
- Core functionality implemented
- Unit tests in progress
- Code review pending

## Technical Details
- **Environment**: Development
- **Database**: Local PostgreSQL
- **External Dependencies**: REST APIs, Mock Servers

## Testing Configuration

### Mock Server (Happy Path)
```bash
# Configure service to use mock endpoint
UPDATE service_config 
SET api_endpoint = 'https://mock.example.com/api' 
WHERE service_id = 1;
```

### Live API (Integration Testing)
```bash
# Configure service to use live endpoint
UPDATE service_config 
SET api_endpoint = 'https://api.example.com/v1' 
WHERE service_id = 1;
```

### Test Request
```bash
curl --location 'http://localhost:8080/api/endpoint' \
--header 'Authorization: Bearer token' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "id": "123",
  "action": "process",
  "timestamp": "2024-01-01T00:00:00Z"
}'
```

## Expected Responses
- **Success**: `{"status": "success", "id": "123", "message": "Processed successfully"}`
- **Failure**: `{"status": "error", "code": "INVALID_REQUEST", "message": "Request validation failed"}`

## Acceptance Criteria
- [ ] Core functionality implemented
- [ ] Unit tests passing (80% coverage)
- [ ] Integration tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Performance benchmarks met

## Development Checklist
1. [x] Review requirements
2. [x] Design technical approach
3. [x] Implement core logic
4. [ ] Write unit tests
5. [ ] Integration testing
6. [ ] Code review
7. [ ] Deploy to staging
8. [ ] QA sign-off

## Notes
- API rate limits: 100 requests/minute
- Cache TTL: 5 minutes
- Retry logic: 3 attempts with exponential backoff

## Handoff Information
- **QA Environment**: staging.example.com
- **Test Data**: Available in test fixtures
- **Known Issues**: None
- **Performance**: < 200ms response time