from app.constants import GRID_SIZE


def parse_coordinates(user_input: str) -> tuple[int, int] | None:
    parts = user_input.strip().split()
    all_parts_are_digits = all(part.isdigit() for part in parts)

    if len(parts) != 2 or not all_parts_are_digits:
        return None

    row = int(parts[0]) - 1
    column = int(parts[1]) - 1
    return row, column


def is_within_bounds(row: int, column: int) -> bool:
    return 0 <= row < GRID_SIZE and 0 <= column < GRID_SIZE


def prompt_for_coordinates() -> tuple[int, int] | None:
    user_input = input(
        f"\nEnter target (row column, from 1 to {GRID_SIZE}): "
    )
    return parse_coordinates(user_input)
