""" Look in base game files and create a map of which traits have machine descriptions for them """

import os
import re
import sys
import argparse
from json import dump as json_dump
from time import perf_counter

from pipeline.mre_common_vars import BUILD_FOLDER

machine_tooltip = re.compile(r"(?P<trait_name>\w*trait\w*)_machine:")

def identify_machine_tooltip(file_line):
    machine_trait = False
    if localisation_key := re.search(machine_tooltip, file_line):
        machine_trait = localisation_key.groupdict()['trait_name']
    return machine_trait

def iterate_lines_collect_machine_localisations(file_object) -> dict:
    traits_with_machine_localisations = []
    for line in file_object:
        if result := identify_machine_tooltip(line):
            traits_with_machine_localisations.append(result)
    return traits_with_machine_localisations

def do_all_work(base_stellaris_path):
    localisation_files_to_examine = [
        "main_1_l_english.yml",
        "main_2_l_english.yml",
        "main_3_l_english.yml",
        "leaders_l_english.yml",
        "paragon_4_l_english.yml",
    ]
    all_traits_machine_localisations_list = []
    for loc_yml in localisation_files_to_examine:
        localisation_file_path = os.path.join(
            base_stellaris_path,
            'localisation', 'english', loc_yml
        )
        with open(localisation_file_path, "r") as vanilla_localisation:
            collected_machine_localisations = iterate_lines_collect_machine_localisations(vanilla_localisation)
            all_traits_machine_localisations_list = [*all_traits_machine_localisations_list, *collected_machine_localisations]
    all_traits_machine_localisations = {
        trait_name: 1
        for trait_name in sorted(all_traits_machine_localisations_list)
    }
    outfile = "98_traits_with_machine_localisations.json"
    outfile_path = os.path.join(BUILD_FOLDER, outfile)
    with open(outfile_path, "w") as json_outfile:
        # nice_and_sorted = sorted(all_traits_machine_localisations, key=lambda x: [*x][0]) 
        json_dump(all_traits_machine_localisations, json_outfile, indent=4)
    print(
        f"** Traits which have machine localisations are in .\\build\\{outfile}\n"
        "Now to get the machine version append _machine to these trait names for a nice tooltip.\n"
        "And _machine_desc for even more immersion."
    )
    
# G:\SteamLibrary\steamapps\common\Stellaris\
    
if __name__=="__main__":
    start_time = perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Read Stellaris traits in abbreviated wannabe YAML"
    )
    parser.add_argument('--stellaris_path', help='Location of Stellaris game folder', required=True)
    args = parser.parse_args()

    print("0xRetro Stellaris script chopper..")
    print("Let's find out which leader traits have machine localisations!")
    do_all_work(args.stellaris_path)
    end_time = perf_counter()
    execution_time = end_time - start_time
    sys.stdout.write(
        f"\nDone in {str(execution_time)[:5]} seconds"
    )