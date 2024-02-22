import argparse
import sys

COLOR_CODES = {
    # https://steamcommunity.com/sharedfiles/filedetails/?id=1955978558
    "blue": "§B",
    "brown": "§L",
    "dark_orange": "§S",
    "green": "§G",
    "light_grey": "§T",
    "light_red": "§P",
    "orange": "§H",
    "purple": "§M",
    "red": "§R",
    "teal": "§E",
    "white": "§W",
    "yellow": "§Y",
}
CLOSE_CODE = "§!"

def make_color_text(color, some_text: str) -> str:
    return f"\"{COLOR_CODES[color]}{some_text}{CLOSE_CODE}\""

if __name__ == "__main__":
    # start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        description=(
            "0xRetro Stellaris Happy Funtime Text Colorizer! Make colored text to put in a Stellaris localisations file or use however else you'd like."
        )
    )
    parser.add_argument(
        '--color',
        help="options are: blue, brown, dark_orange, green, light_grey, light_red, orange, purple, red, teal, white, yellow",
        required=True,
        action="store"
    ),
    parser.add_argument(
        '--text',
        help="Any string of text that you want wrapped in the color code of your choice.",
        action="store",
        dest="text_for_coloring",
        required=True
    )
    args = parser.parse_args()
    if not COLOR_CODES.get(args.color):
        sys.exit(f"{args.color} wasn't a known color. Check help options.")
    sys.stdout.write(
        make_color_text(args.color, args.text_for_coloring)
    )
