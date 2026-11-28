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


## Phase 2D — SJF Technical Audit

Status: PASSED

### Validation
- 100 reproducible randomized scenarios
- SJF reference timeline comparison
- 50 simultaneous-arrival FCFS/SJF comparisons
- Tie-breaking and multiple IDLE intervals
- Non-preemptive execution
- Large arrival-time values

### Results
- Audit tests: 5/5 PASSED
- Full test suite: 108/108 PASSED
- Execution time: 1.37 seconds

### Next Step
Integrate SJF into the ESINOS main application.


## Phase 2 — SJF Scheduling

Status: FUNCTIONALLY VALIDATED

### Implementation
- Non-preemptive SJF scheduler
- Input validation and ready-process selection
- Deterministic tie-breaking
- CPU IDLE interval handling
- SchedulingSummary compatibility
- SJF report visualization
- FCFS vs SJF comparison
- Interactive CLI integration

### Testing
- Full test suite: 124/124 PASSED
- Failures: 0
- Execution time: 2.88 seconds
- Randomized scheduling audit: PASSED
- CLI integration: PASSED

### Remaining
- Final oral defense
- Git milestone commit

### Next Phase
Phase 3 — Round Robin Scheduling


## Phase 3 — Round Robin Scheduling

### Status
FUNCTIONALLY VALIDATED — Oral defense pending

### Implemented Features
- Preemptive Round Robin scheduling
- Configurable positive integer quantum
- FIFO ready queue using deque
- Stable ordering of simultaneous arrivals
- Arrival handling at quantum boundaries
- Remaining CPU burst tracking
- Multiple Gantt segments per process
- First response and final completion tracking
- CPU idle interval handling
- Compatibility with existing scheduling reports

### User Interface
- Interactive menu option [4]: Round Robin
- Interactive menu option [5]: Three-way comparison
- Command: --demo-rr --quantum N
- Command: --compare-all --quantum N

### Testing
- Complete regression suite: 173 passed
- Failed tests: 0
- Execution time: 5.36 seconds
- Deterministic randomized RR audit
- FCFS equivalence with sufficiently large quantum
- CLI and comparison integration tests

### Simulation Rules
- Nonzero positive integer quantum
- Zero context-switch overhead
- Arrivals at quantum boundaries enter the ready
  queue before the preempted process is requeued
- One ProcessResult per completed process
- One GanttSegment per CPU execution interval

### Next Steps
- Final technical review
- Git milestone
- Round Robin oral defense
- Phase 4: Priority Scheduling


## Phase 4 — Priority Scheduling

### Status
FUNCTIONALLY VALIDATED — Oral defense postponed

### Implementation
- Non-preemptive priority scheduling
- Lower numerical value = higher priority
- Ready-process selection
- Stable tie-breaking rules
- CPU idle interval handling
- SchedulingSummary integration
- Existing Gantt and report compatibility
- Interactive CLI integration
- Direct execution using --demo-priority

### Testing
- Full regression suite: 208 passed
- Failures: 0
- Execution time: 6.46 seconds
- 100 reproducible randomized priority scenarios
- 40 randomized FCFS equivalence scenarios
- Priority CLI integration tests

### CPU Module Status
Implemented algorithms:
1. FCFS
2. SJF (Non-Preemptive)
3. Round Robin (Preemptive)
4. Priority (Non-Preemptive)

Remaining work:
- Custom process input
- Final CPU integration audit
- Oral defenses (postponed)

### Next Module
Memory Management


## CPU Scheduling — Final Functional Milestone

Status: VALIDATED
Regression baseline: 242 tests passed

Implemented:
- FCFS
- SJF (non-preemptive)
- Round Robin (preemptive, configurable quantum)
- Priority Scheduling (non-preemptive)
- Gantt chart rendering
- Waiting, turnaround and response time metrics
- CPU utilization and idle-time metrics
- Interactive process input
- Four-algorithm comparison
- CLI demonstrations and interactive menus

Validation:
- Unit tests
- Randomized reference audits
- Integration tests
- Regression tests

Remaining:
- Final oral defenses (postponed)
- Final project-wide integration review

Next milestone: Memory Management
