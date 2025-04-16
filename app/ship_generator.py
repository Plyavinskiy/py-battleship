import random

from app.constants import EXPECTED_SHIPS_BY_DECK_SIZE, GRID_SIZE
from app.field_utils import get_surrounding_cells
from app.types import Cell, ShipCoordinates


def generate_random_ship_coordinates() -> ShipCoordinates:
    ship_sizes = _expand_ship_counts(EXPECTED_SHIPS_BY_DECK_SIZE)

    ship_coordinates: ShipCoordinates = []
    occupied_cells: set[Cell] = set()

    for size in ship_sizes:
        ship = _place_ship(size, occupied_cells)
        ship_coordinates.append((ship[0], ship[-1]))
        occupied_cells.update(ship)

    return ship_coordinates


def _place_ship(size: int, occupied: set[Cell]) -> list[Cell]:
    while True:
        is_horizontal = random.choice([True, False])

        if is_horizontal:
            row = random.randint(0, GRID_SIZE - 1)
            column = random.randint(0, GRID_SIZE - size)
            cells = [(row, column + i) for i in range(size)]
        else:
            row = random.randint(0, GRID_SIZE - size)
            column = random.randint(0, GRID_SIZE - 1)
            cells = [(row + i, column) for i in range(size)]

        if all(cell not in occupied for cell in get_surrounding_cells(cells)):
            return cells


def _expand_ship_counts(counts: dict[int, int]) -> list[int]:
    return [
        size for size, count in counts.items()
        for _ in range(count)
    ]
