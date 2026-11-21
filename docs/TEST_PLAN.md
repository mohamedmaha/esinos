# ESINOS — Test Plan

## Testing Strategy

Each module must pass:
- Normal operation tests
- Edge case tests
- Result correctness tests
- Regression tests

## Phase 0 — Environment Tests

### TEST-001: Application Startup

Objective:
Verify that ESINOS starts successfully.

Command:
python code/main.py

Expected Result:
- Exit code 0
- ESINOS title displayed
- No execution errors

Status: PASSED

### TEST-002: Automated Testing

Objective:
Verify that pytest works correctly.

Command:
python -m pytest -v

Expected Result:
- Tests are discovered
- Smoke test passes
- No test failures

Status: PASSED
Result: 1/1 tests passed

## Future Tests

### CPU Scheduling
To be defined in Phases 1-5.

### Memory Management
To be defined in Phases 6-9.

### File System
To be defined in Phase 11.
