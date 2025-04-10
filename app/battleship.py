import random
from app.ship import Ship
from app.field_utils import get_surrounding_cells


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships: list[Ship] = []
        self.field: dict[tuple[int, int], Ship] = {}

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("Invalid number of ships: expected 10")

        expected_ship_counts = {1: 4, 2: 3, 3: 2, 4: 1}
        actual_ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            ship_size = ship.get_size()
            if ship_size not in actual_ship_counts:
                raise ValueError(f"Invalid ship size: {ship_size}")
            actual_ship_counts[ship_size] += 1

            for deck in ship.decks:
                for neighbor in get_surrounding_cells(
                    [(deck.row, deck.column)]
                ):
                    if (
                        neighbor in self.field
                        and self.field[neighbor] is not ship
                    ):
                        raise ValueError(
                            "Invalid placement: ships must not touch "
                            "each other"
                        )

        for size, expected_count in expected_ship_counts.items():
            actual_count = actual_ship_counts[size]
            if actual_count != expected_count:
                raise ValueError(
                    f"{expected_count} ship(s) of size {size} required, "
                    f"found {actual_count}"
                )

    def fire(self, target: tuple[int, int]) -> str:
        if target in self.field:
            ship = self.field[target]
            ship.fire(*target)
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def __str__(self) -> str:
        lines = []
        for row_index in range(10):
            line = ""
            for column_index in range(10):
                cell = (row_index, column_index)
                if cell not in self.field:
                    line += "~ "
                else:
                    ship = self.field[cell]
                    deck = ship.get_deck(row_index, column_index)
                    if ship.is_drowned:
                        line += "x "
                    elif deck.is_alive:
                        line += "\u25A1 "
                    else:
                        line += "* "
            lines.append(line.strip())
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Battleship(ships=10, remaining={self.get_remaining_ships()})"

    def get_remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)

    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)


def generate_random_ship_coordinates(
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    ship_sizes = [4] + [3] * 2 + [2] * 3 + [1] * 4
    ship_coordinates: list[tuple[tuple[int, int], tuple[int, int]]] = []
    occupied_cells: set[tuple[int, int]] = set()

    for size in ship_sizes:
        placed = False
        while not placed:
            is_horizontal = random.choice([True, False])

            if is_horizontal:
                row = random.randint(0, 9)
                column = random.randint(0, 10 - size)
                cells = [(row, column + i) for i in range(size)]
            else:
                row = random.randint(0, 10 - size)
                column = random.randint(0, 9)
                cells = [(row + i, column) for i in range(size)]

            surrounding = get_surrounding_cells(cells)
            if all(cell not in occupied_cells for cell in surrounding):
                for cell in cells:
                    occupied_cells.add(cell)
                ship_coordinates.append((cells[0], cells[-1]))
                placed = True

    return ship_coordinates
