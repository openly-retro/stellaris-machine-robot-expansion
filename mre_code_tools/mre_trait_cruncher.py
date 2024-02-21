# Read a traits file which has been hacked up into standard YAML, print out only info we care about
import argparse
from copy import copy
from pprint import pprint
import sys
from yaml import safe_load, safe_dump, load as load_yaml, dump as dump_yaml
from yaml import CLoader as Loader, CDumper as Dumper
from json import dump as json_dump

from mre_common_vars import (
    TRAIT_MODIFIER_KEYS,
    MISSING,
    PLACEHOLDER
)

def sort_traits_asc(list_of_class_specific_traits: list):
    """ Sort traits alphabetically, starting from A, after they've been sorted by class """
    return sorted(list_of_class_specific_traits, key=lambda t: t['trait_name']) 

def iterate_yaml_to_create_filtered_sorted_traits(safe_loaded_blob):
    """ Run on a blob of safe_load data. Pick names, filter data, and sort it
        safe_load gives a dictionary, with trait names in the first-level keys
    """
    trait_collection = {
        "commander": [],
        "official": [],
        "scientist": []
    }
    # Create smaller trait blobs for each class the trait applies to
    for k,v in safe_loaded_blob.items():
        trait = {
            k: v
        }
        # breakpoint()
        if trait[k].get("negative"):
            continue
        for leader_class in ["commander", "scientist", "official"]:
            if leader_class in trait[k]['leader_class']:
                try:
                    filtered_trait = {}
                    filtered_trait[k] = filter_trait_info(
                        trait, for_class=leader_class
                    )
                    trait_collection[leader_class].append(filtered_trait)
                except Exception as ex:
                    sys.exit(
                        f"There was a problem processing this trait: {trait}\nfor class {leader_class}.\nReason: {ex}"
                    )
    return trait_collection

def sort_traits_by_leader_class(filtered_trait_data: dict):
    """ Return 3 categories of leader classes:
        - official (1), scientist (2), commander (3)
        - All traits get sorted into their respective classes
        If a trait can be assigned to multiple classes, then it gets copied to each class
        
        Data that reaches this point will have been run through the `filter_trait_info` function
    """

    trait_collection = {
        "commander": [],
        "official": [],
        "scientist": []
    }
    official = []
    scientist = []
    commander = []
    # Iterate the trait names (the dict keys)
    for trait_name in filtered_trait_data:
        filtered_trait = filtered_trait_data[trait_name]
        # Go thru each allowed leader class, and copy the trait to the respective collection
        for leader_class in filtered_trait["leader_class"]:
            # When appending to a class-specific list, drop the other class names
            # So we can create gui, effects, etc, which all only use one name
            class_specific_trait = copy(filtered_trait)
            class_specific_trait["leader_class"] = leader_class
            trait_collection[leader_class].append(class_specific_trait)
            del class_specific_trait
    return trait_collection


def filter_trait_info(given_trait_dict: dict, for_class=None):
    """ Give our best try to fight PDX script for our sanity
        and to iterate through traits
    """
    slim_trait = {}
    trait_name = [*given_trait_dict][0]
    root = given_trait_dict.get(trait_name)
    if root.get('negative', '') == 'yes':
        # Skip negative traits
        return {}
    slim_trait['trait_name'] = trait_name
    if for_class is not None:
        slim_trait['leader_class'] = for_class
    else:
        if type(root['leader_class']) is list:
            if len(root['leader_class']) == 1:
                slim_trait['leader_class'] = root['leader_class'][0]
            elif len(root['leader_class']) > 1:
                raise Exception(
                    f"This trait, {trait_name}, has more than one leader class, so "
                    "you need to specify which leader class to generate the trait info for."
                )
    # Yes it's more Pythonic to drop the ==, but this is Clausewitz script, which is wildy unpredictable
    if root.get('destiny_trait') == True:
        slim_trait['destiny_trait'] = True
    """ Let's get the icon!
    Oh wait, sometimes there will be more than one "inline_script" key,
    so the second one will overwrite the first.
    In case it's been overwritten, check in the usual place,
    then try to guess the gfx name
    """
    if root['inline_script'].get('ICON'):
        slim_trait['gfx'] = root['inline_script']['ICON']
    else:
        slim_trait['gfx'] = guess_gfx_icon_from_trait_name(trait_name)
    """ Get the trait rarity level, same issue as with ICON """
    slim_trait['rarity'] = root['inline_script'].get('RARITY', MISSING)
    if slim_trait['rarity'] == MISSING:
        slim_trait['rarity'] = guess_rarity_from_trait_data(root)
    if root['inline_script'].get('COUNCIL', False) == True:
        slim_trait["is_councilor_trait"] = True
    
    for modifier_info in TRAIT_MODIFIER_KEYS:
        if root.get(modifier_info):
            _modifiers = copy(root[modifier_info])
            nothing = _modifiers.pop('potential', None)
            slim_trait[modifier_info] = _modifiers
    # A key will be None if the next line is a multi-nested assignment on one line, because PDX script is inconsistent
    if root.get("leader_potential_add", {}) is not None:
        slim_trait["requires_paragon_dlc"] = True if root.get("leader_potential_add", {}).get('has_paragon_dlc') == True else False
    else:
        slim_trait["requires_paragon_dlc"] = False
    # Many ways to find subclasses:
    # 1) We concatenated multiple "has_trait = subclass*" into "has_subclass_trait"
    # 2) It's a single key under leader_potential_add
    # 3) Something else we didnt account for
    if root.get("leader_potential_add", None) is not None: # sad kluge
        if root["leader_potential_add"].get("OR",{}).get("has_subclass_trait"):
            potential_subclass_data = root['leader_potential_add']['OR']['has_subclass_trait']
            if type(potential_subclass_data) is list:
                auto_picked_subclass = pick_correct_subclass_from_potential(
                    slim_trait['leader_class'], potential_subclass_data
                )
                slim_trait["required_subclass"] = auto_picked_subclass
            if type(potential_subclass_data) is str:
                slim_trait["required_subclass"] = potential_subclass_data
        # Destiny traits have a required subclass outside an OR
        # elif "subclass" in root["leader_potential_add"].get("has_trait", ""):
        #     slim_trait["required_subclass"] = root["leader_potential_add"]["has_trait"]
        elif root['leader_potential_add'].get('has_subclass_trait'):
            subclasses_list = root['leader_potential_add']['has_subclass_trait']
            this_trait_req_subclass = pick_correct_subclass_from_potential(
                slim_trait['leader_class'], subclasses_list
            )
            slim_trait["required_subclass"] = this_trait_req_subclass
        elif "subclass" in root['leader_potential_add'].get("has_trait", ""):
            potential_subclass = root["leader_potential_add"]["has_trait"]
            if for_class in potential_subclass:
                slim_trait['required_subclass'] = potential_subclass

        # Look for a rule that says the trait shouldnt be permitted to be added to rulers
        if root["leader_potential_add"].get('is_ruler', None) is not None:
            slim_trait['allow_for_ruler'] = root["leader_potential_add"]['is_ruler']
    # There's never just one predictable way for anything (:
    if root.get('custom_tooltip'):
        slim_trait["custom_tooltip"] = root["custom_tooltip"]
    elif root.get('custom_tooltip_with_modifiers'):
        slim_trait['custom_tooltip'] = root['custom_tooltip_with_modifiers']
    if root.get('triggered_councilor_modifier') or root.get('councilor_modifier'):
        slim_trait["is_councilor_trait"] = True

    return slim_trait

