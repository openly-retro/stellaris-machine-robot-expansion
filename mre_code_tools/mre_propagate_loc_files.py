""" Tool to copy Stellaris localisation files to another localisation language 
This does NOT do translations of content. """
import sys
import os
import argparse
from glob import glob as file_glob
import copy
from time import perf_counter

__author__ = '0xRetro (Openly Retro)'
__license__ = 'GPLv3'

LANGUAGES = [
    'english',
    'braz_por',
    'french',
    'german',
    'polish',
    'russian',
    'simp_chinese',
    'spanish',
    'japanese',
    'korean',
]

if __name__ == '__main__':
    start_time = perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris Localisation Copy Machine",
        description="Mass copy all your localisation files to other language folders, and change language keys for each. "\
                    f" Supported language names: {LANGUAGES}."
    )
    parser.add_argument(
        "--source-language",
        dest="source_language",
        help="Specify the source language to copy localisations from, to all other languages. (Required)",
        required=True
    )
    parser.add_argument(
        "--skip-languages",
        nargs="+",
        dest="skip_languages",
        help="Any languages you want to skip copying to, separated by spaces. (Optional)",
        default=[]
    )
    parser.add_argument(
        "--skip-confirm",
        action="store_true",
        default=False,
        help="Use this flag to skip confirmations, for example if you are running this as part of another process. (Optional)"
    )

    if not os.path.isdir(
        'localisation'
    ):
        sys.exit(
            "Run this command from your mod's base folder. "
            "Couldn't find the localisation folder."
        )
    args = parser.parse_args()
    # Now that's out of the way
    print("*~~ 0xRetro Stellaris Localisation Copy Machine ~~*\n")
    print(
        "This tool copies localisations files from the source language you specify, "
        "to other localisation language folders. It changes the l_<language>: key at the top of the file "
        "to the target language you are copying to, for all targeted languages.\n"
    )

    if args.source_language not in LANGUAGES:
        sys.exit(
            f"{args.source_language} is not in the list of supported languages."
        )
    if args.skip_languages and any([
        skipped_language not in LANGUAGES
        for skipped_language in args.skip_languages 
    ]):
        sys,exit(
            "One or more of the languages you specified aren't in the list of supported languages.\n"
            f"You wanted to skip: {args.skip_languages}."
        )
    dest_languages = set(LANGUAGES).difference(set([args.source_language]))
    if args.skip_languages:
        dest_languages = dest_languages.difference(args.skip_languages)

    if not args.skip_confirm:
        if not input(
            f"Please confirm: Going to copy {args.source_language} to these languages: {dest_languages}. "
            "Does that look correct? Enter y/[N] > "
        ) == 'y':
            sys.exit("You did not type 'y'. Exiting ... ")
    else:
        print(f"Copying from {args.source_language} to these languages: {dest_languages}")

    localisation_folder = 'localisation'
    if args.skip_languages:
        print(f"Skipping copying to {args.skip_languages}")
    source_localisation_files = file_glob(
        os.path.join(os.getcwd(), localisation_folder, args.source_language, '*.yml')
    )

    for source_file in source_localisation_files:
        buffer = ''
        with open(source_file, mode="r", encoding="utf-8") as stellaris_localisation_yaml:
            buffer = stellaris_localisation_yaml.read()
        print(f"Starting copy from {os.path.basename(source_file)} to other localisations ...")
        for to_language in dest_languages:
            # Swap 'english' for 'braz_por', for example
            new_language_copy_filename = source_file.replace(
                args.source_language, to_language
            )
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
                target_file_copy.write(
                    contents_copy.encode('utf-8-sig')
                )
    end_time = perf_counter()
    execution_time = end_time - start_time
    print(f"\nDone in {str(execution_time)[:5]} seconds.")
