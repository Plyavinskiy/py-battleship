from typing import TypeAlias

# A board cell represented as (row, column)
Cell: TypeAlias = tuple[int, int]

# A ship as a pair of start and end cells
ShipCoords: TypeAlias = list[tuple[Cell, Cell]]