def pick_correct_subclass_from_potential(leader_class, subclass_list):
    """ Select the subclass corresponding to the leader class """
    # Really this isn't 'correct' it just picks 'first'
    matching_subclass = "PLACEHOLDER_VALUE"
    for subclass_option in subclass_list:
        if leader_class in subclass_option:
            matching_subclass = subclass_option
            break
        else:
            1
            # Raise an exception?
    return matching_subclass

def guess_gfx_icon_from_trait_name(trait_name):
    base = trait_name
    if trait_name[-1].isdigit():
        base = trait_name.rsplit('_',1)[0]
    return f"GFX_{base}"

def guess_rarity_from_trait_data(trait_root_data):
    """ Guess rarity.
        In almost all cases where rarity is missing because of a second 'inline_script' key,
        the trait is a veteran trait
        1) try TIER. If it's 3 or 2, veteran; 1: common
        2) Try destiny_trait. then "paragon"
        3) trait ends in '3'; ends in '2'
    """
    # breakpoint()
    approximated_rarity = ''
    if trait_root_data.get('veteran_class_locked_trait', False) or trait_root_data.get('has_subclass_trait', False):
        approximated_rarity = "veteran"
    elif trait_root_data.get('destiny_trait', False):
        approximated_rarity = "paragon"
    else:
        approximated_rarity = "common"
    # approximated_rarity = ''
    # # In the base game, some traits have None for the TIER value
    # if trait_root_data['inline_script'].get('TIER') is not None:
    #     tier_number = int(trait_root_data['inline_script'].get('TIER', 0))
    #     if tier_number:
    #         # TODO: This logic is wrong. There can be T1 veteran traits.
    #         if tier_number == 1:
    #             approximated_rarity = "common"
    #         elif tier_number > 1:
    #             approximated_rarity = "veteran"
    # else:
    #     # More guesswork
    #     if trait_root_data.get('destiny_trait') == True:
    #         approximated_rarity = "paragon"
    # if not approximated_rarity:
    #     sys.exit(f"We couldnt guess rarity from {trait_root_data}!")
    return approximated_rarity


def read_and_write_traits_data(infile, outfile, format):
    with open(infile, "r") as infile:
        # buffer = safe_load(infile.read())
        buffer = load_yaml(infile, Loader=Loader)
    sorted_data = iterate_yaml_to_create_filtered_sorted_traits(buffer)
    if format=="yaml":
        with open(outfile, "w") as useful_traits_yaml:
            # useful_traits_yaml.write(
            #     (sorted_data)
            # )
            dump_yaml(sorted_data, useful_traits_yaml)
        print(f"Wrote crunched traits data from {infile.name} to {outfile}")
    elif format=="json":
        with open(outfile, "w") as useful_traits_json:
            json_dump(sorted_data, useful_traits_json, indent=4)
        print(f"Wrote crunched traits data from {infile.name} to {outfile}")


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Read Stellaris traits in abbreviated wannabe YAML"
    )
    parser.add_argument('--infile', help='Stellaris standard YAML file to read. This should have been processed already with stellaris_yaml_converter.py.', required=True)
    parser.add_argument('--outfile', help="Write filtered traits to a YAML file.", required=False)

    args = parser.parse_args()
    buffer = ''
    sorted_data = ''
    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    print("0xRetro Stellaris script chopper.. spinning up blades...")
    read_and_write_traits_data(args.infile, args.outfile)
