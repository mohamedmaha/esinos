from esinos.scheduling.summary import SchedulingSummary

from .table import render_process_table
from .gantt import render_gantt


def render_scheduling_report(
    summary: SchedulingSummary,
    algorithm: str,
) -> str:
    """
    Build a complete CPU scheduling report.

    Combines:
    - Process results table
    - CPU Gantt chart
    - Global scheduling statistics
    """

    # Step 1: Validate inputs
    if not isinstance(summary, SchedulingSummary):
        raise TypeError(
            "summary must be a SchedulingSummary"
        )

    if not isinstance(algorithm, str) or not algorithm.strip():
        raise ValueError(
            "algorithm must be a non-empty string"
        )

    # Step 2: Build the report header
    title = (
        f"ESINOS | CPU SCHEDULING | "
        f"{algorithm.strip().upper()}"
    )

    # Step 3: Build the statistics section
    statistics = [
        "SCHEDULING SUMMARY",
        "-" * 50,
        f"Process Count: {summary.process_count}",
        f"Average Waiting Time: {summary.average_waiting_time:.2f}",
        f"Average Turnaround Time: {summary.average_turnaround_time:.2f}",
        f"Average Response Time: {summary.average_response_time:.2f}",
        f"CPU Busy Time: {summary.cpu_busy_time}",
        f"CPU Idle Time: {summary.cpu_idle_time}",
        f"Makespan: {summary.makespan}",
        f"CPU Utilization: {summary.cpu_utilization:.2f}%",
    ]

    # Step 4: Assemble all report sections
    sections = [
        title,
        "=" * 50,
        "",
        render_process_table(summary),
        "",
        render_gantt(summary),
        "",
        "\n".join(statistics),
    ]

    return "\n".join(sections)
