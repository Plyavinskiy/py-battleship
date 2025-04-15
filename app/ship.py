from app.constants import SHIP_AFLOAT, SHIP_DROWNED
from app.deck import Deck
from app.types import Cell


class Ship:
    __slots__ = ("decks",)

    def __init__(self, start: Cell, end: Cell) -> None:
        self.decks: list[Deck] = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                position = (start_row, column)
                self.decks.append(Deck(position=position))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                position = (row, start_column)
                self.decks.append(Deck(position=position))
        else:
            raise ValueError("Ship must be placed in a straight line")

    def get_deck(self, position: Cell) -> Deck:
        for deck in self.decks:
            if deck.position == position:
                return deck
        raise ValueError(f"Deck not found at {position}")

    def fire(self, position: Cell) -> None:
        self.get_deck(position).hit()

    def get_size(self) -> int:
        return len(self.decks)

    @property
    def is_drowned(self) -> bool:
        return all(not deck.is_alive for deck in self.decks)

    def __repr__(self) -> str:
        status = SHIP_DROWNED if self.is_drowned else SHIP_AFLOAT
        return f"Ship(size={self.get_size()}, status={status})"
