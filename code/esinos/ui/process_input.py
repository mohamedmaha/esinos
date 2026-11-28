from collections.abc import Callable

from esinos.scheduling.process import Process


MAX_CUSTOM_PROCESSES = 20


def _read_integer(
    prompt: str,
    *,
    minimum: int,
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    maximum: int | None = None,
    default: int | None = None,
) -> int:
    """Read and validate an integer interactively."""

    while True:
        raw = input_fn(prompt).strip()

        # An empty answer can select a default value.
        if raw == "" and default is not None:
            value = default
        else:
            try:
                value = int(raw)
            except ValueError:
                output_fn(
                    "Invalid value. Enter an integer."
                )
                continue

        if value < minimum:
            output_fn(
                f"Value must be >= {minimum}."
            )
            continue

        if maximum is not None and value > maximum:
            output_fn(
                f"Value must be <= {maximum}."
            )
            continue

        return value


def read_processes(
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> list[Process]:
    """Interactively create validated Process objects."""

    output_fn("ESINOS - CUSTOM PROCESS INPUT")

    # Step 1: Read the number of processes
    count = _read_integer(
        f"Number of processes (1-{MAX_CUSTOM_PROCESSES}): ",
        minimum=1,
        maximum=MAX_CUSTOM_PROCESSES,
        input_fn=input_fn,
        output_fn=output_fn,
    )

    processes: list[Process] = []

    # Step 2: Read every process
    for index in range(1, count + 1):
        pid = f"P{index}"

        output_fn(f"\n--- {pid} ---")

        arrival_time = _read_integer(
            "Arrival time: ",
            minimum=0,
            input_fn=input_fn,
            output_fn=output_fn,
        )

        burst_time = _read_integer(
            "Burst time: ",
            minimum=1,
            input_fn=input_fn,
            output_fn=output_fn,
        )

        priority = _read_integer(
            "Priority [default 1]: ",
            minimum=1,
            default=1,
            input_fn=input_fn,
            output_fn=output_fn,
        )

        process = Process(
            pid=pid,
            arrival_time=arrival_time,
            burst_time=burst_time,
            priority=priority,
        )

        processes.append(process)

    output_fn(
        f"\n{len(processes)} processes created successfully."
    )

    return processes
