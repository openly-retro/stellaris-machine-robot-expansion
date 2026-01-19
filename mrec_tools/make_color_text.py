import argparse
import sys

COLOR_CODES = {
    # https://steamcommunity.com/sharedfiles/filedetails/?id=1955978558
    "blue": "§B",       # B = Blue, used in special cases for text.
    "brown": "§L",      # L = Lore text, not relevant game info, just fun to know backstory info.
    "dark_orange": "§S",
    "green": "§G",      # G = Green, used for numbers that are positive modifiers.
    "light_grey": "§T",
    "light_red": "§P",  # P = Pink, Used for more subtle warnings instead of §R.
    "orange": "§H",     # H = Highlight, Orange in Game.
    "magenta": "§M",    # M = Magenta. Indicator for "Rare Techs".
    "red": "§R",        # R = Red, used for numbers that are negative modifier or warnings.
    "teal": "§E",
    "white": "§W",      # W = White.
    "yellow": "§Y",     # Y = Yellow, to be used for stuff that is sub optimal or for certain highlights.
    "cyan": "§C",       # C = Cyan, Used for Concept Text that generates another tooltip.
    "highlight": "§I",   # I = Highlights for Concepts.
    "text": "§T",        # T = Text, standard for all text, to be used if ALL text needs tweaking.
    "event": "§E",       # E = Standard green, used with large chunks of texts, such as events and advisor.
    "green_light": "§S", # S = Subtitle highlight (light green in this case).
    "green_dark": "§V",  # V = Dark Green, used for event text.
    "gray": "§g",        # g = Grey.
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
