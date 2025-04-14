from typing import TypeAlias


# A single cell position on the game grid: (row, column)
Cell: TypeAlias = tuple[int, int]

# A list of ship coordinates: each ship is (start_cell, end_cell)
ShipCoordinates: TypeAlias = list[tuple[Cell, Cell]]
