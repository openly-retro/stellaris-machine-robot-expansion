# Read a traits file which has been hacked up into standard YAML, print out only info we care about
import argparse
from pprint import pprint
from yaml import safe_load
from stellaris_yaml_converter import convert_stellaris_script_to_standard_yaml

def sort_traits_asc():
    pass

def sort_traits_by_leader_class():
    pass

def populate_subclasses_for_related_traits():
    pass

def filter_trait_info(given_trait_dict):
    slim_trait = {}
    trait_name = list(given_trait_dict.keys())[0]
    root = given_trait_dict[trait_name]
    if root.get('negative') == 'yes':
        # Skip negative traits
        return {}
    slim_trait['trait_name'] = trait_name
    slim_trait['leader_class'] = root['leader_class']
    slim_trait['gfx'] = root['inline_script']['ICON']
    # Negative traits don't have a rarity
    # Destiny trait rarity is "paragon"
    slim_trait['rarity'] = root['inline_script']['RARITY']
    is_councilor_trait = True if root['inline_script'].get('COUNCIL') == "yes" else False
    modifier_keys = [
        "triggered_planet_modifier",
        "triggered_sector_modifier",
        "planet_modifier",
        "sector_modifier",
        "councilor_modifier",
        "modifier",
    ]
    for modifier_info in modifier_keys:
        if root.get(modifier_info):
            slim_trait[modifier_info] = root[modifier_info]
    slim_trait["requires_paragon_dlc"] = True if root.get("leader_potential_add", {}).get('has_paragon_dlc') == "yes" else False
    if "subclass" in root.get("leader_potential_add", {}).get("OR",{}).get("has_trait", ""):
        slim_trait["required_subclass"] = root['leader_potential_add']['OR']['has_trait']
    # Destiny traits have a required subclass outside an OR
    elif "subclass" in root.get("leader_potential_add", {}).get("has_trait", ""):
        slim_trait["required_subclass"] = root["leader_potential_add"]["has_trait"]
    # rename a few things
    if slim_trait.get('triggered_planet_modifier'):
        slim_trait['planet_modifier'] = slim_trait.pop('triggered_planet_modifier')
        slim_trait['planet_modifier'].pop('potential')
    if slim_trait.get('triggered_sector_modifier'):
        slim_trait['sector_modifier'] = slim_trait.pop('triggered_sector_modifier')
        slim_trait['sector_modifier'].pop('potential')
    return slim_trait

def get_filtered_traits_for_leader_class(leader_class: str):
    pass


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Mostly converts Stellaris script to standard YAML"
    )
    parser.add_argument('-i', '--infile', help='Stellaris traits file to read')
    args = parser.parse_args()
    buffer = ''
    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    print("0xRetro Stellaris script chopper.. spinning up blades...")
    with open(args.infile, "r") as infile:
        _tmp = convert_stellaris_script_to_standard_yaml(
            infile.read()
        )
        buffer = safe_load(_tmp)
    pprint(buffer)