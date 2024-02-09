"""
Take the traits from modifiers_l_english.yml, find the uppercase traits, and map them to
mre_<trait_name> keys, with the original modifier as the value.
"""
import re
import sys
import argparse
from json import dump as json_dump
from time import perf_counter

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

    args = parser.parse_args()

    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    print("0xRetro Stellaris script chopper.. Let's wrangle some uppercase translation key names for consistency. ")
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
