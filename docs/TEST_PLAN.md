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


## Phase 1 — Scheduling Data Models

### TEST-003: Process Model Validation

Component: `code/esinos/scheduling/process.py`

Tests:
- Valid process creation
- Default priority
- Invalid PID validation
- Invalid arrival time
- Invalid burst time
- Invalid priority
- Process immutability

Result: PASSED (18/18 tests)

### TEST-004: GanttSegment Validation

Component: `code/esinos/scheduling/result.py`

Tests:
- Valid Gantt segment
- IDLE segment
- Invalid time intervals
- Invalid PID validation

Result: PASSED (10/10 tests)

### TEST-005: ProcessResult Validation

Component: `code/esinos/scheduling/result.py`

Tests:
- FCFS metrics calculation
- Preemptive scheduling metrics
- Invalid process object
- Invalid execution times
- Result immutability

Result: PASSED (8/8 tests)

## Current Test Summary

Command:
`python -m pytest -v`

Results:
- Phase 0: 1 test passed
- Process Model: 18 tests passed
- GanttSegment: 10 tests passed
- ProcessResult: 8 tests passed

**Total: 37 passed, 0 failed**

Execution time: 0.32 seconds

Overall status: PASSED


### TEST-006: FCFS Scheduler

Component: code/esinos/scheduling/fcfs.py

Validated scenarios:
- Standard FCFS scheduling
- CPU idle intervals
- Equal arrival times
- Unsorted process input
- Single process
- Empty input rejection
- Duplicate PID rejection
- Invalid process rejection
- Input preservation

Result: PASSED (9/9)

Full regression suite: 46/46 PASSED

Status: VALIDATED BY AUTOMATED TESTS


### Phase 1 — Gantt Visualization

Status: AUTOMATED TESTS PASSED

#### Implementation
- Created the terminal Gantt renderer
- Added proportional CPU execution blocks
- Added chronological time markers
- Added IDLE interval visualization
- Kept presentation separate from scheduling logic

#### Testing
- New visualization tests: 5/5 PASSED
- Full regression suite: 61/61 PASSED
- Failed tests: 0
- Execution time: 0.30 seconds

#### Next Step
Implement the process results table.


### TEST-009: Process Results Table

Component: code/esinos/ui/table.py

Validated scenarios:
- Correct process metrics
- IDLE exclusion
- Large values and long identifiers
- Invalid input rejection
- Summary preservation

Result: PASSED (5/5)

Full regression suite: 66/66 PASSED


### TEST-011: FCFS Technical Audit

Component: code/esinos/scheduling/fcfs.py

Audit Coverage:
- 100 reproducible random scheduling scenarios
- FCFS mathematical invariants
- Long CPU idle intervals
- Non-preemptive scheduling behavior
- Input data preservation

Results:
- FCFS audit: 3/3 PASSED
- Full regression suite: 78/78 PASSED
- Failed tests: 0
- Execution time: 1.00 seconds

Status: PASSED


## SJF Technical Audit

Component: code/esinos/scheduling/sjf.py
Test file: tests/test_sjf_audit.py

Result: 5/5 PASSED
Full regression suite: 108/108 PASSED

Status: VALIDATED


## Phase 2 — Final SJF Validation

Components:
- code/esinos/scheduling/sjf.py
- code/esinos/ui/comparison.py
- code/main.py

Validated:
- Scheduling correctness
- Ready queue selection
- Tie-breaking rules
- CPU idle intervals
- Non-preemptive execution
- FCFS/SJF metric comparison
- Command-line execution
- Interactive menu functionality
- Regression testing

Final result: 124/124 PASSED
Status: VALIDATED


## Future Tests

### CPU Scheduling
To be defined in Phases 1-5.

### Memory Management
To be defined in Phases 6-9.

### File System
To be defined in Phase 11.

