from app.constants import DEBUG_COORDS, GRID_SIZE


def parse_coordinates(user_input: str) -> tuple[int, int] | None:
    parts = user_input.strip().split()
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        return None

    row = int(parts[0])
    column = int(parts[1])

    if not DEBUG_COORDS:
        row -= 1
        column -= 1

    return row, column


def is_within_bounds(row: int, column: int) -> bool:
    return 0 <= row < GRID_SIZE and 0 <= column < GRID_SIZE


def prompt_for_coordinates() -> tuple[int, int] | None:
    start_label = "0" if DEBUG_COORDS else "1"
    prompt = (
        "\nEnter target (row column, "
        f"{start_label} to {GRID_SIZE}): "
    )
    user_input = input(prompt)
    return parse_coordinates(user_input)
