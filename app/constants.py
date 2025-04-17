# Game board size (10 rows × 10 columns)
GRID_SIZE = 10

# Number of ships per deck size
EXPECTED_SHIPS_BY_DECK_SIZE = {
    1: 4,  # Single-deck ships
    2: 3,  # Double-deck ships
    3: 2,  # Triple-deck ships
    4: 1,  # Four-deck ships
}

# Board symbols (Unicode)
SYMBOL_ALIVE = "□"    # U+25A1
SYMBOL_AROUND = "✖"   # U+2716
SYMBOL_EMPTY = "·"    # U+00B7
SYMBOL_MISS = "•"     # U+2022
SYMBOL_SUNK = "■"     # U+25A0

# Symbol legend (displayed at the start of the game)
SYMBOL_LEGEND_LINES = [
    f"  {SYMBOL_ALIVE} — alive deck",
    f"  {SYMBOL_SUNK} — sunk or hit deck",
    f"  {SYMBOL_EMPTY} — untouched cell",
    f"  {SYMBOL_MISS} — missed shot",
    f"  {SYMBOL_AROUND} — surrounding area"
]

# Deck status values
DECK_ALIVE = "alive"
DECK_HIT = "hit"

# Ship status values
SHIP_AFLOAT = "afloat"
SHIP_DROWNED = "drowned"

# Messages shown after a shot
SHOT_HIT = "Hit!"
SHOT_MISS = "Miss!"
SHOT_REPEAT = "You already fired at this location."
SHOT_SUNK = "Sunk!"
