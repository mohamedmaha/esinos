from esinos.scheduling.summary import SchedulingSummary


def render_four_way_comparison(
    fcfs: SchedulingSummary,
    sjf: SchedulingSummary,
    rr: SchedulingSummary,
    priority: SchedulingSummary,
    quantum: int,
) -> str:
    """Compare all four CPU scheduling algorithms."""

    summaries = {
        "FCFS": fcfs,
        "SJF": sjf,
        "RR": rr,
        "PRIORITY": priority,
    }

    # Step 1: Validate summaries
    for name, summary in summaries.items():
        if not isinstance(summary, SchedulingSummary):
            raise TypeError(
                f"{name} must be a SchedulingSummary"
            )

    if type(quantum) is not int:
        raise TypeError("quantum must be an integer")

    if quantum <= 0:
        raise ValueError("quantum must be positive")

    # Step 2: Validate identical workloads
    def workload(summary):
        return {
            result.pid: (
                result.process.arrival_time,
                result.process.burst_time,
                result.process.priority,
            )
            for result in summary.results
        }

    expected = workload(fcfs)

    for name, summary in summaries.items():
        if workload(summary) != expected:
            raise ValueError(
                f"{name} has a different workload"
            )

    # Step 3: Build the metric table
    metrics = [
        ("Average WT", "average_waiting_time"),
        ("Average TAT", "average_turnaround_time"),
        ("Average RT", "average_response_time"),
        ("CPU Utilization", "cpu_utilization"),
        ("CPU Busy Time", "cpu_busy_time"),
        ("CPU Idle Time", "cpu_idle_time"),
        ("Makespan", "makespan"),
    ]

    rows = []

    for label, attribute in metrics:
        values = []

        for summary in summaries.values():
            value = getattr(summary, attribute)

            if attribute == "cpu_utilization":
                values.append(f"{value:.2f}%")

            elif attribute.startswith("average_"):
                values.append(f"{value:.2f}")

            else:
                values.append(str(value))

        rows.append((label, *values))

    # Step 4: Find the best average metrics
    def best_algorithms(attribute):
        values = {
            name: getattr(summary, attribute)
            for name, summary in summaries.items()
        }

        best_value = min(values.values())

        winners = [
            name
            for name, value in values.items()
            if value == best_value
        ]

        return " / ".join(winners)

    # Step 5: Format the table
    headers = (
        "METRIC",
        "FCFS",
        "SJF",
        f"RR(q={quantum})",
        "PRIORITY",
    )

    widths = [
        max(
            [len(headers[i])]
            + [len(row[i]) for row in rows]
        )
        for i in range(len(headers))
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

    # Step 6: Show execution orders
    def completion_order(summary):
        return " -> ".join(
            result.pid for result in summary.results
        )

    rr_timeline = " -> ".join(
        f"{segment.label}[{segment.start}-{segment.end}]"
        for segment in rr.gantt
    )

    # Step 7: Assemble the final report
    lines = [
        "ESINOS - FOUR-WAY SCHEDULING COMPARISON",
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
        f"FCFS: {completion_order(fcfs)}",
        f"SJF: {completion_order(sjf)}",
        f"PRIORITY: {completion_order(priority)}",
        f"RR Gantt: {rr_timeline}",
        "",
        "PERFORMANCE ANALYSIS",
        "Best average WT: "
        + best_algorithms("average_waiting_time"),
        "Best average TAT: "
        + best_algorithms("average_turnaround_time"),
        "Best average RT: "
        + best_algorithms("average_response_time"),
    ])

    return "\n".join(lines)
