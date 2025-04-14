from app.constants import (
    GRID_SIZE,
    EXPECTED_SHIP_COUNTS,
    SYMBOL_ALIVE,
    SYMBOL_SUNK,
    SYMBOL_MISS,
    SYMBOL_AROUND,
    SYMBOL_EMPTY,
    SHOT_HIT,
    SHOT_SUNK,
    SHOT_MISS,
)
from app.field_utils import get_surrounding_cells
from app.ship import Ship
from app.types import Cell, ShipCoordinates


class Battleship:
    def __init__(self, ships: ShipCoordinates) -> None:
        self.ships: list[Ship] = []
        self.field: dict[Cell, Ship] = {}
        self.shots: set[Cell] = set()

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def _validate_field(self) -> None:
        if len(self.ships) != sum(EXPECTED_SHIP_COUNTS.values()):
            raise ValueError("Invalid number of ships")

        actual_counts = {size: 0 for size in EXPECTED_SHIP_COUNTS}

        for ship in self.ships:
            size = ship.get_size()
            if size not in actual_counts:
                raise ValueError(f"Invalid ship size: {size}")
            actual_counts[size] += 1

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

        for size, expected in EXPECTED_SHIP_COUNTS.items():
            actual = actual_counts[size]
            if actual != expected:
                raise ValueError(
                    f"{expected} ship(s) of size {size} required, "
                    f"found {actual}"
                )

    def _is_surrounding_sunk_ship(self, cell: Cell) -> bool:
        for ship in self.ships:
            if ship.is_drowned:
                surrounding = get_surrounding_cells(
                    [(deck.row, deck.column) for deck in ship.decks]
                )
                if cell in surrounding and cell not in self.field:
                    return True
        return False

    def fire(self, target: Cell) -> str:
        self.shots.add(target)

        if target in self.field:
            ship = self.field[target]
            ship.fire(*target)
            return SHOT_SUNK if ship.is_drowned else SHOT_HIT

        return SHOT_MISS

    def get_remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)

    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)

    def __str__(self) -> str:
        # SYMBOL LEGEND:
        #   □ — alive deck         (U+25A1)
        #   ■ — sunk/hit deck      (U+25A0)
        #   • — missed shot        (U+2022)
        #   ✖ — surrounding area   (U+2716)
        #   · — untouched cell     (U+00B7)

        header = "   " + " ".join(str(i) for i in range(1, GRID_SIZE + 1))
        lines = [header]

        for row in range(GRID_SIZE):
            line = f"{row + 1: <2} "
            for col in range(GRID_SIZE):
                cell = (row, col)

                if cell in self.field:
                    ship = self.field[cell]
                    deck = ship.get_deck(cell)
                    if ship.is_drowned or not deck.is_alive:
                        line += f"{SYMBOL_SUNK} "
                    elif cell in self.shots:
                        line += f"{SYMBOL_MISS} "
                    else:
                        line += f"{SYMBOL_ALIVE} "
                else:
                    if self._is_surrounding_sunk_ship(cell):
                        line += f"{SYMBOL_AROUND} "
                    elif cell in self.shots:
                        line += f"{SYMBOL_MISS} "
                    else:
                        line += f"{SYMBOL_EMPTY} "
            lines.append(line.strip())

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Battleship(ships={len(self.ships)}, "
            f"remaining={self.get_remaining_ships()})"
        )
