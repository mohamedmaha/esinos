from esinos.scheduling.summary import SchedulingSummary


def render_three_way_comparison(
    fcfs: SchedulingSummary,
    sjf: SchedulingSummary,
    rr: SchedulingSummary,
    quantum: int,
) -> str:
    """Compare FCFS, SJF and Round Robin on one workload."""

    summaries = {
        "FCFS": fcfs,
        "SJF": sjf,
        "RR": rr,
    }

    # Step 1: Validate input types
    for name, summary in summaries.items():
        if not isinstance(summary, SchedulingSummary):
            raise TypeError(
                f"{name} must be a SchedulingSummary"
            )

    if type(quantum) is not int:
        raise TypeError("quantum must be an integer")

    if quantum <= 0:
        raise ValueError("quantum must be positive")

    # Step 2: Ensure identical workloads
    def workload(summary):
        return {
            result.pid: (
                result.process.arrival_time,
                result.process.burst_time,
                result.process.priority,
            )
            for result in summary.results
        }

    expected_workload = workload(fcfs)

    if (
        workload(sjf) != expected_workload
        or workload(rr) != expected_workload
    ):
        raise ValueError(
            "All algorithms must use identical workloads"
        )

    # Step 3: Prepare comparative statistics
    rows = [
        (
            "Average WT",
            f"{fcfs.average_waiting_time:.2f}",
            f"{sjf.average_waiting_time:.2f}",
            f"{rr.average_waiting_time:.2f}",
        ),
        (
            "Average TAT",
            f"{fcfs.average_turnaround_time:.2f}",
            f"{sjf.average_turnaround_time:.2f}",
            f"{rr.average_turnaround_time:.2f}",
        ),
        (
            "Average RT",
            f"{fcfs.average_response_time:.2f}",
            f"{sjf.average_response_time:.2f}",
            f"{rr.average_response_time:.2f}",
        ),
        (
            "CPU Utilization",
            f"{fcfs.cpu_utilization:.2f}%",
            f"{sjf.cpu_utilization:.2f}%",
            f"{rr.cpu_utilization:.2f}%",
        ),
        (
            "CPU Busy Time",
            str(fcfs.cpu_busy_time),
            str(sjf.cpu_busy_time),
            str(rr.cpu_busy_time),
        ),
        (
            "CPU Idle Time",
            str(fcfs.cpu_idle_time),
            str(sjf.cpu_idle_time),
            str(rr.cpu_idle_time),
        ),
        (
            "Makespan",
            str(fcfs.makespan),
            str(sjf.makespan),
            str(rr.makespan),
        ),
    ]

    # Step 4: Calculate dynamic column widths
    headers = ("METRIC", "FCFS", "SJF", f"RR(q={quantum})")

    widths = [
        max(
            [len(headers[i])]
            + [len(row[i]) for row in rows]
        )
        for i in range(4)
    ]

    def format_row(values):
        cells = []

        for i, value in enumerate(values):
            if i == 0:
                cells.append(value.ljust(widths[i]))
            else:
                cells.append(value.rjust(widths[i]))

        return " | ".join(cells)

    separator = "-+-".join(
        "-" * width for width in widths
    )

    # Step 5: Determine best average metrics
    def best_algorithms(metric_name):
        values = {
            name: getattr(summary, metric_name)
            for name, summary in summaries.items()
        }

        minimum = min(values.values())

        winners = [
            name
            for name, value in values.items()
            if value == minimum
        ]

        return " / ".join(winners)

    # Step 6: Build execution orders
    fcfs_order = " -> ".join(
        result.pid for result in fcfs.results
    )

    sjf_order = " -> ".join(
        result.pid for result in sjf.results
    )

    # RR has multiple CPU segments for some processes
    rr_timeline = " -> ".join(
        f"{segment.label}[{segment.start}-{segment.end}]"
        for segment in rr.gantt
    )

    # Step 7: Assemble final report
    lines = [
        "FCFS VS SJF VS ROUND ROBIN",
        "=" * len(separator),
        format_row(headers),
        separator,
    ]

    for row in rows:
        lines.append(format_row(row))

    lines.extend([
        "=" * len(separator),
        "",
        "EXECUTION ORDER",
        f"FCFS: {fcfs_order}",
        f"SJF : {sjf_order}",
        f"RR Gantt: {rr_timeline}",
        "",
        "PERFORMANCE ANALYSIS",
        "Best average WT: "
        + best_algorithms("average_waiting_time"),
        "Best average RT: "
        + best_algorithms("average_response_time"),
    ])

    return "\n".join(lines)
