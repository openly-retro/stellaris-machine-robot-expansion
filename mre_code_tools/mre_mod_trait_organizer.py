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

import sys
from json import load as json_load
import argparse

TRAITS_TO_EXCLUDE = (
    "trait_ruler_champion_of_the_people",  # Machines not affected by happiness
    "leader_trait_aturion_organizer", # Neither happiness nor ethics are used
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

def trait_qualifies_for_leader_making(trait_dict):
    is_leader_making_trait = False
    if not trait_dict.get('councilor_modifier') and \
        not trait_dict.get('triggered_councilor_modifier') and \
        "ruler" not in trait_dict["trait_name"]:
        is_leader_making_trait = True
    return is_leader_making_trait

def trait_qualifies_for_core_modifying(trait_dict):
    is_core_modifying_trait = False
    # Ruler is a type of councilor, so these modifiers will work
    if trait_dict.get('self_modifier') or \
        "ruler" in trait_dict['trait_name'] or \
        trait_dict.get('councilor_modifier') or \
        trait_dict.get('triggered_councilor_modifier'):
        is_core_modifying_trait = True
    return is_core_modifying_trait

def pick_highest_tier_of_trait(list_of_traits):
    pass


def do_qa_on_pipeline_files(traits_list):
    """ Quick QA check to find potential missing data """
    rogue_trait_names = []
    sys.stdout.write("** Checking for any issues with trait data ... **")
    for trait in traits_list:
        issues = []
        trait_key = [*trait][0]
        root = trait[trait_key]
        # if trait_key == "leader_trait_bellicose":
        #     breakpoint()
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
        '--find_issues', required=False,
        help="Put together a list of trait names where the trait data doesn't have any known modifiers.",
        action="store_true"
    )
    args = parser.parse_args()
    with open(args.infile, "r") as input_file:
        buffer = json_load(input_file)
        if args.find_issues:
            do_qa_on_pipeline_files(buffer)
