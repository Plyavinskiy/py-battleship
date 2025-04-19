from app.constants import (
    DEBUG_COORDS,
    EXPECTED_SHIPS_BY_DECK_SIZE,
    GRID_SIZE,
    SHOT_HIT,
    SHOT_MISS,
    SHOT_REPEAT,
    SHOT_SUNK,
    SYMBOL_ALIVE,
    SYMBOL_AROUND,
    SYMBOL_EMPTY,
    SYMBOL_MISS,
    SYMBOL_SUNK,
)
from app.field_utils import get_surrounding_cells
from app.ship import Ship
from app.types_aliases import Cell, ShipCoords


class Battleship:
    def __init__(self, ships: ShipCoords) -> None:
        self.ships: list[Ship] = []
        self.field: dict[Cell, Ship] = {}
        self.shots: set[Cell] = set()

        for start, end in ships:
            ship = Ship(start, end)
            self.ships.append(ship)
            for deck in ship.decks:
                self.field[deck.position] = ship

        self._validate_field()

    @property
    def remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not ship.is_drowned)

    @property
    def is_game_over(self) -> bool:
        return all(ship.is_drowned for ship in self.ships)

    def fire(self, target: Cell) -> str:
        if target in self.shots:
            return SHOT_REPEAT

        self.shots.add(target)

        if target in self.field:
            ship = self.field[target]
            ship.hit(target)
            return SHOT_SUNK if ship.is_drowned else SHOT_HIT

        return SHOT_MISS

    def __str__(self) -> str:
        header_range = (
            range(GRID_SIZE)
            if DEBUG_COORDS
            else range(1, GRID_SIZE + 1)
        )
        header = "   " + " ".join(str(i) for i in header_range)
        lines = [header]

        for row in range(GRID_SIZE):
            prefix = f"{row: <2} " if DEBUG_COORDS else f"{row + 1: <2} "
            line = prefix

            for column in range(GRID_SIZE):
                position = (row, column)

                if position in self.field:
                    ship = self.field[position]
                    deck = ship.get_deck(position)

                    if ship.is_drowned or not deck.is_alive:
                        line += f"{SYMBOL_SUNK} "
                    else:
                        line += f"{SYMBOL_ALIVE} "
                else:
                    if self._should_mark_sunk_area(position):
                        line += f"{SYMBOL_AROUND} "
                    elif position in self.shots:
                        line += f"{SYMBOL_MISS} "
                    else:
                        line += f"{SYMBOL_EMPTY} "

            lines.append(line.strip())

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Battleship(ships={len(self.ships)}, "
            f"remaining={self.remaining_ships})"
        )

    def _validate_field(self) -> None:
        expected_total = sum(EXPECTED_SHIPS_BY_DECK_SIZE.values())
        actual_total = len(self.ships)

        if actual_total != expected_total:
            raise ValueError(
                f"{expected_total} ships expected, "
                f"but found {actual_total}"
            )

        ships_by_size = {size: 0 for size in EXPECTED_SHIPS_BY_DECK_SIZE}

        for ship in self.ships:
            size = ship.size
            if size not in ships_by_size:
                raise ValueError(f"Invalid ship size: {size}")
            ships_by_size[size] += 1

            for deck in ship.decks:
                for neighbor in get_surrounding_cells([deck.position]):
                    if (
                        neighbor in self.field
                        and self.field[neighbor] is not ship
                    ):
                        raise ValueError(
                            "Invalid placement: ships must not touch "
                            "each other"
                        )

        for size, expected_count in EXPECTED_SHIPS_BY_DECK_SIZE.items():
            actual_count = ships_by_size[size]
            if actual_count != expected_count:
                raise ValueError(
                    f"{expected_count} ship(s) of size {size} required, "
                    f"but found {actual_count}"
                )

    def _should_mark_sunk_area(self, cell: Cell) -> bool:
        for ship in self.ships:
            if not ship.is_drowned:
                continue

            surrounding = get_surrounding_cells(
                [deck.position for deck in ship.decks]
            )

            if cell in surrounding and cell not in self.field:
                return True

        return False
