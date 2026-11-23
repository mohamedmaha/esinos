# ESINOS — Development Log

## Phase 0 — Project Foundation

### Work Completed
- Started the ESINOS project
- Selected Python as the programming language
- Selected Ubuntu / WSL as the environment
- Defined a modular architecture

### Problems Encountered

#### Python Virtual Environment

Problem:
The venv creation failed because ensurepip
was unavailable.

Solution:
Install python3.14-venv and recreate
the virtual environment.

### Tests and Validation
Status: In Progress

### Notes
Project documentation and configuration
are currently being prepared.


### Phase 0 — Final Validation

Status: PASSED

#### Environment
- Platform: Ubuntu / WSL
- Python: 3.14.4
- pytest: 9.2.0
- Virtual environment: Active

#### Test Results
- Application startup: PASSED
- Automated tests: 1/1 PASSED
- Git working tree: CLEAN
- GitHub synchronization: SUCCESS

#### Git
- Branch: main
- Initial commit: e6fff03
- Remote: origin/main

#### Conclusion
Phase 0 has been successfully validated.
The project is ready for Phase 1:
Process Management and FCFS Scheduling.


### Phase 1 — Process Model

Status: VALIDATED

#### Implementation
- Created the Process dataclass
- Added process attribute validation
- Implemented immutable process objects

#### Testing
- Process model: 18 tests passed
- Phase 0 smoke test: 1 test passed
- Total: 19/19 passed

#### Conclusion
The Process model is validated and ready
to be used by scheduling algorithms.


### Phase 1 — Scheduling Result Models

Status: VALIDATED

#### Components
- GanttSegment: Validated
- ProcessResult: Validated
- Process: Validated

#### Tests
- Total tests: 37
- Passed: 37
- Failed: 0
- Execution time: 0.32 seconds

#### Conclusion
The scheduling data models are ready.
FCFS algorithm implementation can begin.


### Phase 1 — FCFS Scheduler

Status: AUTOMATED TESTS PASSED

#### Implementation
- Implemented FCFS scheduling algorithm
- Added arrival-time sorting
- Preserved input order for equal arrival times
- Implemented simulated CPU clock
- Added CPU IDLE interval handling
- Generated scheduling results
- Generated Gantt chart segments

#### Testing
- FCFS tests: 9/9 PASSED
- Total project tests: 46/46 PASSED
- Failed tests: 0
- Execution time: 0.27 seconds

#### Next Steps
- Complete technical review
- Implement scheduling summary metrics
- Implement readable Gantt visualization
- Prepare FCFS oral defense


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
