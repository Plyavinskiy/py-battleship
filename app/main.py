import random
from dataclasses import dataclass


@dataclass(slots=True)
class Deck:
    row: int
    column: int
    is_alive: bool = True

    def hit(self) -> None:
        self.is_alive = False

    def __repr__(self) -> str:
        status = "alive" if self.is_alive else "hit"
        return f"Deck({self.row}, {self.column}, {status})"


class Ship:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks: list[Deck] = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for current_column in range(start_column, end_column + 1):
                self.decks.append(Deck(row=start_row, column=current_column))
        elif start_column == end_column:
            for current_row in range(start_row, end_row + 1):
                self.decks.append(Deck(row=current_row, column=start_column))

    def get_size(self) -> int:
        return len(self.decks)

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck:
            deck.hit()
        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True

    def __repr__(self) -> str:
        status = "drowned" if self.is_drowned else "afloat"
        return f"Ship(size={self.get_size()}, {status})"


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
            raise ValueError("Must be exactly 10 ships")

        expected_counts = {1: 4, 2: 3, 3: 2, 4: 1}
        actual_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for ship in self.ships:
            size = ship.get_size()
            if size not in actual_counts:
                raise ValueError(f"Invalid ship size: {size}")
            actual_counts[size] += 1

            for deck in ship.decks:
                for row_offset in (-1, 0, 1):
                    for col_offset in (-1, 0, 1):
                        if row_offset == col_offset == 0:
                            continue
                        neighbor_row = deck.row + row_offset
                        neighbor_column = deck.column + col_offset
                        if (
                            0 <= neighbor_row < 10
                            and 0 <= neighbor_column < 10
                        ):
                            neighbor_ship = self.field.get(
                                (neighbor_row, neighbor_column)
                            )
                            if (
                                neighbor_ship is not None
                                and neighbor_ship is not ship
                            ):
                                raise ValueError("Ships are touching!")

        for size, expected in expected_counts.items():
            actual = actual_counts[size]
            if actual != expected:
                raise ValueError(
                    f"{expected} ship(s) of size {size} required, "
                    f"found {actual}"
                )

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(*location)
            return "Sunk!" if ship.is_drowned else "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        print(self)

    def __str__(self) -> str:
        rows = []
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
            rows.append(line.strip())
        return "\n".join(rows)

    def __repr__(self) -> str:
        remaining = self.get_remaining_ships()
        return f"Battleship(ships=10, remaining={remaining})"

    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)

    def get_remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)


def generate_random_ships() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    ship_sizes = [4] + [3] * 2 + [2] * 3 + [1] * 4
    result: list[tuple[tuple[int, int], tuple[int, int]]] = []
    occupied_cells = set()

    def get_surrounding_cells(
        cells: list[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        surrounding = set()
        for cell_row, cell_column in cells:
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    neighbor_row = cell_row + row_offset
                    neighbor_column = cell_column + column_offset
                    if (
                        0 <= neighbor_row < 10
                        and 0 <= neighbor_column < 10
                    ):
                        surrounding.add((neighbor_row, neighbor_column))
        return surrounding

    for size in ship_sizes:
        placed = False
        while not placed:
            is_horizontal = random.choice([True, False])
            if is_horizontal:
                base_row = random.randint(0, 9)
                base_column = random.randint(0, 10 - size)
                cells = [(base_row, base_column + i) for i in range(size)]
            else:
                base_row = random.randint(0, 10 - size)
                base_column = random.randint(0, 9)
                cells = [(base_row + i, base_column) for i in range(size)]

            if all(
                cell not in occupied_cells
                for cell in get_surrounding_cells(cells)
            ):
                for cell in cells:
                    occupied_cells.add(cell)
                result.append((cells[0], cells[-1]))
                placed = True

    return result


if __name__ == "__main__":
    ships = generate_random_ships()
    game = Battleship(ships=ships)

    print("\nWelcome to Battleship!\n")
    print(game)

    while not game.is_game_over():
        try:
            input_text = input("\nEnter target (row column): ")
            row_part, column_part = input_text.strip().split()
            row = int(row_part)
            column = int(column_part)

            if not (0 <= row < 10 and 0 <= column < 10):
                print("Coordinates must be between 0 and 9.")
                continue

            fire_result = game.fire((row, column))
            print(fire_result)
            print(game)

        except ValueError:
            print("Invalid input. Use format: row column (e.g., 2 3)")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            break

    print("\n🔥 All ships are sunk! Game over!")
