from app.constants import GRID_SIZE
from app.types import Cell


def get_surrounding_cells(positions: list[Cell]) -> set[Cell]:
    surrounding: set[Cell] = set()

    for row, column in positions:
        for delta_row in (-1, 0, 1):
            for delta_column in (-1, 0, 1):
                neighbor_row = row + delta_row
                neighbor_column = column + delta_column

                if (
                    0 <= neighbor_row < GRID_SIZE
                    and 0 <= neighbor_column < GRID_SIZE
                ):
                    surrounding.add((neighbor_row, neighbor_column))

    return surrounding
