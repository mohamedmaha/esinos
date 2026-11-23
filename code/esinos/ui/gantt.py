from esinos.scheduling.summary import SchedulingSummary


def render_gantt(
    summary: SchedulingSummary,
    unit_width: int = 4,
) -> str:
    """
    Render a scheduling Gantt chart as plain text.

    Args:
        summary: A validated scheduling summary.
        unit_width: Character width per simulated time unit.

    Returns:
        A formatted multiline string.
    """

    if not isinstance(summary, SchedulingSummary):
        raise TypeError("summary must be a SchedulingSummary")

    if type(unit_width) is not int or not 1 <= unit_width <= 12:
        raise ValueError("unit_width must be between 1 and 12")

    # Build process blocks and timeline boundaries
    blocks = []
    boundaries = [0]
    position = 0

    for segment in summary.gantt:
        label = segment.label

        width = max(
            segment.duration * unit_width,
            len(label) + 2,
            len(str(segment.start)) + 1,
        )

        blocks.append(f"{label:^{width}}")

        position += width + 1
        boundaries.append(position)

    # Build the Gantt bar
    bar = "|" + "|".join(blocks) + "|"

    # Build the time axis
    times = [" "] * len(bar)

    for position, segment in zip(boundaries, summary.gantt):
        timestamp = str(segment.start)

        for offset, character in enumerate(timestamp):
            times[position + offset] = character

    # Add the final completion time
    final_position = boundaries[-1]
    final_time = str(summary.makespan)

    required_length = final_position + len(final_time)

    if required_length > len(times):
        times.extend([" "] * (required_length - len(times)))

    for offset, character in enumerate(final_time):
        times[final_position + offset] = character

    timeline = "".join(times).rstrip()

    return "CPU GANTT\n" + bar + "\n" + timeline
