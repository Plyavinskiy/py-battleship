from app.battleship import Battleship, generate_random_ship_coordinates


def main() -> None:
    ship_coordinates = generate_random_ship_coordinates()
    game = Battleship(ship_coordinates)

    print("\nWelcome to Battleship!\n")
    print(game)

    while not game.is_game_over():
        try:
            target_input = input("\nEnter target (row column): ")
            target_row, target_column = map(int, target_input.strip().split())

            if not (0 <= target_row < 10 and 0 <= target_column < 10):
                print("Coordinates must be between 0 and 9.")
                continue

            shot_result = game.fire((target_row, target_column))
            print(shot_result)
            print(game)

        except ValueError:
            print("Invalid input. Use format: row column (e.g., 2 3)")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            break

    print("\n🔥 All ships are sunk! Game over!")


if __name__ == "__main__":
    main()
