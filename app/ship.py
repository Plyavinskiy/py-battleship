from app.deck import Deck


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = False
        self.decks: list[Deck] = []

        start_row, start_column = start
        end_row, end_column = end

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                self.decks.append(Deck(row=start_row, column=column))
        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                self.decks.append(Deck(row=row, column=start_column))

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
        return (
            f"Ship(size={self.get_size()}, status={status})"
        )
