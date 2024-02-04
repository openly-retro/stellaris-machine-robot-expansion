"""
Once the base trait files have been crunched,
we have 3 files with the three classes' traits,
nicely organized and sorted alphabetically.

Traits will need to be filtered for whether they'll work 
in the leader-making feature, and the core-modifying feature.
Not all traits can be used by both features,
so in this script we further filter and sort traits
for those two features.

We also need some functionality to pick the highest rank of a 
given trait, and give that to players, to avoid overwhelming the
UI with dozens of traits.
Thankfully, in pre-processing, traits are sorted alphabetically and
it'll be easy to get the highest rank of that trait series.
"""
from copy import copy
import os
import sys
from json import load as json_load
import argparse

from run_mre_trait_pipeline import (
    BUILD_FOLDER,
    LEADER_CLASSES
)

TRAITS_TO_EXCLUDE = (
    "leader_trait_intemporal", # Does nothing, no effects, no custom tooltip
)

MODIFIERS = (
    "army_modifier",
    "councilor_modifier",
    "fleet_modifier",
    "modifier",
    "planet_modifier",
    "sector_modifier",
    "self_modifier",
    "triggered_army_modifier",
    "triggered_councilor_modifier",
    "triggered_fleet_modifier",
    "triggered_planet_modifier",
    "triggered_sector_modifier",
    "triggered_self_modifier",
)

def trait_qualifies_for_leader_making(trait_dict: dict) -> bool:
    is_leader_making_trait = False
    if not any(
        [
            trait_dict.get('councilor_modifier'),
            trait_dict.get('triggered_councilor_modifier'),
            "ruler" in trait_dict['trait_name'],
            trait_dict.get('is_councilor_trait'),
        ]
    ):
        is_leader_making_trait = True
    return is_leader_making_trait

def trait_qualifies_for_core_modifying(trait_dict: dict) -> bool:
    is_core_modifying_trait = False
    # Ruler is a type of councilor, so these modifiers will work
    if any(
        [
            "ruler" in trait_dict['trait_name'],
            trait_dict.get('self_modifier'),
            trait_dict.get('councilor_modifier'),
            trait_dict.get('triggered_councilor_modifier')
        ]
    ):
        is_core_modifying_trait = True
    # breakpoint()
    return is_core_modifying_trait

def pick_highest_tier_of_trait(list_of_traits):
    # Drop traits that have a higher tier of trait
    # Thankfully all our data is alphabetically sorted so "this will be simple" (Famous Last Words)
    tier_tracker = {}
    list_of_traits_copy = copy(list_of_traits)
    position_in_list = 0
    for trait in list_of_traits:
        trait_level = 1
        current_trait_name = [*trait][0]
        if current_trait_name[-1].isdigit():
            current_trait_name_series, trait_level = current_trait_name.rsplit('_', 1)
            trait_level = int(trait_level)
        else:
            current_trait_name_series = current_trait_name
        print(f"Evaluating {current_trait_name} in series {current_trait_name_series}")
        # Is the next trait in the same series? If so, pop it off the copy
        # If there is no next trait (end of list) we have evaluated the highest in the series
        if position_in_list+1 == len(list_of_traits):
            # Nothing to do
            continue
        else:
            next_trait = list_of_traits[position_in_list+1]
            next_trait_name = [*next_trait][0]
            # If the next trait in the list doesn't have a number at the end, it's a new series
            # And this trait we were looking at is the highest in its series
            print(f"Comparing it to {next_trait_name}")
            if current_trait_name_series == get_trait_series_name(next_trait_name):
                print(f"Next trait is in the same series, so drop current trait")
                list_of_traits_copy.remove(trait)
        position_in_list = position_in_list + 1
    return list_of_traits_copy

def get_trait_series_name(trait_name: str) -> str:
    name_series = trait_name
    if trait_name[-1].isdigit():
        name_series = trait_name.rsplit('_',1)[0]
    return name_series


def filter_traits_by_mod_feature(traits_list: list) -> dict:
    """ Organize traits by whether it should go to the leader-making feature or core-modifying """

    leader_making_traits = []
    core_modifying_traits = []
    outliers = []
    for trait in traits_list:
        trait_name = [*trait][0]
        root = trait[trait_name]
        if trait_qualifies_for_core_modifying(root):
            core_modifying_traits.append(trait)
        if trait_qualifies_for_leader_making(root):
            leader_making_traits.append(trait)
        if not trait_qualifies_for_core_modifying and not trait_qualifies_for_leader_making:
            # No idea how this could happen.. but
            outliers.append(trait)
    return {
        "leader_making_traits": leader_making_traits,
        "core_modifying_traits": core_modifying_traits,
        "outliers": outliers
    }



def do_qa_on_pipeline_files(traits_list):
    """ Quick QA check to find potential missing data """
    rogue_trait_names = []
    sys.stdout.write("** Checking for any issues with trait data ... **")
    for trait in traits_list:
        issues = []
        trait_key = [*trait][0]
        root = trait[trait_key]
        missing_modifiers = not any([bool(root.get(modifier)) for modifier in MODIFIERS])
        if missing_modifiers and not root.get("custom_tooltip"):
            issues.append(
                f"Trait has no modifiers, and is !!missing!! custom_tooltip (BAD)"
            )
        if root.get('councilor_modifier') or root.get('triggered_councilor_modifier'):
            if root.get("is_councilor_trait") != True:
                issues.append(
                    "Trait has councilor modifiers but is_councilor_trait is NOT set"
                )
        if len(issues):
            rogue_trait_names.append(
                f"{trait_key} ... {','.join(issues)}"
            )
    if len(rogue_trait_names):
        sys.stdout.write(f"** Found {len(rogue_trait_names)} traits needing review:\n")
        for trait_name in rogue_trait_names:
            sys.stdout.write(f"{trait_name}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Machine & Robot Expansion Data Tools",
        description="Do operations on filtered data crunched from base trait files"
    )
    parser.add_argument('--infile', help='A traits JSON file that we processed, like 00_mre_commander_traits.json, created from the pipeline script.')
    parser.add_argument(
        '--qa', required=False,
        help="Put together a list of trait names where the trait data doesn't have any known modifiers.",
        action="store_true"
    )
    parser.add_argument(
        '--qa_all',
        action="store_true",
        help="Checks traits for issues, in all 3 files produced by run_me_trait_pipeline.py"
    )
    args = parser.parse_args()
    if args.infile and args.qa:
        with open(args.infile, "r") as input_file:
            buffer = json_load(input_file)
            do_qa_on_pipeline_files(buffer)
    elif args.qa_all:
        if not os.path.exists(BUILD_FOLDER):
            sys.exit(
                'Couldnt find the build folder. Run this from within the mre_code_tools folder, '
                'and make sure that "run_mre_trait_pipeline" was run.'
            )
        pipeline_output_files = [
            f"00_mre_{leader_class}_traits.json" for leader_class in LEADER_CLASSES
        ]
        for filename in pipeline_output_files:
            input_file = os.path.join('build', filename)
            with open(input_file, "r") as input_file:
                sys.stdout.write(
                    f"Results for {input_file.name}:\n"
                )
                buffer = json_load(input_file)
                do_qa_on_pipeline_files(buffer)
    