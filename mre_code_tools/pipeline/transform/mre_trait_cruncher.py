# Read a traits file which has been hacked up into standard YAML, print out only info we care about
import argparse
from copy import copy
from dataclasses import dataclass
from enum import Enum
from pprint import pprint
import sys
# from yaml import safe_load, safe_dump, load as load_yaml, dump as dump_yaml
# from yaml import CLoader as Loader, CDumper as Dumper
from json import dump as json_dump

from pipeline.mre_common_vars import (
    LEADER_CLASSES,
    TRAIT_MODIFIER_KEYS,
    MISSING,
    PLACEHOLDER
)

def sort_traits_asc(list_of_class_specific_traits: list):
    """ Sort traits alphabetically, starting from A, after they've been sorted by class """
    return sorted(list_of_class_specific_traits, key=lambda t: t['trait_name']) 


def filter_trait_info(given_trait_dict: dict, for_class=None):
    """ Give our best try to fight PDX script for our sanity
        and to iterate through traits
    """
    slim_trait = {}
    trait_name = given_trait_dict['trait_name']
    root = given_trait_dict
    # breakpoint()
    if root.get('leader_trait_type', '') == 'negative':
        # Skip negative traits
        return {}
    # Skip 'triggered' traits
    if council_value := root['inline_script'].get('COUNCIL', False):
        if council_value == "triggered":
            print(
                f"Skipped {trait_name} because it is a triggered / special trait"
            )
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
    if root.get('leader_trait_type') == "destiny":
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
    
    for modifier_info in TRAIT_MODIFIER_KEYS:
        if root.get(modifier_info):
            _modifiers = copy(root[modifier_info])
            nothing = _modifiers.pop('potential', None)
            slim_trait[modifier_info] = _modifiers
    # A key will be None if the next line is a multi-nested assignment on one line, because PDX script is inconsistent
    if root.get("leader_potential_add"):

        slim_trait["requires_paragon_dlc"] = True if root.get("leader_potential_add", {}).get('has_paragon_dlc') == True else False
        # Start harvesting this in order to build triggers to check the trait can be added
        slim_trait["leader_potential_add"] = root["leader_potential_add"]
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
        slim_trait['custom_tooltip_with_modifiers'] = root['custom_tooltip_with_modifiers']
    # Yet another new way in 3.11 to have custom tooltip text
    if triggered_desc_text := root.get('triggered_desc', {}).get('text', None):
        slim_trait['custom_tooltip'] = triggered_desc_text
    if root.get('triggered_councilor_modifier') or root.get('councilor_modifier'):
        slim_trait["is_councilor_trait"] = True
    if root.get('force_councilor_trait'):
        slim_trait["is_councilor_trait"] = True
    if 'COUNCIL' in root.get('inline_script'):
        if root['inline_script']['COUNCIL'] == False:
            slim_trait["is_councilor_trait"] = False
        # Yes there's a more pythonic way, don't lecture me, it's 12:03 AM
        elif root['inline_script']['COUNCIL'] == True:
            slim_trait["is_councilor_trait"] = True
            # print(f'Council trait detected for {trait_name} from inline_script COUNCIL key')
    # Galcom stuff
    if root.get('galcom_modifier'):
        slim_trait['galcom_modifier'] = root['galcom_modifier']
    # federation modifiers
    if root.get('federation_modifier'):
        slim_trait['federation_modifier'] = root['federation_modifier']

    # Collect prerequisites in order to determine certain DLC requirements
    if root.get('prerequisites'):
        # Simple convert to list, also captures just 1 string
        slim_trait['prerequisites'] = root['prerequisites']

    return slim_trait

def qa_trait(slim_trait: dict) -> bool:
    """ Sanity checks on our lil trait """
    if not slim_trait.get('trait_name'):
        raise KeyError(f"Where the hell is 'trait_name' in {slim_trait}")
    if slim_trait['leader_class'] not in LEADER_CLASSES:
        raise KeyError(f"WhatInTheShroud is this leader class? : {slim_trait}")
    if slim_trait['rarity'] not in ['common','veteran','destiny','paragon']:
        raise ValueError(f"Trait rarity : {slim_trait['rarity']} : is unknown")
    if slim_trait.get('requires_paragon_dlc') == False and slim_trait.get('leader_potential_add', {}).get('has_paragon_dlc', '') == "yes":
        raise ValueError(
            f"The trait says it doesnt require paragons but the leader add does! : {slim_trait}"
        )
    return True


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
    """ Take rarity from leader_trait_type; if not present, it's common """
    approximated_rarity = 'common'
    if declared_rarity := trait_root_data.get("leader_trait_type", None):
        if declared_rarity == "destiny":
            approximated_rarity = "paragon"
        else:
            approximated_rarity = declared_rarity

    return approximated_rarity

class LeaderType(Enum):
    COMMANDER = "commander"
    OFFICIAL = "official"
    SCIENTIST = "scientist"

class TraitRarity(Enum):
    COMMON = "common"
    VETERAN = "veteran"
    PARAGON = "paragon"
    DESTINY = "destiny"


@dataclass
class SlimTrait:
    trait_name: str
    council_value: str
    leader_class: LeaderType
    rarity: TraitRarity
    gfx: str = ''               # optional
    
