# ESINOS — Project Specification

## 1. Project Overview

ESINOS is an educational operating system simulator
developed in Python.

The project simulates fundamental operating system
mechanisms without modifying the real Linux kernel.

## 2. Official Requirements

### CPU Scheduling
- First Come, First Served (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling
- Gantt charts
- Average waiting and turnaround times

### Memory Management
- Paging
- Logical-to-physical address translation
- FIFO page replacement
- LRU page replacement
- Optimal page replacement
- Translation Lookaside Buffer (TLB)
- Effective Access Time (EAT)

### Optional File System
- Inode-based allocation
- Virtual disk stored in a file
- Create, read, and delete files

### Integration
- Integrated application menu

## 3. Technical Decisions

- Language: Python 3
- Platform: Ubuntu / WSL
- Editor: Visual Studio Code
- Architecture: Modular
- Testing: pytest
- Version control: Git / GitHub
- Development: Individual

## 4. Simulation Conventions

- Single simulated CPU
- Integer time units
- FCFS: Non-preemptive
- SJF: Non-preemptive
- Round Robin: Preemptive
- Priority: Non-preemptive
- Lower priority number = Higher priority
- Context-switching cost: 0 (initial version)

## 5. Project Status

Phase 0 — In Progress
