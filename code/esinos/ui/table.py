from esinos.scheduling.summary import SchedulingSummary


def render_process_table(summary: SchedulingSummary) -> str:
    """
    Render a table of individual scheduling results.

    The first column is left-aligned.
    Numeric columns are right-aligned.
    """

    if not isinstance(summary, SchedulingSummary):
        raise TypeError("summary must be a SchedulingSummary")

    # Step 1: Define table headers
    headers = (
        "PID", "AT", "BT", "ST",
        "CT", "WT", "TAT", "RT",
    )

    # Step 2: Extract process results
    rows = []

    for result in summary.results:
        rows.append((
            result.pid,
            str(result.process.arrival_time),
            str(result.process.burst_time),
            str(result.start_time),
            str(result.completion_time),
            str(result.waiting_time),
            str(result.turnaround_time),
            str(result.response_time),
        ))

    # Step 3: Calculate column widths
    widths = [
        max(
            len(header),
            max(len(row[i]) for row in rows),
        )
        for i, header in enumerate(headers)
    ]

    # Step 4: Build horizontal separators
    separator = "+" + "+".join(
        "-" * (width + 2)
        for width in widths
    ) + "+"

    # Step 5: Format a table row
    def format_row(values):
        cells = []

        for i, value in enumerate(values):
            if i == 0:
                cells.append(value.ljust(widths[i]))
            else:
                cells.append(value.rjust(widths[i]))

        return "| " + " | ".join(cells) + " |"

    # Step 6: Assemble the table
    lines = [
        "PROCESS RESULTS",
        separator,
        format_row(headers),
        separator,
    ]

    for row in rows:
        lines.append(format_row(row))

    lines.append(separator)

    return "\n".join(lines)
