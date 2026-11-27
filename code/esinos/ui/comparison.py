from esinos.scheduling.summary import SchedulingSummary


def render_scheduling_comparison(
    fcfs: SchedulingSummary,
    sjf: SchedulingSummary,
) -> str:
    """Compare FCFS and SJF scheduling summaries."""

    # Step 1: Validate input types
    if not isinstance(fcfs, SchedulingSummary):
        raise TypeError("fcfs must be a SchedulingSummary")

    if not isinstance(sjf, SchedulingSummary):
        raise TypeError("sjf must be a SchedulingSummary")

    # Step 2: Check that both algorithms used
    # exactly the same processes
    def workload(summary):
        return {
            result.pid: (
                result.process.arrival_time,
                result.process.burst_time,
                result.process.priority,
            )
            for result in summary.results
        }

    if workload(fcfs) != workload(sjf):
        raise ValueError(
            "FCFS and SJF must use identical workloads"
        )

    # Step 3: Prepare metric rows
    metrics = [
        (
            "Average WT",
            f"{fcfs.average_waiting_time:.2f}",
            f"{sjf.average_waiting_time:.2f}",
        ),
        (
            "Average TAT",
            f"{fcfs.average_turnaround_time:.2f}",
            f"{sjf.average_turnaround_time:.2f}",
        ),
        (
            "Average RT",
            f"{fcfs.average_response_time:.2f}",
            f"{sjf.average_response_time:.2f}",
        ),
        (
            "CPU Utilization",
            f"{fcfs.cpu_utilization:.2f}%",
            f"{sjf.cpu_utilization:.2f}%",
        ),
        (
            "CPU Busy Time",
            str(fcfs.cpu_busy_time),
            str(sjf.cpu_busy_time),
        ),
        (
            "CPU Idle Time",
            str(fcfs.cpu_idle_time),
            str(sjf.cpu_idle_time),
        ),
        (
            "Makespan",
            str(fcfs.makespan),
            str(sjf.makespan),
        ),
    ]

    # Step 4: Calculate average waiting time improvement
    difference = (
        fcfs.average_waiting_time
        - sjf.average_waiting_time
    )

    if fcfs.average_waiting_time == 0:
        improvement = "N/A"
    else:
        percentage = (
            difference / fcfs.average_waiting_time * 100
        )
        improvement = f"{percentage:.2f}%"

    if difference > 0:
        best = "SJF"
    elif difference < 0:
        best = "FCFS"
    else:
        best = "Tie"

    # Step 5: Build execution orders
    fcfs_order = " -> ".join(
        result.pid for result in fcfs.results
    )

    sjf_order = " -> ".join(
        result.pid for result in sjf.results
    )

    # Step 6: Build the comparison table
    lines = [
        "FCFS VS SJF COMPARISON",
        "=" * 49,
        f"{'METRIC':<25}{'FCFS':>12}{'SJF':>12}",
        "-" * 49,
    ]

    for name, fcfs_value, sjf_value in metrics:
        lines.append(
            f"{name:<25}{fcfs_value:>12}{sjf_value:>12}"
        )

    lines.extend([
        "=" * 49,
        "",
        "EXECUTION ORDER",
        f"FCFS: {fcfs_order}",
        f"SJF : {sjf_order}",
        "",
        "PERFORMANCE ANALYSIS",
        f"Average WT difference (FCFS - SJF): {difference:+.2f}",
        f"Average WT improvement with SJF: {improvement}",
        f"Best average WT: {best}",
    ])

    return "\n".join(lines)
