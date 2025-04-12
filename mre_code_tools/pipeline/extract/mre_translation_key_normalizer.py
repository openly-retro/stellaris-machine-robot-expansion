"""
Take the traits from modifiers_l_english.yml, find the uppercase traits, and map them to
mre_<trait_name> keys, with the original modifier as the value.
"""
import os
import re
import sys
import argparse
from json import dump as json_dump
from time import perf_counter

from pipeline.mre_common_vars import BUILD_FOLDER

def pick_uppercase_translation_keys(input_file_object, return_keys=False) -> list:
    uppercase_translation_keys = []
    uppercase_map_dict = {}
    translation_key = re.compile(r"(\w*):\d")
    for line in input_file_object:
        results = re.findall(translation_key, line)
        for result in results:
            if result.isupper() and result.startswith("MOD"):
                # breakpoint()
                if return_keys:
                    uppercase_map_dict[result] = 1
                else:
                    uppercase_translation_keys.append(
                        create_translation_key_map_prepend_mre(result)
                    )
    if return_keys:
        return uppercase_map_dict
    else:
        return uppercase_translation_keys


def create_translation_key_map_prepend_mre(uppercase_key: str):
    return f"mre_{uppercase_key.lower()}:0 \"${uppercase_key}$\""

def do_all_work(base_stellaris_path):
    loc_files_with_uppercase = [
        "modifiers_1_l_english",
        "modifiers_2_l_english",
        "modifiers_3_l_english",
        "megacorp_l_english",
        "paragon_2_l_english"
    ]
    json_outfiles_list = []
    localisations_outfiles_list = []
    for file_identifier in loc_files_with_uppercase:
        _uppercase_keys_dict = {}
        _uppercase_keys_list = []
        loc_filepath = os.path.join(
            base_stellaris_path, 'localisation', 'english', f"{file_identifier}.yml"
        )
        with open(loc_filepath, "r") as loc_file_object:
            _uppercase_keys_dict = pick_uppercase_translation_keys(
                loc_file_object, return_keys=True
            )
            # Set cursor at beginning for reading file again
            loc_file_object.seek(0)
            uppercase_keys_list = pick_uppercase_translation_keys(
                loc_file_object, return_keys=False
            )
        # JSON file will be read by later process
        json_outfile_path = os.path.join(
            BUILD_FOLDER, f"{file_identifier}_upper.json"
        )
        # localisation map needs copy/paste by a human
        localisations_outfile_path = os.path.join(
            BUILD_FOLDER, f"{file_identifier}_upper_map.txt"
        )
        json_outfiles_list.append(json_outfile_path)
        localisations_outfiles_list.append(localisations_outfile_path)
        with open(json_outfile_path, "w") as json_outfile:
            json_dump(_uppercase_keys_dict, json_outfile)
            sys.stdout.write(f"+ Created {json_outfile_path}\n")
        with open(localisations_outfile_path, "w") as loc_outfile:
            loc_outfile.write("\n".join(_uppercase_keys_list))
    sys.stdout.write(
        "Important: These files have localisation keys in them, copy them to \n"
        "\\localisation\\english\\xvcv_mdlc_l_english_uppercase_modifiers_map.yml\n"
    )
    sys.stdout.write(
        f"{'\n'.join(localisations_outfiles_list)}\n"
    )

if __name__=="__main__":
    start_time = perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Read Stellaris traits in abbreviated wannabe YAML"
    )
    parser.add_argument('--infile', help='Location of modifiers_l_english.yml in base Stellaris', required=True)
    parser.add_argument('--outfile', help="Write results to a file.", required=False)
    parser.add_argument(
        '--list_keys', help="Make a dict of the uppercase keys", required=False, default=False,
        action="store_true"
    )
    parser.add_argument(
        '--stellaris_path',
        help='Location of base Stellaris game files',
        required=False
    )
    parser.add_argument(
        '--do_all_work',
        help="Just make all the files so we dont have to input anything.",
        action="store_true", required=False
    )

    args = parser.parse_args()

    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    print("0xRetro Stellaris script chopper.. Let's wrangle some uppercase translation key names for consistency. ")
    if args.do_all_work and not args.stellaris_path:
        sys.exit('You specified to --do_all_work but you need to also specify --base_stellaris_path')
    elif args.do_all_work and args.stellaris_path:
        do_all_work()
    else:
        uppercase_keys_list = []
        uppercase_keys_dict = {}
        with open(args.infile, "r") as modifiers_l_english:
            if args.list_keys:
                uppercase_keys_dict = pick_uppercase_translation_keys(
                    modifiers_l_english, return_keys=True
                )
            else:
                uppercase_keys_list = pick_uppercase_translation_keys(
                    modifiers_l_english, return_keys=False
                )
        target_file = "mre_base_modifiers_translation_map.txt"
        if args.outfile:
            target_file = args.outfile
        with open(target_file, "w") as output_file:
            if args.list_keys:
                json_dump(uppercase_keys_dict, output_file)
            else:
                output_file.write('\n'.join(uppercase_keys_list))
            end_time = perf_counter()
            print(
                f"Look in {output_file.name}.\n "
                f"DONE in {str(end_time - start_time)[:5]} seconds and and hope we never have to run this again."
            )
