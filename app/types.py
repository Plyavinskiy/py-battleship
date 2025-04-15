from typing import TypeAlias

# Represents a position on the game grid (row, column)
Cell: TypeAlias = tuple[int, int]

# List of ship coordinates:
# each ship is represented as (start_cell, end_cell)
ShipCoordinates: TypeAlias = list[tuple[Cell, Cell]]
