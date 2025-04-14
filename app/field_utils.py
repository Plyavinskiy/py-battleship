from app.constants import GRID_SIZE
from app.types import Cell


def get_surrounding_cells(
    deck_positions: list[Cell]
) -> set[Cell]:
    surrounding_cells: set[Cell] = set()

    for row, column in deck_positions:
        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                neighbor_row = row + row_offset
                neighbor_column = column + column_offset

                if (
                    0 <= neighbor_row < GRID_SIZE
                    and 0 <= neighbor_column < GRID_SIZE
                ):
                    surrounding_cells.add((neighbor_row, neighbor_column))

    return surrounding_cells
