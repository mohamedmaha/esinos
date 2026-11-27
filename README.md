
## CPU Scheduling

ESINOS currently implements:

- FCFS (First Come, First Served)
- SJF (Shortest Job First, non-preemptive)
- RR (Round Robin, preemptive)

### Run the application

```bash
python code/main.py
```

### Direct demonstrations

```bash
python code/main.py --demo-fcfs
python code/main.py --demo-sjf
python code/main.py --demo-rr --quantum 3
```

### Compare algorithms

```bash
python code/main.py --compare-fcfs-sjf
python code/main.py --compare-all --quantum 2
```

### Run automated tests

```bash
python -m pytest -v
```

Round Robin uses a FIFO ready queue and a configurable
time quantum. Context-switch overhead is assumed to be zero.
