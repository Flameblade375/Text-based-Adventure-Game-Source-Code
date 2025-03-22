# T-BAG (Text-Based Adventure Game)

T-BAG is a text-based RPG game where the player navigates through different rooms, collects items, and avoids monsters to reach the garden and win the game.

## Description

In this game, you start in a hall and must navigate through different rooms, collecting items and avoiding monsters. Your goal is to reach the garden with the key and a potion to win the game.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/T-BAG.git
    ```
2. Navigate to the project directory:
    ```sh
    cd T-BAG
    ```
3. Run the game:
    ```sh
    python T-BAG_main.py
    ```

## Usage

- Use the `go` command to move to a different room. For example:
    ```sh
    go east
    ```
- Use the [get](http://_vscodecontentref_/0) command to pick up an item. For example:
    ```sh
    get key
    ```
- Use the [quit](http://_vscodecontentref_/1) command to exit the game. For example:
    ```sh
    quit 5
    ```

## Commands

- `go [direction]`: Move to a different room.
- [get [item]](http://_vscodecontentref_/2): Pick up an item from the room.
- [quit [seconds]](http://_vscodecontentref_/3): Quit the game after waiting for the specified number of seconds.
- `help [number]`: Show the list of commands. If a number is provided, show that many commands; otherwise, show all commands.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
