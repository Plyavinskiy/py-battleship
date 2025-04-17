from itertools import product
import random

from app.constants import EXPECTED_SHIPS_BY_DECK_SIZE, GRID_SIZE
from app.field_utils import get_surrounding_cells
from app.types_aliases import Cell, ShipCoords


def generate_random_ship_coordinates() -> ShipCoords:
    ship_sizes = _expand_ship_counts(EXPECTED_SHIPS_BY_DECK_SIZE)

    ship_coordinates: ShipCoords = []
    occupied_cells: set[Cell] = set()

    for size in ship_sizes:
        ship_cells = _select_valid_ship_coordinates(size, occupied_cells)
        ship_coordinates.append((ship_cells[0], ship_cells[-1]))
        occupied_cells.update(ship_cells)

    return ship_coordinates


def _select_valid_ship_coordinates(
    size: int,
    occupied: set[Cell]
) -> list[Cell]:
    candidate_positions = _get_all_valid_positions(size, occupied)

    if not candidate_positions:
        raise RuntimeError(
            f"Unable to place ship: no available space for size {size}."
        )

    return random.choice(candidate_positions)


def _get_all_valid_positions(
    size: int,
    occupied: set[Cell]
) -> list[list[Cell]]:
    valid_positions: list[list[Cell]] = []

    for row, column in product(range(GRID_SIZE), repeat=2):
        horizontal_cells = [(row, column + i) for i in range(size)]
        if (
            column + size <= GRID_SIZE
            and _is_valid_placement(horizontal_cells, occupied)
        ):
            valid_positions.append(horizontal_cells)

        vertical_cells = [(row + i, column) for i in range(size)]
        if (
            row + size <= GRID_SIZE
            and _is_valid_placement(vertical_cells, occupied)
        ):
            valid_positions.append(vertical_cells)

    return valid_positions


def _is_valid_placement(
    cells: list[Cell],
    occupied: set[Cell]
) -> bool:
    surrounding = get_surrounding_cells(cells)
    return all(cell not in occupied for cell in surrounding)


def _expand_ship_counts(counts: dict[int, int]) -> list[int]:
    return [
        size
        for size, count in counts.items()
        for _ in range(count)
    ]
