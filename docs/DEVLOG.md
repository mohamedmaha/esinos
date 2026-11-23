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


### Phase 1 — Process Results Table

Status: VALIDATED

#### Implementation
- Created the process results table renderer
- Added dynamic column widths
- Added aligned process metrics
- Kept the presentation layer separate from the scheduler

#### Tests
- New table tests: 5/5 PASSED
- Full test suite: 66/66 PASSED
- Execution time: 0.31 seconds

#### Next Step
Integrate the results table, Gantt chart,
and scheduling statistics into one report.


### Phase 1 — FCFS Technical Audit

Status: PASSED

#### Verification
- Completed 100 reproducible scheduling scenarios
- Verified process execution order
- Verified scheduling time calculations
- Verified CPU busy and idle time consistency
- Confirmed non-preemptive behavior

#### Results
- 78/78 automated tests passed
- No failures detected

#### Remaining Tasks
- Complete the FCFS oral defense
- Finalize Phase 1 documentation
- Commit and push the validated version


## Phase 1 — Final Validation

Status: COMPLETED

### Implementation
- Process model
- GanttSegment and ProcessResult
- FCFS scheduling algorithm
- SchedulingSummary
- Gantt visualization
- Process results table
- Integrated scheduling report
- Main application CLI

### Quality Assurance
- Automated tests: 78/78 PASSED
- Reproducible FCFS audit: PASSED
- Integration tests: PASSED

### Oral Defense
- Score: 17/20 (practice assessment)
- Strong understanding of FCFS and architecture
- Improvement area: detailed scheduling calculations

### Conclusion
FCFS development and validation completed.
Ready to begin Phase 2 — SJF Scheduling.
