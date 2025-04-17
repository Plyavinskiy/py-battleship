from app.battleship import Battleship
from app.constants import GRID_SIZE, SYMBOL_LEGEND_LINES
from app.input_utils import is_within_bounds, prompt_for_coordinates
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
            coordinates = prompt_for_coordinates()

            if coordinates is None:
                print(f"Please enter two numbers from 1 to {GRID_SIZE}.")
                continue

            row, column = coordinates

            if not is_within_bounds(row, column):
                print(f"Coordinates must be between 1 and {GRID_SIZE}.")
                continue

            result = game.fire((row, column))
            print(result)
            print("\n" + str(game))

        except ValueError:
            print("Invalid input. Please enter two numbers (e.g., 5 7).")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            break

    print("\n🔥 All ships are sunk! Game over!")


if __name__ == "__main__":
    main()
