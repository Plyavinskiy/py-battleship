# Grid size: 10x10
GRID_SIZE = 10

# Expected ships grouped by deck size (decks per ship)
EXPECTED_SHIPS_BY_DECK_SIZE = {
    1: 4,  # Single-deck
    2: 3,  # Double-deck
    3: 2,  # Triple-deck
    4: 1,  # Four-deck
}

# Ordered ship sizes used for random generation
RANDOM_SHIP_SIZES = [4] + [3] * 2 + [2] * 3 + [1] * 4

# Unicode symbols for board display
SYMBOL_ALIVE = "□"  # U+25A1
SYMBOL_SUNK = "■"   # U+25A0
SYMBOL_MISS = "•"   # U+2022
SYMBOL_AROUND = "✖"  # U+2716
SYMBOL_EMPTY = "·"   # U+00B7

# Symbol legend (shown before the game starts)
SYMBOL_LEGEND_LINES = [
    f"  {SYMBOL_ALIVE} — alive deck",
    f"  {SYMBOL_SUNK} — sunk or hit deck",
    f"  {SYMBOL_MISS} — missed shot",
    f"  {SYMBOL_AROUND} — surrounding area",
    f"  {SYMBOL_EMPTY} — untouched cell",
]

# Deck status labels
DECK_ALIVE = "alive"
DECK_HIT = "hit"

# Ship status labels
SHIP_AFLOAT = "afloat"
SHIP_DROWNED = "drowned"

# Shot result messages
SHOT_HIT = "Hit!"
SHOT_SUNK = "Sunk!"
SHOT_MISS = "Miss!"
