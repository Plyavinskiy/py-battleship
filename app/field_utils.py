def get_surrounding_cells(
    deck_positions: list[tuple[int, int]]
) -> set[tuple[int, int]]:
    surrounding_cells = set()

    for row, column in deck_positions:
        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                neighbor_row = row + row_offset
                neighbor_column = column + column_offset

                if (
                    0 <= neighbor_row < 10
                    and 0 <= neighbor_column < 10
                ):
                    surrounding_cells.add((neighbor_row, neighbor_column))

    return surrounding_cells
