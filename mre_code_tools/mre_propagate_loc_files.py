import sys
import os
import argparse
from glob import glob as file_glob
import copy

LANGUAGES = [
    'english',
    'braz_por',
    'french',
    'german',
    'polish',
    'russian',
    'simp_chinese',
    'spanish',
    'japanese'
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris Localisation Copy Machine",
        description="Mass copy all your localisation files to other language folders, and change language keys for each."
    )
    parser.add_argument(
        "--source-language",
        default="english",
        dest="source_language",
        help="Specify the source language to copy localisations from, to all other languages. (Optional)"
    )
    parser.add_argument(
        "--skip-language",
        nargs="+",
        dest="skip_languages",
        help="Any languages you want to skip copying to, separated by spaces. (Optional)",
        default=[]
    )

    if not os.path.isdir(
        'localisation'
    ):
        sys.exit(
            "Run this command from your mod's base folder. "
            "Couldn't find the localisation folder."
        )
    args = parser.parse_args()
    if args.source_language not in LANGUAGES:
        sys.exit(
            f"{args.source_language} is not in the list of known languages."
        )
    if args.skip_languages and any([
        skipped_language not in LANGUAGES
        for skipped_language in args.skip_languages 
    ]):
        sys,exit(
            "One or more of the languages you specified aren't in the list of known languages. "
            f"You wanted to skip: {args.skip_languages}"
        )
    # Last confirmation
    dest_languages = set(LANGUAGES).difference(set([args.source_language]))
    if args.skip_languages:
        dest_languages = dest_languages.difference(args.skip_languages)

    if not input(
            f"Confirmation: Going to copy {args.source_language} to these languages: {dest_languages}. "
            "Does that look correct? Enter y/[N] > "
        ) == 'y':
            sys.exit("You did not type 'y'. Exiting ... ")

    # Now that's out of the way
    localisation_folder = 'localisation'
    print(f"Going to copy {args.source_language} to other localisation folders.")
    if args.skip_languages:
        print(f"Except for {args.skip_languages}")
    source_localisation_files = file_glob(
        os.path.join(os.getcwd(), localisation_folder, args.source_language, '*.yml')
    )

    for source_file in source_localisation_files:
        buffer = ''
        with open(source_file, mode="r", encoding="utf-8") as stellaris_localisation_yaml:
            buffer = stellaris_localisation_yaml.read()
        
        for to_language in dest_languages:
            # Swap 'english' for 'braz_por', for example
            new_language_copy_filename = source_file.replace(
                args.source_language, to_language
            )
            """ The file is open.
            If I replace 'english' with 'braz_por' """
            print(f"*** {to_language.upper()} ***")
            # TODO: A better memory efficient way to do this
            contents_copy = copy.copy(buffer)
            contents_copy = contents_copy.replace(
                f"l_{args.source_language}", f"l_{to_language}"
            )
            with open(
                os.path.join(
                    os.getcwd(), 'localisation', to_language, new_language_copy_filename
                ), "wb"
            ) as target_file_copy:
                print(
                    f"Writing copy of {source_file} to {new_language_copy_filename}.."
                )
                target_file_copy.write(
                    contents_copy.encode('utf-8-sig')
                )
    print("** DONE **")
