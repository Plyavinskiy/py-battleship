from app.battleship import Battleship
from app.constants import GRID_SIZE, SYMBOL_LEGEND_LINES
from app.ship_generator import generate_random_ship_coordinates


def print_symbol_legend() -> None:
    print("\nSYMBOL LEGEND:")
    print("\n".join(SYMBOL_LEGEND_LINES))


def main() -> None:
    ship_coordinates = generate_random_ship_coordinates()
    game = Battleship(ship_coordinates)

    print("\nWelcome to Battleship!")
    print_symbol_legend()
    print("\n" + str(game))

    while not game.is_game_over:
        try:
            user_input = input(
                f"\nEnter target (row column, from 1 to {GRID_SIZE}): "
            )
            parts = user_input.strip().split()

            if len(parts) != 2 or not all(part.isdigit() for part in parts):
                print(f"Please enter two numbers from 1 to {GRID_SIZE}.")
                continue

            row = int(parts[0]) - 1
            column = int(parts[1]) - 1

            if not (0 <= row < GRID_SIZE and 0 <= column < GRID_SIZE):
                print(f"Coordinates must be between 1 and {GRID_SIZE}.")
                continue

            result = game.fire((row, column))
            print(result)
            print("\n" + str(game))

        except ValueError:
            print("Invalid input. Use format: row column (e.g., 5 7)")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            break

    print("\n🔥 All ships are sunk! Game over!")


if __name__ == "__main__":
    main()
