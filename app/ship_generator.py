import random

from app.constants import EXPECTED_SHIP_COUNTS, GRID_SIZE
from app.field_utils import get_surrounding_cells
from app.types import Cell, ShipCoordinates


def generate_random_ship_coordinates() -> ShipCoordinates:
    ship_sizes = [
        size
        for size, count in EXPECTED_SHIP_COUNTS.items()
        for _ in range(count)
    ]

    ship_coordinates: ShipCoordinates = []
    occupied_cells: set[Cell] = set()

    for size in ship_sizes:
        is_placed = False
        while not is_placed:
            is_horizontal = random.choice([True, False])

            if is_horizontal:
                row = random.randint(0, GRID_SIZE - 1)
                column = random.randint(0, GRID_SIZE - size)
                cells: list[Cell] = [(row, column + i) for i in range(size)]
            else:
                row = random.randint(0, GRID_SIZE - size)
                column = random.randint(0, GRID_SIZE - 1)
                cells: list[Cell] = [(row + i, column) for i in range(size)]

            surrounding = get_surrounding_cells(cells)
            if all(cell not in occupied_cells for cell in surrounding):
                occupied_cells.update(cells)
                ship_coordinates.append((cells[0], cells[-1]))
                is_placed = True

    return ship_coordinates
