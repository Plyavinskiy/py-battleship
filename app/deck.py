from dataclasses import dataclass

from app.constants import DECK_ALIVE, DECK_HIT


@dataclass(slots=True)
class Deck:
    row: int
    column: int
    is_alive: bool = True

    def hit(self) -> None:
        self.is_alive = False

    def __repr__(self) -> str:
        status = DECK_ALIVE if self.is_alive else DECK_HIT
        return (
            f"Deck(row={self.row}, column={self.column}, status={status})"
        )
