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
        return (
            f"Deck(row={self.row}, column={self.column}, status={status})"
        )
